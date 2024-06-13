//! Implementation of the ``rust:impl`` directive

use quote::quote;
use syn::{ItemImpl, Visibility};

use crate::directives::{
    extract_doc_from_attrs,
    Directive,
    DirectiveOption,
    DirectiveVisibility,
    IndexEntryType,
};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

#[derive(Clone, Debug)]
pub(crate) struct ImplDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
    pub(crate) items: Vec<Directive>,
}

impl ImplDirective {
    const DIRECTIVE_NAME: &'static str = "impl";

    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemImpl,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let self_ty = &item.self_ty;
        let mut name = format!("{parent_path}::{}", quote! {#self_ty},);

        let (ig, tg, wc) = item.generics.split_for_impl();
        let trait_ = item.trait_.as_ref().map(|(bang, path, _)| {
            let mut trait_name = String::new();
            if bang.is_some() {
                trait_name += "!";
            }
            trait_name += &*path.segments.last().unwrap().ident.to_string();
            name += "::";
            name += &*trait_name;

            quote! {#path for}
        });
        let unsafety = item.unsafety.as_ref();
        let sig = quote! {#unsafety impl #ig #trait_ #self_ty #tg #wc};

        let options = vec![
            DirectiveOption::Index(IndexEntryType::None),
            DirectiveOption::Vis(DirectiveVisibility::Pub),
            DirectiveOption::Sig(sig.to_string()),
            DirectiveOption::Toc(format!(
                "impl {}{}",
                trait_
                    .as_ref()
                    .map(|t| quote! {#t}.to_string() + " ")
                    .unwrap_or_default(),
                quote! {#self_ty}
            )),
        ];

        let items = Directive::from_impl_items(&name, item.items.iter(), inherited_visibility);
        Directive::Impl(ImplDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            items,
        })
    }
}

impl RstDirective for ImplDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        let content_indent = Self::make_content_indent(level + 1);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        for item in self.items {
            text.extend(item.get_rst_text(level + 1, max_visibility))
        }

        text
    }
}

impl MdDirective for ImplDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
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
