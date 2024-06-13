//! Implementation of the ``rust:struct`` directive

use quote::quote;
use syn::{Fields, ItemStruct, ItemUnion, Variant, Visibility};

use crate::directives::variable_directive::VariableDirective;
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
pub(crate) struct StructDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
    pub(crate) fields: Vec<VariableDirective>,
}

macro_rules! make_sig {
    ($item:expr) => {{
        let ident = &$item.ident;
        let fields = if matches!(&$item.fields, Fields::Unnamed(_)) {
            format!(
                "({})",
                $item
                    .fields
                    .iter()
                    .map(|f| {
                        let ty = &f.ty;
                        quote! {#ty}.to_string()
                    })
                    .collect::<Vec<String>>()
                    .join(", ")
            )
        }
        else {
            String::new()
        };
        let mut sig = quote! {#ident}.to_string();
        sig += &*fields;
        sig
    }};
}

impl StructDirective {
    const DIRECTIVE_NAME: &'static str = "struct";

    pub(crate) fn from_variant(
        parent_path: &str,
        variant: &Variant,
        inherited_visibility: &Option<&Visibility>,
    ) -> StructDirective {
        let name = format!("{}::{}", parent_path, variant.ident);

        let options = vec![
            DirectiveOption::Index(IndexEntryType::SubEntry),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &Visibility::Inherited,
                inherited_visibility,
            )),
            DirectiveOption::Sig(make_sig!(variant)),
            DirectiveOption::Toc(format!("{}", &variant.ident)),
        ];

        let fields = VariableDirective::from_fields(
            &name,
            &variant.fields,
            inherited_visibility,
            IndexEntryType::None,
        );

        StructDirective {
            name,
            options,
            content: extract_doc_from_attrs(&variant.attrs),
            fields,
        }
    }

    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemStruct,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let name = format!("{}::{}", parent_path, item.ident);

        let options = vec![
            DirectiveOption::Index(IndexEntryType::WithSubEntries),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &item.vis,
                inherited_visibility,
            )),
            DirectiveOption::Sig(make_sig!(item)),
            DirectiveOption::Toc(format!("struct {}", &item.ident)),
        ];

        let fields = VariableDirective::from_fields(
            &name,
            &item.fields,
            &visibility_to_inherit!(item.vis, *inherited_visibility),
            IndexEntryType::SubEntry,
        );

        Directive::Struct(StructDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            fields,
        })
    }

    pub(crate) fn from_union(
        parent_path: &str,
        item: &ItemUnion,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let ident = &item.ident;
        let (_, tg, wc) = item.generics.split_for_impl();

        let name = format!("{parent_path}::{ident}");
        let signature = quote! {union #ident #tg #wc}.to_string();

        let options = vec![
            DirectiveOption::Index(IndexEntryType::WithSubEntries),
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                &item.vis,
                inherited_visibility,
            )),
            DirectiveOption::Sig(signature),
            DirectiveOption::Toc(format!("union {}", &item.ident)),
        ];

        let fields = VariableDirective::from_fields(
            &name,
            &Fields::Named(item.fields.clone()),
            &visibility_to_inherit!(item.vis, *inherited_visibility),
            IndexEntryType::SubEntry,
        );

        Directive::Struct(StructDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            fields,
        })
    }
}

impl RstDirective for StructDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_content_indent(level);

        let mut text =
            Self::make_rst_header(Self::DIRECTIVE_NAME, &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        for field in self.fields {
            text.extend(field.get_rst_text(level + 1, max_visibility));
        }

        text
    }
}

impl MdDirective for StructDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text =
            Self::make_md_header(Self::DIRECTIVE_NAME, &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        for field in self.fields {
            text.extend(field.get_md_text(fence_size - 1, max_visibility));
        }

        text.push(fence);
        text
    }

    // noinspection DuplicatedCode
    fn fence_size(&self) -> usize {
        match self.fields.iter().map(VariableDirective::fence_size).max() {
            Some(s) => s + 1,
            None => 3,
        }
    }
}
