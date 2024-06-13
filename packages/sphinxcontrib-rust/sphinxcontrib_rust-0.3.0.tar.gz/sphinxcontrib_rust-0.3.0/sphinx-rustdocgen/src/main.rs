//! sphinx-rustdocgen is an executable to extract doc comments from Rust
//! crates. It is tightly coupled with the sphinxcontrib-rust extension and is
//! used by it during the Sphinx build process.
//!
//! Usage:
//!
//! .. code-block::
//!
//!    sphinx-rustdocgen <JSON config>
//!
//! See :rust:struct:`sphinx-rustdocgen::Configuration` for the configuration
//! schema.

use std::env;

use sphinx_rustdocgen::traverse_crate;

static USAGE: &str = "sphinx-rustdocgen <JSON configuration>";

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Invalid number of arguments: {}\n\n{USAGE}", args.len());
    }

    traverse_crate(serde_json::from_str(&args[1]).unwrap())
}
