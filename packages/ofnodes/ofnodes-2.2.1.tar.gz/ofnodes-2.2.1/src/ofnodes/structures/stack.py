from typing import Optional

from ofnodes.nodes.singlynode import SinglyNode
from ofnodes.components.structures.descriptors import Head
from ofnodes.components.structures.mixins import RemoveMixin,  PrintMixin

class Stack(RemoveMixin, PrintMixin):
    """Support for a reference-based LIFO object.
    
    The head is considered the last node. The head is popped
    and a node pushed onto the stack becomes the new head."""

    __slots__ = ('_head',)

    head = Head()

    def __init__(self, values=None) -> None:
        self._head: Optional[SinglyNode] = None
        if values:
            for value in values:
                self.head = value

    def __dir__(self) -> list[str]:
        # Get the list of attributes and methods from the parent classes
        parent_dir = set(super().__dir__())
        # Filter out private attributes and methods
        parent_dir = {attr for attr in parent_dir if attr not in {'_head', '_tail', '_target'}}
        # Return a sorted list of all attributes and methods
        return sorted(parent_dir)

    def __repr__(self) -> str:
        #return f"{type(self).__name__}(head={type(self.head).__name__}, tail={self.tail})"
        if not self._head:
            return f"{type(self).__name__}()"
        node = self._head
        nodes = []
        while node:
            nodes.append(repr(node.data))
            node = node.next
        return f"{type(self).__name__}([" + ', '.join(nodes) + "])"

    def __str__(self) -> str:
        if not self._head:
            return f"Empty {type(self).__name__}"
        node = self._head
        nodes = []
        while node:
            nodes.append(str(node.data))
            node = node.next
        return ' -> '.join(nodes)

    def push(self, data):
        self.head = data  # trigger the setter, setter validates data

    def pop(self):
        return self.remove_head()

    def peek(self):
        if self._head:
            return self._head.data
        raise IndexError("Stack is empty, cannot peek at top element")

    def display(self):
        self.print_node_data()

    def is_empty(self):
        return self._head is None

