"""Defines a node for a singly linked list.

This module contains the definition for the `SinglyNode` class, which represents
a node in a singly linked list. Each node contains data and a reference to the
next node in the list.

Example:
    Typical usage example:

        uni_node = SinglyNode("a string of characters")
"""
from difflib import get_close_matches
from typing import Any, Optional
from ofnodes.components.nodes.descriptors import Data, Next
from ofnodes.components.nodes.mixins import AddMixin


class SinglyNode(AddMixin):
    """Represents a node in a singly linked list.

    Attributes:
        data: The data stored in the node.
        next: Reference to the next node in the linked list. Defaults to None.
    """

    __slots__ = ('_data', '_next')

    data = Data()
    next = Next()

    def __init__(self, data: Any) -> None:
        self._data: Optional[Any] = data
        self._next: Optional[SinglyNode] = None

    def __dir__(self) -> list[str]:
        # Get the list of attributes and methods from the parent classes
        parent_dir = set(super().__dir__())
        # Filter out private attributes and methods
        parent_dir = {attr for attr in parent_dir if attr not in {'_data', '_next',}}
        # Return a sorted list of all attributes and methods
        return sorted(parent_dir)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            "("
            f"data={repr(self.data)}"
            ")"
        )

    def __str__(self) -> str:
        return str(self.data)
