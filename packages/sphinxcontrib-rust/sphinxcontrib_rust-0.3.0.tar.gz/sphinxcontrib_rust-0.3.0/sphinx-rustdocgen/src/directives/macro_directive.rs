//! Implementation of the ``rust:macro`` directive

use syn::ItemMacro;

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
pub(crate) struct MacroDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
}

impl MacroDirective {
    const DIRECTIVE_NAME: &'static str = "macro";

    pub(crate) fn from_item(parent_path: &str, item: &ItemMacro) -> Option<Directive> {
        let ident = item.ident.as_ref()?;
        let name = format!("{}::{}", parent_path, ident);

        let is_exported = item
            .attrs
            .iter()
            .any(|a| !a.path().segments.is_empty() && a.path().segments[0].ident == "macro_export");

        let vis = if is_exported {
            DirectiveVisibility::Pub
        }
        else {
            DirectiveVisibility::Pvt
        };

        let options = vec![
            DirectiveOption::Index(IndexEntryType::Normal),
            DirectiveOption::Vis(vis),
        ];

        Some(Directive::Macro(MacroDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
        }))
    }
}

impl RstDirective for MacroDirective {
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

impl MdDirective for MacroDirective {
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
