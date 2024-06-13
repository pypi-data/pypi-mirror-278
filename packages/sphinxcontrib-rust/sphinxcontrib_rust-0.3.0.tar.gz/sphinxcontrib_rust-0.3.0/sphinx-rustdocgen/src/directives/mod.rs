//! Module for the various Sphinx directives for the Rust domain.
//!
//! The module primarily provides the
//! :rust:enum:`~sphinx-rustdocgen::directives::Directive`, which implements the
//! various directives using directive specific structs. The enum and all
//! directive specific structs implement both
//! :rust:trait:`~sphinx-rustdocgen::formats::RstContent` and
//! :rust:trait:`~sphinx-rustdocgen::formats::MdContent` traits.
//! It also provides the
//! :rust:enum:`~sphinx-rustdocgen::directives::DirectiveOption` enum, which
//! implements the various options of the directive.
//!
//! The output of the directives is parsed by the
//! :py:class:`sphinxcontrib_rust.directives.RustDirective` within the Python
//! extension.

mod crate_directive;
mod enum_directive;
mod executable_directive;
mod foreign_mod;
mod function_directive;
mod impl_directive;
mod macro_directive;
mod module_directive;
mod struct_directive;
mod trait_directive;
mod type_directive;
mod variable_directive;

use std::fmt::{Display, Formatter};
use std::str::FromStr;

use quote::ToTokens;
use serde::Deserialize;
use syn::{Attribute, Expr, ForeignItem, ImplItem, Item, Lit, TraitItem, Visibility};

pub(crate) use crate::directives::crate_directive::CrateDirective;
pub(crate) use crate::directives::enum_directive::EnumDirective;
pub(crate) use crate::directives::executable_directive::ExecutableDirective;
pub(crate) use crate::directives::foreign_mod::ForeignModDirective;
pub(crate) use crate::directives::function_directive::FunctionDirective;
pub(crate) use crate::directives::impl_directive::ImplDirective;
pub(crate) use crate::directives::macro_directive::MacroDirective;
pub(crate) use crate::directives::module_directive::ModuleDirective;
pub(crate) use crate::directives::struct_directive::StructDirective;
pub(crate) use crate::directives::trait_directive::TraitDirective;
pub(crate) use crate::directives::type_directive::TypeDirective;
pub(crate) use crate::directives::variable_directive::VariableDirective;
pub(crate) use crate::formats::{MdDirective, RstDirective};
use crate::formats::{MdOption, RstOption};

/// The Sphinx directives that are implemented by the Rust domain.
#[derive(Clone, Debug)]
pub(crate) enum Directive {
    Crate(CrateDirective),
    Enum(EnumDirective),
    Executable(ExecutableDirective),
    ForeignMod(ForeignModDirective),
    Function(FunctionDirective),
    Impl(ImplDirective),
    Macro(MacroDirective),
    Module(ModuleDirective),
    Struct(StructDirective),
    Trait(TraitDirective),
    Type(TypeDirective),
    Variable(VariableDirective),
}

impl Directive {
    fn name(&self) -> &str {
        match self {
            Directive::Crate(c) => &c.name,
            Directive::Enum(e) => &e.name,
            Directive::Executable(e) => &e.name,
            Directive::ForeignMod(_) => "",
            Directive::Function(f) => &f.name,
            Directive::Impl(i) => &i.name,
            Directive::Macro(m) => &m.name,
            Directive::Module(m) => &m.name,
            Directive::Struct(s) => &s.name,
            Directive::Trait(t) => &t.name,
            Directive::Type(t) => &t.name,
            Directive::Variable(v) => &v.name,
        }
    }

    /// Create the appropriate directive from the provided ``syn::Item``
    ///
    /// Args:
    ///     :parent_path: The parent path of the item.
    ///     :item: The item to parse into a directive.
    ///
    /// Returns:
    ///     An option a :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variant.
    fn from_item(
        parent_path: &str,
        item: &Item,
        inherited_visibility: &Option<&Visibility>,
    ) -> Option<Directive> {
        match item {
            Item::Const(c) => Some(VariableDirective::from_const(
                parent_path,
                c,
                inherited_visibility,
            )),
            Item::Enum(e) => Some(EnumDirective::from_item(
                parent_path,
                e,
                inherited_visibility,
            )),
            Item::ExternCrate(_) => None,
            Item::Fn(f) => Some(FunctionDirective::from_item(
                parent_path,
                f,
                inherited_visibility,
            )),
            Item::ForeignMod(f) => Some(ForeignModDirective::from_item(
                parent_path,
                f,
                inherited_visibility,
            )),
            Item::Impl(i) => Some(ImplDirective::from_item(
                parent_path,
                i,
                inherited_visibility,
            )),
            Item::Macro(m) => MacroDirective::from_item(parent_path, m),
            Item::Mod(m) => ModuleDirective::from_item(parent_path, m),
            Item::Static(s) => Some(VariableDirective::from_static(
                parent_path,
                s,
                inherited_visibility,
            )),
            Item::Struct(s) => Some(StructDirective::from_item(
                parent_path,
                s,
                inherited_visibility,
            )),
            Item::Trait(t) => Some(TraitDirective::from_item(
                parent_path,
                t,
                inherited_visibility,
            )),
            Item::TraitAlias(t) => Some(TraitDirective::from_alias(
                parent_path,
                t,
                inherited_visibility,
            )),
            Item::Type(t) => Some(TypeDirective::from_item(
                parent_path,
                t,
                inherited_visibility,
            )),
            Item::Union(u) => Some(StructDirective::from_union(
                parent_path,
                u,
                inherited_visibility,
            )),
            Item::Use(_) => {
                // TODO: Implement re-exports at some point
                // TODO: Use this to update paths in the references to support
                //   relative referencing.
                None
            }
            Item::Verbatim(_) => None,
            i => panic!("Unexpected item: {:?}", i),
        }
    }

    /// Create the appropriate directives from the provided ``syn::Item``
    /// iterator.
    ///
    /// Args:
    ///     :parent_path: The parent path of the items.
    ///     :items: The items to parse into a directive.
    ///
    /// Returns:
    ///     An vec of :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variants.
    fn from_items<'a, T: Iterator<Item = &'a Item>>(
        parent_path: &str,
        items: T,
        inherited_visibility: &Option<&Visibility>,
    ) -> Vec<Directive> {
        items
            .filter_map(|i| Self::from_item(parent_path, i, inherited_visibility))
            .collect()
    }

    /// Create the appropriate directive from the provided ``syn::ImplItem``
    ///
    /// Args:
    ///     :parent_path: The path of the impl block which defines the item.
    ///     :item: The impl item to parse into a directive.
    ///
    /// Returns:
    ///     An option a :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variant.
    fn from_impl_item(
        parent_path: &str,
        item: &ImplItem,
        inherited_visibility: &Option<&Visibility>,
    ) -> Option<Directive> {
        match item {
            ImplItem::Const(c) => Some(VariableDirective::from_impl_const(
                parent_path,
                c,
                inherited_visibility,
            )),
            ImplItem::Fn(f) => Some(FunctionDirective::from_impl_item(
                parent_path,
                f,
                inherited_visibility,
            )),
            ImplItem::Type(t) => Some(TypeDirective::from_impl_item(
                parent_path,
                t,
                inherited_visibility,
            )),
            ImplItem::Macro(_) | ImplItem::Verbatim(_) => None,
            i => panic!("Unexpected impl item: {:?}", i),
        }
    }

    /// Create the appropriate directives from the provided ``syn::ImplItem``
    /// iterator.
    ///
    /// Args:
    ///     :parent_path: The path of the impl block which defines the items.
    ///     :items: The impl items to parse into a directive.
    ///
    /// Returns:
    ///     An vec of :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variants.
    fn from_impl_items<'a, T: Iterator<Item = &'a ImplItem>>(
        parent_path: &str,
        items: T,
        inherited_visibility: &Option<&Visibility>,
    ) -> Vec<Directive> {
        items
            .filter_map(|i| Self::from_impl_item(parent_path, i, inherited_visibility))
            .collect()
    }

    /// Create the appropriate directive from the provided ``syn::TraitItem``
    ///
    /// Args:
    ///     :parent_path: The path of the trait which defines the items.
    ///     :item: The trait item to parse into a directive.
    ///
    /// Returns:
    ///     An option a :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variant.
    fn from_trait_item(
        parent_path: &str,
        item: &TraitItem,
        inherited_visibility: &Option<&Visibility>,
    ) -> Option<Directive> {
        match item {
            TraitItem::Const(c) => Some(VariableDirective::from_trait_const(
                parent_path,
                c,
                inherited_visibility,
            )),
            TraitItem::Fn(f) => Some(FunctionDirective::from_trait_item(
                parent_path,
                f,
                inherited_visibility,
            )),
            TraitItem::Type(t) => Some(TypeDirective::from_trait_item(
                parent_path,
                t,
                inherited_visibility,
            )),
            TraitItem::Macro(_) | TraitItem::Verbatim(_) => None,
            i => panic!("Unexpected trait item: {:?}", i),
        }
    }

    /// Create the appropriate directives from the provided ``syn::TraitItem``
    /// iterator.
    ///
    /// Args:
    ///     :parent_path: The path of the trait which defines the items.
    ///     :items: The trait items to parse into a directive.
    ///
    /// Returns:
    ///     An vec of :rust:enum:`sphinx-rustdocgen::directives::Directive`
    ///     variants.
    fn from_trait_items<'a, T: Iterator<Item = &'a TraitItem>>(
        parent_path: &str,
        items: T,
        inherited_visibility: &Option<&Visibility>,
    ) -> Vec<Directive> {
        items
            .filter_map(|i| Self::from_trait_item(parent_path, i, inherited_visibility))
            .collect()
    }

    fn from_extern_item(
        parent_path: &str,
        item: &ForeignItem,
        inherited_visibility: &Option<&Visibility>,
    ) -> Option<Directive> {
        match item {
            ForeignItem::Fn(f) => Some(FunctionDirective::from_extern(
                parent_path,
                f,
                inherited_visibility,
            )),
            ForeignItem::Static(s) => Some(VariableDirective::from_extern_static(
                parent_path,
                s,
                inherited_visibility,
            )),
            ForeignItem::Type(t) => Some(TypeDirective::from_extern(
                parent_path,
                t,
                inherited_visibility,
            )),
            _ => None,
        }
    }

    fn from_extern_items<'a, T: Iterator<Item = &'a ForeignItem>>(
        parent_path: &str,
        items: T,
        inherited_visibility: &Option<&Visibility>,
    ) -> Vec<Directive> {
        items
            .filter_map(|i| Self::from_extern_item(parent_path, i, inherited_visibility))
            .collect()
    }
}

impl Display for Directive {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let value = match self {
            Directive::Crate(_) => "crate",
            Directive::Enum(_) => "enum",
            Directive::Executable(_) => "executable",
            Directive::ForeignMod(_) => "",
            Directive::Function(_) => "function",
            Directive::Impl(_) => "impl",
            Directive::Macro(_) => "macro",
            Directive::Module(_) => "module",
            Directive::Struct(_) => "struct",
            Directive::Trait(_) => "trait",
            Directive::Type(_) => "type",
            Directive::Variable(_) => "variable",
        };
        write!(f, "{value}")
    }
}

impl RstDirective for Directive {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        match self {
            Directive::Crate(c) => c.get_rst_text(level, max_visibility),
            Directive::Enum(e) => e.get_rst_text(level, max_visibility),
            Directive::Executable(e) => e.get_rst_text(level, max_visibility),
            Directive::ForeignMod(f) => f.get_rst_text(level, max_visibility),
            Directive::Function(f) => f.get_rst_text(level, max_visibility),
            Directive::Impl(i) => i.get_rst_text(level, max_visibility),
            Directive::Macro(m) => m.get_rst_text(level, max_visibility),
            Directive::Module(m) => m.get_rst_text(level, max_visibility),
            Directive::Struct(s) => s.get_rst_text(level, max_visibility),
            Directive::Trait(t) => t.get_rst_text(level, max_visibility),
            Directive::Type(t) => t.get_rst_text(level, max_visibility),
            Directive::Variable(v) => v.get_rst_text(level, max_visibility),
        }
    }
}

impl MdDirective for Directive {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        match self {
            Directive::Crate(c) => c.get_md_text(fence_size, max_visibility),
            Directive::Enum(e) => e.get_md_text(fence_size, max_visibility),
            Directive::Executable(e) => e.get_md_text(fence_size, max_visibility),
            Directive::ForeignMod(f) => f.get_md_text(fence_size, max_visibility),
            Directive::Function(f) => f.get_md_text(fence_size, max_visibility),
            Directive::Impl(i) => i.get_md_text(fence_size, max_visibility),
            Directive::Macro(m) => m.get_md_text(fence_size, max_visibility),
            Directive::Module(m) => m.get_md_text(fence_size, max_visibility),
            Directive::Struct(s) => s.get_md_text(fence_size, max_visibility),
            Directive::Trait(t) => t.get_md_text(fence_size, max_visibility),
            Directive::Type(t) => t.get_md_text(fence_size, max_visibility),
            Directive::Variable(v) => v.get_md_text(fence_size, max_visibility),
        }
    }

    fn fence_size(&self) -> usize {
        match self {
            Directive::Crate(c) => c.fence_size(),
            Directive::Enum(e) => e.fence_size(),
            Directive::Executable(e) => e.fence_size(),
            Directive::ForeignMod(f) => f.fence_size(),
            Directive::Function(f) => f.fence_size(),
            Directive::Impl(i) => i.fence_size(),
            Directive::Macro(m) => m.fence_size(),
            Directive::Module(m) => m.fence_size(),
            Directive::Struct(s) => s.fence_size(),
            Directive::Trait(t) => t.fence_size(),
            Directive::Type(t) => t.fence_size(),
            Directive::Variable(v) => v.fence_size(),
        }
    }
}

/// Extract the docstring from the attrs of an item.
///
/// Args:
///     :attrs: ``syn::attr::Attribute`` vec.
///
/// Returns:
///     A vec of strings, where each string is a line of a documentation
///     comment. If there are no documentation comments, an empty vec is
///     returned.
pub(crate) fn extract_doc_from_attrs(attrs: &Vec<Attribute>) -> Vec<String> {
    let mut content = Vec::new();
    for attr in attrs {
        if attr.path().segments.is_empty() {
            continue;
        }

        if attr.path().segments[0].ident != "doc" {
            continue;
        }

        if let Expr::Lit(e) = &attr.meta.require_name_value().unwrap().value {
            if let Lit::Str(d) = &e.lit {
                let line = d.value();
                content.push(line.strip_prefix(' ').unwrap_or(&line).to_string());
            }
        }
    }
    content
}

/// DRY macro to check which visibility value to pass to inner items.
#[macro_export]
macro_rules! visibility_to_inherit {
    ($directive:expr, $inherited:expr) => {
        if let Visibility::Inherited = $directive {
            $inherited
        }
        else {
            Some(&$directive)
        }
    };
}

/// Enum for the values of the
/// :rust:struct:`~sphinx-rustdocgen::directives::DirectiveOption::Vis` option
///
/// The enum is ordered ``Pub < Crate < Pvt``, so it can be efficiently
/// compared for filtering. Note that ordering here is opposite to that of the
/// visibility itself.
#[derive(Clone, Copy, Debug, Default, Deserialize, Ord, PartialOrd, Eq, PartialEq)]
#[serde(rename_all = "lowercase")]
pub(crate) enum DirectiveVisibility {
    #[default]
    Pub = 0,
    Crate = 1,
    Pvt = 2,
}

impl DirectiveVisibility {
    fn effective_visibility(
        visibility: &Visibility,
        inherited_visibility: &Option<&Visibility>,
    ) -> DirectiveVisibility {
        match visibility {
            Visibility::Public(_) => DirectiveVisibility::Pub,
            Visibility::Restricted(v) => {
                if v.path.to_token_stream().to_string() == "crate" {
                    DirectiveVisibility::Crate
                }
                else {
                    DirectiveVisibility::Pvt
                }
            }
            Visibility::Inherited => match inherited_visibility {
                None => DirectiveVisibility::Pvt,
                Some(v) => Self::effective_visibility(v, &None),
            },
        }
    }
}

impl Display for DirectiveVisibility {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            DirectiveVisibility::Pub => f.write_str("pub"),
            DirectiveVisibility::Crate => f.write_str("crate"),
            DirectiveVisibility::Pvt => f.write_str("pvt"),
        }
    }
}

impl FromStr for DirectiveVisibility {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let s = s.to_lowercase();
        if s == "pub" {
            Ok(DirectiveVisibility::Pub)
        }
        else if s == "crate" {
            Ok(DirectiveVisibility::Crate)
        }
        else if s == "pvt" {
            Ok(DirectiveVisibility::Pvt)
        }
        else {
            Err(())
        }
    }
}

/// Check the options to determine if the visibility of a directive matches
/// the specified max visibility and return empty Vec if not.
///
/// This macro should be used within a function and will cause it to return
/// early when the visibility of the options provided does not meet the
/// specified max.
///
/// Args:
///     :options: A vec of ``DirectiveOption``
///     :max: The maximum visibility that should be included in the output.
#[macro_export]
macro_rules! check_visibility {
    ($options:expr, $max:expr) => {{
        for option in $options.iter() {
            if let DirectiveOption::Vis(v) = option {
                if v > $max {
                    return Vec::new();
                }
            }
        }
    }};
}

/// The different index entry types.
///
/// This corresponds to the Python enum
/// :py:class:`sphinxcontrib_rust.items.SphinxIndexEntryType`.
#[derive(Copy, Clone, Debug)]
#[repr(i8)]
pub(crate) enum IndexEntryType {
    None = -1,
    Normal = 0,
    WithSubEntries = 1,
    SubEntry = 2,
}

/// Enum to represent the various options for the directives.
///
/// The enum implements the
/// :rust:trait:`~sphinx-rustdocgen::formats::RstContent` and
/// :rust:trait:`~sphinx-rustdocgen::formats::MdContent` traits for easily
/// converting the options to required text.
#[derive(Clone, Debug)]
pub(crate) enum DirectiveOption {
    /// The ``:index:`` option
    Index(IndexEntryType),
    /// The ``:vis:`` option.
    Vis(DirectiveVisibility),
    /// The ``:sig:`` option.
    Sig(String),
    /// The ``:toc:`` option.
    Toc(String),
}

impl RstOption for DirectiveOption {
    fn get_rst_text(&self, indent: &str) -> Option<String> {
        Some(match self {
            DirectiveOption::Index(i) => {
                format!("{indent}:index: {}", *i as i8)
            }
            DirectiveOption::Vis(v) => {
                format!("{indent}:vis: {v}")
            }
            DirectiveOption::Sig(s) => {
                format!("{indent}:sig: {s}")
            }
            DirectiveOption::Toc(t) => {
                format!("{indent}:toc: {t}")
            }
        })
    }
}

impl MdOption for DirectiveOption {
    fn get_md_text(&self) -> Option<String> {
        Some(match self {
            DirectiveOption::Index(i) => {
                format!(":index: {}", *i as i8)
            }
            DirectiveOption::Vis(v) => {
                format!(":vis: {v}")
            }
            DirectiveOption::Sig(s) => {
                format!(":sig: {s}")
            }
            DirectiveOption::Toc(t) => {
                format!(":toc: {t}")
            }
        })
    }
}

macro_rules! push_sorted {
    ($sorted:expr, $items:expr, $name:expr) => {{
        if !$items.is_empty() {
            $items.sort_by(|a, b| a.name().cmp(b.name()));
            $sorted.push(($name, $items));
        }
    }};
}

/// Order the items for documentation
///
/// The items are ordered using the following rules:
///
/// 1. If the item is a module without content, it is removed and a link to the
///    module is added to the ``toctree``. If there are no such module, the
///    ``toctree`` isn't added.
/// 2. Each directive is then separated by type and ordered alphabetically
///    except for ``impl`` directives.
/// 3. All ``impl`` blocks associated with a struct or enum are ordered after
///    it, starting with the associated ``impl`` block, followed by trait
///    ``impl`` blocks in alphabetical order.
///
/// Returns:
///    An vec of module directives that have no items and a vec of
///    section names with their directives.
fn order_items(
    items: Vec<Directive>,
) -> (Vec<ModuleDirective>, Vec<(&'static str, Vec<Directive>)>) {
    let mut enums = vec![];
    let mut fns = vec![];
    let mut impls = vec![];
    let mut macros = vec![];
    let mut toc_tree_modules = vec![];
    let mut defined_modules = vec![];
    let mut structs = vec![];
    let mut traits = vec![];
    let mut types = vec![];
    let mut vars = vec![];

    for item in items {
        match item {
            Directive::Crate(_) => {
                unreachable!("Unexpected crate directive as an item")
            }
            Directive::Enum(e) => enums.push(Directive::Enum(e)),
            Directive::Executable(_) => {
                unreachable!("Unexpected executable directive as an item")
            }
            Directive::ForeignMod(f) => {
                for item in f.items {
                    match item {
                        Directive::Function(f) => fns.push(Directive::Function(f)),
                        Directive::Type(t) => types.push(Directive::Type(t)),
                        Directive::Variable(v) => vars.push(Directive::Variable(v)),
                        _ => {
                            unreachable!("Foreign mod should not have any other item types")
                        }
                    }
                }
            }
            Directive::Function(f) => fns.push(Directive::Function(f)),
            Directive::Impl(i) => impls.push(Directive::Impl(i)),
            Directive::Macro(m) => macros.push(Directive::Macro(m)),
            Directive::Module(m) => {
                if m.items.is_empty() {
                    toc_tree_modules.push(m)
                }
                else {
                    defined_modules.push(Directive::Module(m))
                }
            }
            Directive::Struct(s) => structs.push(Directive::Struct(s)),
            Directive::Trait(t) => traits.push(Directive::Trait(t)),
            Directive::Type(t) => types.push(Directive::Type(t)),
            Directive::Variable(v) => vars.push(Directive::Variable(v)),
        }
    }

    impls.sort_by(|a, b| a.name().cmp(b.name()));

    let mut sorted = Vec::new();
    push_sorted!(sorted, defined_modules, "Inline Modules");
    push_sorted!(sorted, types, "Types");
    push_sorted!(sorted, vars, "Variables");
    push_sorted!(sorted, macros, "Macros");
    push_sorted!(sorted, fns, "Functions");

    push_sorted!(sorted, traits, "Traits");
    push_sorted!(sorted, enums, "Enums");
    push_sorted!(sorted, structs, "Structs and Unions");
    push_sorted!(sorted, impls, "Impls");

    (toc_tree_modules, sorted)
}
