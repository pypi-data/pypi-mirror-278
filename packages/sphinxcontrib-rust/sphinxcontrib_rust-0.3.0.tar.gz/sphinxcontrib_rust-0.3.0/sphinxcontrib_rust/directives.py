""" Module for all the directive classes of the Rust domain """

from abc import ABC, abstractmethod
from typing import Sequence, Type

from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.addnodes import desc_signature
from sphinx.directives import (
    ObjDescT,
    ObjectDescription,
    nl_escape_re,
    strip_backslash_re,
)
from sphinx.util.nodes import make_id

from sphinxcontrib_rust.items import RustItem, RustItemType, SphinxIndexEntryType


class RustDirective(ABC, ObjectDescription[Sequence[str]]):
    """Base class for Rust directives.

    This class implements most of the logic for the directives. For each directive,
    there is a subclass that overrides any directive specific behaviour.

    The input for the directives is generated with the Rust code in
    :rust:module:`sphinx-rustdocgen::directives`
    """

    option_spec = {
        "index": lambda arg: SphinxIndexEntryType(int(arg)),
        "vis": directives.unchanged_required,
        "sig": directives.unchanged,
        "toc": directives.unchanged,
    }

    @property
    @abstractmethod
    def rust_item_type(self) -> RustItemType:
        """The Rust object type for the directive"""
        raise NotImplementedError

    @classmethod
    def get_directives(cls) -> dict[RustItemType, Type["RustDirective"]]:
        """Get all the directives for the object types"""
        return {
            RustItemType.CRATE: RustCrateDirective,
            RustItemType.ENUM: RustEnumDirective,
            RustItemType.EXECUTABLE: RustExecutableDirective,
            RustItemType.FUNCTION: RustFunctionDirective,
            RustItemType.IMPL: RustImplDirective,
            RustItemType.MACRO: RustMacroDirective,
            RustItemType.MODULE: RustModuleDirective,
            RustItemType.STRUCT: RustStructDirective,
            RustItemType.TRAIT: RustTraitDirective,
            RustItemType.TYPE: RustTypeDirective,
            RustItemType.VARIABLE: RustVariableDirective,
        }

    def add_target_and_index(
        self, name: Sequence[str], sig: str, signode: desc_signature
    ) -> None:
        """Adds the item to the domain and generates the index for it.

        This is called after :py:func:`handle_signature` has executed.

        Args:
            :name: The name of the item, which is the return value from
                :py:func:`handle_signature`.
            :sig: The argument to the directive, which is the Rust path
                of the item set by the Rust doc generator.
            :signode: The docutils node of the for item.
        """
        fullname = "::".join(name)  # XXX: Can we just use sig here?
        node_id = make_id(self.env, self.state.document, "", fullname)
        signode["ids"].append(node_id)

        item = RustItem(
            name=fullname,
            display_text=self.options.get("sig", name[-1]),
            type_=self.rust_item_type,
            docname=self.env.docname,
            anchor="-".join(name),  # Need to join with - for HTML anchors
            index_entry_type=self.options["index"],
            index_text=self.options.get(
                "toc", f"{self.rust_item_type.display_text} {name[-1]}"
            ),
            index_descr=(
                self.content[0]
                if self.content and not self.content[0].startswith("..")
                else ""
            ),
        )

        # Add to the domain
        self.env.domains["rust"].data[self.rust_item_type].append(item)

        if item.index_entry_type != SphinxIndexEntryType.NONE:
            self.indexnode["entries"].append(("single", fullname, node_id, "", None))

    def get_signatures(self) -> list[str]:
        """Override the default get_signatures method, which splits the signatures by line.

        Currently, only one signature is allowed for each Rust object, and due to the use
        of where on new lines, it is all part of one signature. Only the final newline is
        removed.

        See Also:
            * `Docs for the method`_
            * `Source code for super`_

        .. _`Docs for the method`:
            https://www.sphinx-doc.org/en/master/_modules/sphinx/directives.html#ObjectDescription.get_signatures
        .. _`Source code for super`:
            https://www.sphinx-doc.org/en/master/_modules/sphinx/directives.html#ObjectDescription.get_signatures
        """
        sig = nl_escape_re.sub("", self.arguments[0]).strip()
        return (
            [strip_backslash_re.sub(r"\1", sig)]
            if self.config.strip_signature_backslash
            else [sig]
        )

    def handle_signature(self, sig: str, signode: addnodes.desc_signature) -> ObjDescT:
        """Handle the directive and generate its display signature.

        The display signature is what is displayed instead of the directive name and
        options in the generated output. The ``:sig:`` option of the directive is used
        to override the provided ``sig`` value. If the option is not set, the item type
        and the final component of the path are used.

        Raising ``ValueError`` will put the ``sig`` value into a single node, which
        is what the super implementation does.

        Args:
            :sig: The argument of the directive as set during doc generation, not the
                ``:sig:`` option. The Rust side of the code will put the full Rust path
                of the item as the argument.
            :signode: The docutils node for the item, to which the display signature nodes
                should be appended.

        Returns:
            The path for the object, which is a tuple of the Rust path components and
            defines the hierarchy of the object for indexing.
        """
        path = tuple(sig.split("::"))
        # TODO: Parse the signature as RST content and handle multi-line
        signode += addnodes.desc_name(
            sig,
            self.options.get("sig", f"{self.rust_item_type.display_text} {path[-1]}"),
        )
        signode.path = path
        return path

    def _object_hierarchy_parts(
        self, sig_node: addnodes.desc_signature
    ) -> tuple[str, ...]:
        """Returns the hierarchy of the object for indexing and de-duplication.

        Args:
            :sig_node: The docutils node of the for item.

        Returns:
            A tuple of the Rust path for the item, as set during the
            doc generation.
        """
        return sig_node.path

    def _toc_entry_name(self, sig_node: addnodes.desc_signature) -> str:
        """Generate the TOC entry for the item.

        For most directives, this is just the item type and identifier of the
        item. The ``:toc:`` option is set during doc generation where that is
        not sufficient (``impl`` blocks) or not desired (enum variants).

        Args:
            sig_node: The docutils node for the item.

        Returns:
            The text to display for the item in the TOC and sidebar.
        """
        return self.options.get(
            "toc", f"{self.rust_item_type.display_text} {sig_node.path[-1]}"
        )


class RustCrateDirective(RustDirective):
    """Directive for handling crate documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.CRATE

    def _toc_entry_name(self, sig_node: addnodes.desc_signature) -> str:
        return ""


class RustEnumDirective(RustDirective):
    """Directive for handling enum documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.ENUM


class RustExecutableDirective(RustDirective):
    """Directive for handling executable documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.EXECUTABLE

    def _toc_entry_name(self, sig_node: addnodes.desc_signature) -> str:
        return ""


class RustFunctionDirective(RustDirective):
    """Directive for handling function documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.FUNCTION


class RustImplDirective(RustDirective):
    """Directive for handling function documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.IMPL


class RustMacroDirective(RustDirective):
    """Directive for handling function documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.MACRO


class RustModuleDirective(RustDirective):
    """Directive for handling module documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.MODULE

    def _toc_entry_name(self, sig_node: addnodes.desc_signature) -> str:
        return ""


class RustStructDirective(RustDirective):
    """Directive for handling struct documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.STRUCT


class RustTraitDirective(RustDirective):
    """Directive for handling trait documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.TRAIT


class RustTypeDirective(RustDirective):
    """Directive for handling type documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.TYPE


class RustVariableDirective(RustDirective):
    """Directive for handling type documentation"""

    @property
    def rust_item_type(self) -> RustItemType:
        return RustItemType.VARIABLE
