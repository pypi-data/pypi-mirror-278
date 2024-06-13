""" Module for code related to generating the index of Rust items """

from collections import defaultdict
from typing import Iterable

# noinspection PyProtectedMember
from sphinx.locale import _  # pylint:disable=protected-access
from sphinx.domains import Index, IndexEntry

from sphinxcontrib_rust.items import RustItem, RustItemType, SphinxIndexEntryType


class RustIndex(Index):
    """Class for implementing the index of Rust items.

    The class inherits from :py:class:`Index` and produces an index of the
    various items documented in the build. The index sections are the item
    types.
    """

    # pylint: disable=too-few-public-methods

    name = "items"
    localname = _("Index of Rust items")
    shortname = _("Rust items")

    def generate(
        self, docnames: Iterable[str] | None = None
    ) -> tuple[list[tuple[str, list[IndexEntry]]], bool]:
        """Generate the index content for a list of items of the same type.

        Args:
            :items: The items to include in the index.
            :subtype: The sub-entry related type. One of
                0 - A normal entry
                1 - A entry with subtypes.
                2 - A sub-entry

        Returns:
            A list of ``(key, list[IndexEntry])`` tuples that can be used as the
            content for generating the index.
        """
        data: dict[RustItemType, list[RustItem]]

        content = defaultdict(list)
        data = self.domain.data
        for item_type, items in data.items():
            if not isinstance(item_type, RustItemType):
                # Sphinx adds some other things to the dict
                continue

            for item in items:
                # Skip items that don't have to be indexed
                if item.index_entry_type == SphinxIndexEntryType.NONE:
                    continue

                # Skip items that are not from the provided list of docnames, if any.
                if item.docname not in (docnames or [item.docname]):
                    continue

                if item.index_entry_type == SphinxIndexEntryType.SUB_ENTRY:
                    # find the appropriate section for the item
                    index_section = {
                        RustItemType.STRUCT: RustItemType.ENUM,
                        RustItemType.VARIABLE: RustItemType.STRUCT,
                        RustItemType.TYPE: RustItemType.TRAIT,
                        RustItemType.FUNCTION: RustItemType.TRAIT,
                    }[item.type_].index_section_name
                else:
                    index_section = item_type.index_section_name

                content[index_section].append(item)

        # Remove any empty sections
        empty_sections = [s for s, i in content.items() if not i]
        for section in empty_sections:
            content.pop(section)

        # Sort items within sections by name so the nesting works properly.
        for section, items in content.items():
            items.sort(key=lambda i: i.name)

        return (
            sorted(
                (s, [i.make_index_entry() for i in items])
                for s, items in content.items()
            ),
            True,
        )
