//! Implementation of the ``rust:enum`` directive

use quote::quote;
use syn::{ItemEnum, Visibility};

use crate::directives::struct_directive::StructDirective;
use crate::directives::{
    extract_doc_from_attrs,
    Directive,
    DirectiveOption,
    DirectiveVisibility,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};
use crate::{check_visibility, visibility_to_inherit};

/// Struct to hold data for documenting an enum
#[derive(Clone, Debug)]
pub(crate) struct EnumDirective {
    /// The full Rust path of the enum, used as the name of the directive.
    pub(crate) name: String,
    /// The directive options to use.
    pub(crate) options: Vec<DirectiveOption>,
    /// The docstring for the enum.
    pub(crate) content: Vec<String>,
    /// The variants within the enum.
    pub(crate) variants: Vec<StructDirective>,
}

impl EnumDirective {
    const DIRECTIVE_NAME: &'static str = "enum";

    /// Create a new ``Directive::Enum`` from a ``syn::ItemEnum``
    ///
    /// Args:
    ///     :parent_path: The full path of the module the enum is in.
    ///     :item: The ``syn::ItemEnum`` to parse.
    ///
    /// Returns:
    ///     A new ``Directive::Enum``, which contains the parsed
    ///     ``EnumDirective`` in it.
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemEnum,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let name = format!("{}::{}", parent_path, item.ident);
        let variants = item
            .variants
            .iter()
            .map(|v| {
                StructDirective::from_variant(
                    &name,
                    v,
                    &visibility_to_inherit!(item.vis, *inherited_visibility),
                )
            })
            .collect();

        let (_, ty, wc) = item.generics.split_for_impl();
        let ident = &item.ident;
        let signature = quote! {enum #ident #ty #wc}.to_string();

        let options = vec![
            DirectiveOption::Index(IndexEntryType::WithSubEntries),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &item.vis,
                inherited_visibility,
            )),
            DirectiveOption::Sig(signature),
        ];

        Directive::Enum(EnumDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            variants,
        })
    }
}

impl RstDirective for EnumDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_indent(level + 1);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        for variant in self.variants {
            text.extend(variant.get_rst_text(level + 1, max_visibility));
        }

        text
    }
}

impl MdDirective for EnumDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text =
            Self::make_md_header(Self::DIRECTIVE_NAME, &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        for variant in self.variants {
            text.extend(variant.get_md_text(fence_size - 1, max_visibility));
        }

        text.push(fence);
        text
    }

    fn fence_size(&self) -> usize {
        match self.variants.iter().map(StructDirective::fence_size).max() {
            Some(s) => s + 1,
            None => 3,
        }
    }
}
