//! Library for the docextractor executable.
//!
//! It consists of functions to extract content from the AST and
//! to write the content to an RST or MD file. The crate is tested on itself,
//! so all the documentation in the crate is in RST. The tests for Markdown
//! are done on the dependencies.

mod directives;
mod formats;

use std::fs::{create_dir_all, read_to_string, File};
use std::io::Write;
use std::path::{Path, PathBuf};

use serde::Deserialize;

use crate::directives::{
    CrateDirective,
    Directive,
    DirectiveVisibility,
    ExecutableDirective,
    ModuleDirective,
};
use crate::formats::Format;

#[derive(Debug, Deserialize)]
pub struct Configuration {
    crate_name: String,
    src_dir: PathBuf,
    doc_dir: PathBuf,
    #[serde(default)]
    force: bool,
    #[serde(default)]
    format: Format,
    #[serde(default)]
    visibility: DirectiveVisibility,
}

impl Configuration {
    // noinspection RsLiveness
    /// Canonicalize the source and documents directory.
    ///
    /// The method checks that the directories exist and have proper permissions
    /// before updating them with their canonical paths.
    ///
    /// Panics:
    /// * If the source directory is not a directory or cannot be accessed.
    /// * If the documents directory cannot be created.
    fn canonicalize(&mut self) -> &mut Self {
        if !self.src_dir.is_dir() {
            panic!("{} is not a directory", self.src_dir.to_str().unwrap());
        }

        // Check if it ends with src, and convert to owned value
        if !self.src_dir.ends_with("src") {
            self.src_dir = self.src_dir.join("src");
        }

        // Canonicalize, which also checks that it exists.
        self.src_dir = match self.src_dir.canonicalize() {
            Ok(d) => d,
            Err(e) => panic!("Could not find crate source directory: {e}"),
        };

        // Check if the output directory ends with the crate name
        if !self.doc_dir.ends_with(&self.crate_name) {
            self.doc_dir = self.doc_dir.join(&self.crate_name);
        }

        // Create output directory and canonicalize it.
        // Canonicalize fails if the output_dir doesn't exist, so it is also a
        // good check for permissions.
        create_dir_all(&self.doc_dir).unwrap();
        self.doc_dir = match self.doc_dir.canonicalize() {
            Ok(d) => d,
            Err(e) => panic!("Could not create the output directory: {e}"),
        };

        self
    }

    fn get_doc_file_name(&self, file_name: &Path) -> String {
        let rel_path = file_name.strip_prefix(&self.src_dir).unwrap_or(file_name);

        // For mod.rs files, the output file name is the parent directory name.
        // Otherwise, it is same as the file name.
        let doc_file_name = if rel_path.ends_with("mod.rs") {
            rel_path.parent().unwrap().to_owned()
        }
        else {
            rel_path
                .parent()
                .unwrap()
                .join(rel_path.file_stem().unwrap())
        };

        // Convert to absolute path and add the extension.
        // Cannot use canonicalize here since it will error.
        let doc_file_name = self
            .doc_dir
            .join(doc_file_name)
            .to_str()
            .unwrap()
            .to_string()
            + self.format.extension();

        // Create the parent directory if required
        create_dir_all(self.doc_dir.join(&doc_file_name).parent().unwrap()).unwrap();
        doc_file_name
    }
}

/// Find the file for the module under the parent directory.
///
/// The module's source code file in this case can be ``parent_dir/modname.rs``
/// or ``parent_dir/modname/mod.rs``.
///
/// Args:
///     :parent_dir: The directory under which to find the module's file.
///     :module_directive: The directive for the module.
///
/// Returns:
///     The path for the module's source code file.
///
/// Panics:
///     If neither ``parent_dir/modname.rs`` nor ``parent_dir/modname/mod.rs``
///     exist.
fn find_mod_file_under(parent_dir: &Path, module_directive: &ModuleDirective) -> PathBuf {
    // Check modname.rs under the same directory as crate.
    let mut mod_file = parent_dir.join(format!("{}.rs", &module_directive.ident));

    // Check modname/mod.rs under the crate's directory
    if !mod_file.is_file() {
        mod_file = parent_dir.join(&module_directive.ident).join("mod.rs");
    }

    // Panic if still not found.
    if !mod_file.is_file() {
        panic!(
            "Could not locate file for module {}",
            &module_directive.ident
        );
    }
    mod_file
}

/// Find the file for the module from provided parent path.
///
/// If the parent path is a directory, this calls
/// :rust:fn:`~sphinx-rustdocgen::find_mod_file_under` to locate the module's
/// file. If the parent path is a file name, it is assumed to be the path to
/// the module's parent module's file. If the file name is ``mod.rs``, the
/// module's file is searched under the same directory. Otherwise, it is
/// searched under the directory with the same name as the parent module.
///
/// Args:
///     :parent_path: The path to the file for the parent module of the current
///         module.
///     :module_directive: The directive for the module.
///
/// Returns:
///     The path for the module's source code file.
///
/// Panics:
///     If the module's file cannot be determined.
fn find_mod_file(parent_path: &Path, module_directive: &ModuleDirective) -> PathBuf {
    if parent_path.is_dir() {
        find_mod_file_under(parent_path, module_directive)
    }
    else {
        // Parent is a file. Remove the extension from it.
        if parent_path.ends_with("mod.rs") {
            find_mod_file_under(parent_path.parent().unwrap(), module_directive)
        }
        else {
            find_mod_file_under(
                &parent_path
                    .parent()
                    .unwrap()
                    .join(parent_path.file_stem().unwrap()),
                module_directive,
            )
        }
    }
}

/// The different types of files that can be encountered.
/// For each file, the name of the item within it is captured.
enum FileType {
    /// A binary executable's source file.
    Bin(String),
    /// The crate's library file.
    Lib(String),
    /// All other module files.
    Mod(String),
}

/// Macro to push the module files to the files vec for processing
///
/// Args:
///     :files: The files list to push the files to.
///     :parent: The parent path of the module or crate's file.
///     :directive: The directive for the module or crate.
macro_rules! push_module_files {
    ($files:expr, $parent:expr, $directive:expr) => {
        for directive in &$directive.items {
            if let Directive::Module(m) = directive {
                if m.items.is_empty() {
                    // Push the file to the vec
                    $files.push((
                        find_mod_file($parent, &m),
                        FileType::Mod(m.name.clone()),
                        Some(m.visibility.clone()),
                    ));
                }
            }
        }
    };
}

/// Traverse the crate and extract the docstrings for the items.
///
/// Args:
///     :config: The configuration for the crate.
pub fn traverse_crate(mut config: Configuration) {
    config.canonicalize();
    log::debug!(
        "Extracting docs for crate {} from {}",
        &config.crate_name,
        config.src_dir.to_str().unwrap()
    );
    log::debug!(
        "Generated docs will be stored in {}",
        config.doc_dir.to_str().unwrap()
    );

    // Vec of files that we need to process
    let mut files = vec![];

    // Add the main file if it exists.
    // TODO: Make configurable
    let main = config.src_dir.join("main.rs");
    if main.is_file() {
        files.push((main, FileType::Bin(config.crate_name.clone()), None));
    }

    // Check src/bin for other executables
    let bin_dir = config.src_dir.join("bin");
    if bin_dir.is_dir() {
        for path in bin_dir.read_dir().unwrap() {
            let path = path.unwrap().path();
            if path.is_dir() {
                let executable = path
                    .components()
                    .last()
                    .unwrap()
                    .as_os_str()
                    .to_str()
                    .unwrap()
                    .to_string();
                files.push((path.join("main.rs"), FileType::Bin(executable), None));
            }
            else if path.extension() == Some("rs".as_ref()) {
                let executable = path.file_stem().unwrap().to_str().unwrap().to_string();
                files.push((path, FileType::Bin(executable), None));
            }
        }
    }

    // Add the lib file if it exists.
    // TODO: Make configurable
    let lib = config.src_dir.join("lib.rs");
    if lib.is_file() {
        files.push((lib, FileType::Lib(config.crate_name.to_string()), None));
    }

    while let Some((path, file, vis)) = files.pop() {
        log::debug!("Processing file {}", path.to_str().unwrap());

        let ast = syn::parse_file(&read_to_string(&path).unwrap()).unwrap();
        let text = match file {
            FileType::Bin(exe_name) => {
                let exe_directive = ExecutableDirective::new(&exe_name, &ast);

                push_module_files!(files, path.parent().unwrap(), exe_directive);

                let mut text = config.format.make_title(&exe_name);
                text.extend(
                    config
                        .format
                        .format_directive(Directive::Executable(exe_directive), &config.visibility),
                );
                text
            }
            FileType::Lib(crate_name) => {
                let crate_directive = CrateDirective::new(&crate_name, &ast);

                push_module_files!(files, path.parent().unwrap(), crate_directive);

                let mut text = config.format.make_title(&format!(
                    "Crate {}",
                    config.format.make_inline_code(&crate_name)
                ));
                text.extend(
                    config
                        .format
                        .format_directive(Directive::Crate(crate_directive), &config.visibility),
                );
                text
            }
            FileType::Mod(module) => {
                let module_directive = ModuleDirective::new(&module, &ast, vis.unwrap());

                push_module_files!(files, &path, module_directive);

                let mut text = config.format.make_title(
                    &config
                        .format
                        .make_inline_code(&format!("mod {}", module_directive.ident)),
                );
                text.extend(
                    config
                        .format
                        .format_directive(Directive::Module(module_directive), &config.visibility),
                );
                text
            }
        };

        let doc_file_name = config.get_doc_file_name(&path);
        let doc_file = Path::new(&doc_file_name);

        // If file doesn't exist or the module file has been modified since the
        // last modification of the doc file, create/truncate it and rebuild the
        // documentation.
        if config.force
            || !doc_file.exists()
            || doc_file.metadata().unwrap().modified().unwrap()
                < path.metadata().unwrap().modified().unwrap()
        {
            let mut doc_file = File::create(doc_file).unwrap();
            log::debug!("Writing docs to file {doc_file_name}");
            for line in text {
                writeln!(&mut doc_file, "{line}").unwrap();
            }
        }
        else {
            log::debug!("Docs are up to date")
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_foo() {
        println!("{}", bool::default())
    }

    #[test]
    fn test_self() {
        // Test just extracts the documents for the current crate. This avoids
        // creating unnecessary test files when the source code itself can be
        // used.
        traverse_crate(Configuration {
            crate_name: String::from("sphinx-rustdocgen"),
            src_dir: Path::new(".").to_owned(),
            doc_dir: Path::new("../docs/crates").to_owned(),
            format: Format::Rst,
            visibility: DirectiveVisibility::Pvt,
            force: true,
        })
    }

    #[test]
    fn test_markdown() {
        traverse_crate(Configuration {
            crate_name: String::from("test_crate"),
            src_dir: Path::new("../tests/test_crate").to_owned(),
            doc_dir: Path::new("../tests/test_crate/docs/crates").to_owned(),
            format: Format::Md,
            visibility: DirectiveVisibility::Pvt,
            force: true,
        })
    }
}
