//! Implementation of the ``rust:function`` directive

use quote::quote;
use syn::{ForeignItemFn, ImplItemFn, ItemFn, TraitItemFn, Visibility};

use crate::check_visibility;
use crate::directives::{
    extract_doc_from_attrs,
    Directive,
    DirectiveOption,
    DirectiveVisibility,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

/// Struct to hold data for documenting a function.
#[derive(Clone, Debug)]
pub(crate) struct FunctionDirective {
    /// The full Rust path of the function.
    pub(crate) name: String,
    /// The directive options to use.
    pub(crate) options: Vec<DirectiveOption>,
    /// The docstring for the function.
    pub(crate) content: Vec<String>,
}

/// DRY macro to parse the different item types.
macro_rules! func_from_item {
    ($parent_path:expr, $item:expr, $vis:expr, $inherited:expr) => {{
        let sig = &$item.sig;
        let options = vec![
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(&$vis, $inherited)),
            DirectiveOption::Sig(quote! {#sig}.to_string()),
        ];

        FunctionDirective {
            name: format!("{}::{}", $parent_path, $item.sig.ident),
            options,
            content: extract_doc_from_attrs(&$item.attrs),
        }
    }};
}

impl FunctionDirective {
    const DIRECTIVE_NAME: &'static str = "function";

    /// Create a new ``Directive::Function`` from a ``syn::ItemFn``.
    ///
    /// Args:
    ///     :parent_path: The full path of the module the function is in.
    ///     :item: The ``syn::ItemFn`` reference to parse.
    ///
    /// Returns:
    ///     A new ``Directive::Function`` value, which contains the parsed
    ///     ``FunctionDirective`` in it.
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemFn,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = func_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::Normal));
        Directive::Function(directive)
    }

    /// Create a new ``Directive::Function`` from a ``syn::ImplItemFn``.
    ///
    /// Args:
    ///     :parent_path: The full path of the impl block the function is in.
    ///     :item: The ``syn::ImplItemFn`` reference to parse.
    ///
    /// Returns:
    ///     A new ``Directive::Function`` value, which contains the parsed
    ///     ``FunctionDirective`` in it.
    pub(crate) fn from_impl_item(
        parent_path: &str,
        item: &ImplItemFn,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = func_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::None));
        Directive::Function(directive)
    }

    /// Create a new ``Directive::Function`` from a ``syn::TraitItemFn``.
    ///
    /// Args:
    ///     :parent_path: The full path of the trait the function is in.
    ///     :item: The ``syn::TraitItemFn`` reference to parse.
    ///
    /// Returns:
    ///     A new ``Directive::Function`` value, which contains the parsed
    ///     ``FunctionDirective`` in it.
    pub(crate) fn from_trait_item(
        parent_path: &str,
        item: &TraitItemFn,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = func_from_item!(
            parent_path,
            item,
            &Visibility::Inherited,
            inherited_visibility
        );
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::SubEntry));
        Directive::Function(directive)
    }

    pub(crate) fn from_extern(
        parent_path: &str,
        item: &ForeignItemFn,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = func_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::Normal));
        Directive::Function(directive)
    }
}

impl RstDirective for FunctionDirective {
    // noinspection DuplicatedCode
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_content_indent(level);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        text
    }
}

impl MdDirective for FunctionDirective {
    // noinspection DuplicatedCode
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text =
            Self::make_md_header(Self::DIRECTIVE_NAME, &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());
        text.push(fence);

        text
    }
}
