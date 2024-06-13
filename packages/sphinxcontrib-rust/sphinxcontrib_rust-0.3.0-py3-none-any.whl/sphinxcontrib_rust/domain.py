""" Module for the ``rust`` Sphinx domain for documentation Rust items """

from typing import Optional, Type, Union, Iterable

from docutils.nodes import Element
from docutils.parsers.rst import Directive
from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.domains import Domain, Index, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode
from sphinx.util.typing import RoleFunction

from sphinxcontrib_rust.directives import RustDirective
from sphinxcontrib_rust.index import RustIndex
from sphinxcontrib_rust.items import RustItem, RustItemType

LOGGER = logging.getLogger(__name__)


class RustXRefRole(XRefRole):
    """An :py:class:`XRefRole` extension for Rust roles"""

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        """Process the link by parsing the tile and the target"""
        # pylint: disable=too-many-arguments
        if not has_explicit_title:
            # This is the most common case where
            # only the target is specified as the title like
            # `` :rust:struct:`~crate::module::Struct` ``
            # title == target in this case

            # Remove any leading or trailing ::s.
            # Only meaningful for targets, once support
            # for relative references is added.
            title = title.strip("::")

            # Remove the ~ from the target, only meaningful for titles.
            target = target.lstrip("~")

            # ~ will use only the final part of the name as the title
            # instead of the full path.
            if title[0:1] == "~":
                _, _, title = title[1:].rpartition("::")

        return title, target


class RustDomain(Domain):
    """The Sphinx domain for the Rust programming language.

    The domain provides the various roles and directives that can be used in the Sphinx
    documentation for linking with Rust code.
    """

    name = "rust"
    label = "Rust"

    # The various object types provided by the domain
    object_types: dict[str, ObjType] = {
        t.value: t.get_sphinx_obj_type() for t in RustItemType
    }

    # The various directives add to Sphinx for documenting the Rust object types
    directives: dict[str, Type[Directive]] = {
        t.value: d for t, d in RustDirective.get_directives().items()
    }

    # The various roles added to Sphinx for referencing the Rust object types
    roles: dict[str, Union[RoleFunction, XRefRole]] = {
        # TODO: Customize this role
        r: RustXRefRole()
        for _, r in RustItemType.iter_roles()
    }

    # The indices for all the object types
    indices: list[Type[Index]] = [RustIndex]

    # The domain data created by Sphinx. This is here just for type annotation.
    data: dict[RustItemType, list[RustItem]]

    # Initial data for the domain, gets copied as self.data by Sphinx
    initial_data: dict[RustItemType, list[RustItem]] = {
        t: [] for t in RustItemType
    }  # XXX: Perhaps better to create dict instead of list and key by name.

    # Bump this when the data format changes.
    data_version = 0

    def get_objects(self) -> Iterable[tuple[str, str, str, str, str, int]]:
        for typ, objs in self.data.items():
            if not isinstance(typ, RustItemType):
                continue
            for obj in objs:
                yield (
                    obj.name,
                    obj.display_text,
                    obj.type_.value,
                    obj.docname,
                    obj.anchor,
                    obj.priority,
                )

    def clear_doc(self, docname: str) -> None:
        for typ, objs in self.data.items():
            if isinstance(typ, RustItemType):
                self.data[typ][:] = [o for o in objs if o.docname != docname]

    def _find_match(self, target: str, typ: str | None = None) -> Optional[RustItem]:
        search_types = [RustItemType.from_str(typ)] if typ else self.data.keys()

        matches = set()
        for search_type in search_types:
            matches.update(o for o in self.data[search_type] if o.name == target)

        # No match, return None
        if not matches:
            return None

        # Just 1 match, return it.
        if len(matches) == 1:
            return list(matches)[0]

        # Multiple matches, prefer a match that is not an impl.
        # This is likely to happen with a ref that matches a struct and the impl.
        for match in matches:
            if match.type_ != RustItemType.IMPL:
                return match

        # Return the first one if everything is an impl.
        return list(matches)[0]

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> Element | None:
        """Resolve a reference to a Rust item with the directive type specified"""
        # pylint:disable=too-many-arguments
        match = self._find_match(target, typ)
        return (
            make_refnode(
                builder,
                fromdocname,
                match.docname,
                match.name.replace("::", "-"),
                [contnode],
                match.name,
            )
            if match
            else None
        )

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> list[tuple[str, Element]]:
        """Resolve a reference to a Rust item with an unspecified directive type"""
        # pylint:disable=too-many-arguments
        match = self._find_match(target)
        return (
            make_refnode(
                builder,
                fromdocname,
                match.docname,
                match.name.replace("::", "-"),
                [contnode],
                match.name,
            )
            if match
            else None
        )

    def merge_domaindata(self, docnames: list[str], otherdata: dict) -> None:
        otherdata: dict[RustItemType, list[RustItem]]
        for typ, objs in otherdata.items():
            self.data[typ].extend(o for o in objs if o.docname in docnames)
