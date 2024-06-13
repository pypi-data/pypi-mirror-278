//! Implementation of the pseudo-directive for foreign modules.
//!
//! The directive is not really published to the documentation, but used only
//! for organizing the content of the items within it.

use syn::{ItemForeignMod, Visibility};

use crate::directives::{Directive, MdDirective, RstDirective};
use crate::DirectiveVisibility;

#[derive(Clone, Debug)]
pub(crate) struct ForeignModDirective {
    pub(crate) items: Vec<Directive>,
}

impl ForeignModDirective {
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemForeignMod,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        Directive::ForeignMod(ForeignModDirective {
            items: Directive::from_extern_items(
                parent_path,
                item.items.iter(),
                inherited_visibility,
            ),
        })
    }
}

impl RstDirective for ForeignModDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        self.items
            .into_iter()
            .flat_map(|item| item.get_rst_text(level, max_visibility))
            .collect()
    }
}

impl MdDirective for ForeignModDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        self.items
            .into_iter()
            .flat_map(|item| item.get_md_text(fence_size, max_visibility))
            .collect()
    }

    fn fence_size(&self) -> usize {
        self.items
            .iter()
            .map(Directive::fence_size)
            .max()
            .unwrap_or(3)
    }
}
