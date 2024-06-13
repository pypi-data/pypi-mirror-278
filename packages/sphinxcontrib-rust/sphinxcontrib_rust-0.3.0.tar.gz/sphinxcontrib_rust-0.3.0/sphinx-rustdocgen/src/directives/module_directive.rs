//! Implementation of the ``rust:module`` directive

use std::cmp::max;

use syn::{File, ItemMod, Meta, Visibility};

use crate::directives::{
    extract_doc_from_attrs,
    order_items,
    Directive,
    DirectiveOption,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};
use crate::DirectiveVisibility;

/// Struct to hold data for a module's documentation.
#[derive(Clone, Debug)]
pub(crate) struct ModuleDirective {
    /// The full path to the module.
    pub(crate) name: String,
    /// The options for the module directive.
    pub(crate) options: Vec<DirectiveOption>,
    /// The docstring for the module.
    pub(crate) content: Vec<String>,
    /// The items defined within the module.
    pub(crate) items: Vec<Directive>,
    /// The identifier of the module (i.e. the final portion of name).
    pub(crate) ident: String,
    /// The visibility of the module.
    pub(crate) visibility: Visibility,
}

#[inline]
fn has_test_token(tokens: &str) -> bool {
    tokens == "test"
        || tokens.matches(", test").any(|_| true)
        || tokens.matches("test, ").any(|_| true)
}

/// Determines if the module is a test module or not.
fn is_test_module(item_mod: &ItemMod) -> bool {
    // XXX: Find a better way to do this.
    for attr in &item_mod.attrs {
        if let Meta::List(meta) = &attr.meta {
            for segment in &meta.path.segments {
                if segment.ident == "cfg" && has_test_token(&meta.tokens.to_string()) {
                    return true;
                }
            }
        }
    }
    false
}

impl ModuleDirective {
    const DIRECTIVE_NAME: &'static str = "module";

    /// Create a new ``ModuleDirective`` from name, AST and visibility.
    ///
    /// Args:
    ///     :module_name: The full path to the module, starting with the crate
    ///         name.
    ///     :ast: The ``syn::File`` reference from parsing the module's file.
    ///     :visibility: The visibility of the module. This is typically
    ///         determined when the parent module is parsed.
    pub(crate) fn new(module_name: &str, ast: &File, visibility: Visibility) -> ModuleDirective {
        ModuleDirective {
            name: module_name.to_string(),
            options: vec![DirectiveOption::Index(IndexEntryType::Normal)],
            content: extract_doc_from_attrs(&ast.attrs),
            ident: module_name.split("::").last().unwrap().to_string(),
            items: Directive::from_items(module_name, ast.items.iter(), &Some(&visibility)),
            visibility,
        }
    }

    /// Create a :rust:struct:`sphinx-rustdocgen::directives::Directive::Module`
    /// from the item, if the module is not a test module.
    ///
    /// ``ItemMod`` is both a mod declaration and mod definition.
    /// When it is only a declaration like ``pub mod foo;``, there are no items
    /// but the visibility is known. If it is an inline definition, both items
    /// and visibility are available. If the returned value has an empty
    /// ``items`` vec, only the declaration was provided, and the module
    /// definition is in a separate file. In such cases, the module content
    /// should be updated later using the
    /// :rust:fn:`sphinx-rustdocgen::directives::module_directive::ModuleDirective::update_items`.
    ///
    /// Args:
    ///     :parent_path: The path of the module's parent module or the crate
    ///         name.
    ///     :item: The ``ItemMod`` parsed out by ``syn``.
    ///
    /// Returns:
    ///     A ``Some`` value if the module is not a test module, otherwise
    ///     ``None``.
    pub(crate) fn from_item(parent_path: &str, item: &ItemMod) -> Option<Directive> {
        if is_test_module(item) {
            return None;
        }

        let name = format!("{}::{}", parent_path, item.ident);
        let items = if let Some((_, items)) = &item.content {
            Directive::from_items(&name, items.iter(), &Some(&item.vis))
        }
        else {
            Vec::new()
        };
        Some(Directive::Module(ModuleDirective {
            name,
            options: vec![DirectiveOption::Index(IndexEntryType::Normal)],
            content: extract_doc_from_attrs(&item.attrs),
            ident: item.ident.to_string(),
            items,
            visibility: item.vis.clone(),
        }))
    }
}

impl RstDirective for ModuleDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        // Do not filter for visibility here. Modules are always documented.
        let content_indent = Self::make_content_indent(level + 1);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        let (toc_tree_modules, ordered_items) = order_items(self.items);

        text.extend(Self::make_rst_toctree(
            &content_indent,
            "Modules",
            Some(1),
            toc_tree_modules
                .iter()
                .map(|m| format!("{}/{}", &self.ident, m.ident)),
        ));

        for (name, item) in ordered_items {
            text.extend(Self::make_rst_section(name, level, item, max_visibility));
        }

        text
    }
}

impl MdDirective for ModuleDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        // Do not filter for visibility here. Modules are always documented.
        let fence = Self::make_fence(max(fence_size, 4));

        let mut text =
            Self::make_md_header(Self::DIRECTIVE_NAME, &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        let (toc_tree_modules, ordered_items) = order_items(self.items);

        text.extend(Self::make_md_toctree(
            3,
            "Modules",
            Some(1),
            toc_tree_modules
                .iter()
                .map(|m| format!("{}/{}", &self.ident, m.ident)),
        ));

        for (name, item) in ordered_items {
            text.extend(Self::make_md_section(
                name,
                fence_size,
                item,
                max_visibility,
            ));
        }
        text.push(fence);

        text
    }

    fn fence_size(&self) -> usize {
        Self::calc_fence_size(&self.items)
    }
}
