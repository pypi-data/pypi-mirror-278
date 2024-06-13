//! Implementation of the ``rust:type`` directive

use quote::quote;
use syn::{ForeignItemType, ImplItemType, ItemType, TraitItemType, Visibility};

use crate::check_visibility;
use crate::directives::{
    extract_doc_from_attrs,
    Directive,
    DirectiveOption,
    DirectiveVisibility,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

#[derive(Clone, Debug)]
pub(crate) struct TypeDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
}

macro_rules! type_from_item {
    ($parent_path:expr, $item:expr, $vis:expr, $inherited:expr) => {{
        let name = format!("{}::{}", $parent_path, &$item.ident);

        let ident = &$item.ident;
        let (_, ty, wc) = $item.generics.split_for_impl();
        let options = vec![
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(&$vis, $inherited)),
            DirectiveOption::Sig(quote! {type #ident #ty #wc}.to_string()),
        ];

        TypeDirective {
            name,
            options,
            content: extract_doc_from_attrs(&$item.attrs),
        }
    }};
}

impl TypeDirective {
    const DIRECTIVE_NAME: &'static str = "type";

    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = type_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::Normal));
        Directive::Type(directive)
    }

    pub(crate) fn from_impl_item(
        parent_path: &str,
        item: &ImplItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = type_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::None));
        Directive::Type(directive)
    }

    pub(crate) fn from_trait_item(
        parent_path: &str,
        item: &TraitItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = type_from_item!(
            parent_path,
            item,
            Visibility::Inherited,
            inherited_visibility
        );
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::SubEntry));
        Directive::Type(directive)
    }

    pub(crate) fn from_extern(
        parent_path: &str,
        item: &ForeignItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut directive = type_from_item!(parent_path, item, item.vis, inherited_visibility);
        directive
            .options
            .push(DirectiveOption::Index(IndexEntryType::Normal));
        Directive::Type(directive)
    }
}

impl RstDirective for TypeDirective {
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

impl MdDirective for TypeDirective {
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
