//! Implementation of the ``rust:trait`` directive

use quote::quote;
use syn::{ItemTrait, ItemTraitAlias, Visibility};

use crate::directives::{
    extract_doc_from_attrs,
    Directive,
    DirectiveOption,
    DirectiveVisibility,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};
use crate::{check_visibility, visibility_to_inherit};

#[derive(Clone, Debug)]
pub(crate) struct TraitDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
    pub(crate) items: Vec<Directive>,
}

impl TraitDirective {
    const DIRECTIVE_NAME: &'static str = "trait";

    // noinspection DuplicatedCode
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemTrait,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let name = format!("{}::{}", parent_path, item.ident);

        let ident = &item.ident;
        let (_, tg, wc) = item.generics.split_for_impl();
        let unsafety = &item.unsafety;
        let options = vec![
            DirectiveOption::Index(IndexEntryType::WithSubEntries),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &item.vis,
                inherited_visibility,
            )),
            DirectiveOption::Sig(quote! {#unsafety trait #ident #tg #wc}.to_string()),
        ];

        let items = Directive::from_trait_items(
            &name,
            item.items.iter(),
            &visibility_to_inherit!(item.vis, *inherited_visibility),
        );

        Directive::Trait(TraitDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            items,
        })
    }

    // noinspection DuplicatedCode
    pub(crate) fn from_alias(
        parent_path: &str,
        alias: &ItemTraitAlias,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let name = format!("{}::{}", parent_path, alias.ident);

        let ident = &alias.ident;
        let (_, tg, wc) = alias.generics.split_for_impl();
        let options = vec![
            DirectiveOption::Index(IndexEntryType::Normal),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &alias.vis,
                inherited_visibility,
            )),
            DirectiveOption::Sig(quote! {trait #ident #tg #wc}.to_string()),
        ];

        Directive::Trait(TraitDirective {
            name,
            options,
            content: extract_doc_from_attrs(&alias.attrs),
            items: Vec::new(),
        })
    }
}

impl RstDirective for TraitDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_content_indent(level);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        for item in self.items {
            text.extend(item.get_rst_text(level + 1, max_visibility));
        }

        text
    }
}

impl MdDirective for TraitDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text =
            Self::make_md_header(Self::DIRECTIVE_NAME, &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        for item in self.items {
            text.extend(item.get_md_text(fence_size - 1, max_visibility));
        }

        text.push(fence);
        text
    }

    fn fence_size(&self) -> usize {
        Self::calc_fence_size(&self.items)
    }
}
