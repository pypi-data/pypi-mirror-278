from typing import Optional, Any

from ofnodes.nodes.singlynode import SinglyNode
from ofnodes.components.structures.descriptors import Head, Tail, Target
from ofnodes.components.structures.mixins import CycleDetectionMixin, SearchMixin, RemoveMixin, InsertHeadMixin, InsertTailMixin, InsertAfterTargetMixin, InsertBeforeTargetMixin, PrintMixin
from ofnodes.sorting.mixins import BubbleSortMixin, InsertionSortMixin, ReverseOrderMixin

class SinglyLinkedList(CycleDetectionMixin, InsertionSortMixin, SearchMixin, RemoveMixin, InsertHeadMixin, InsertTailMixin, InsertAfterTargetMixin, InsertBeforeTargetMixin, PrintMixin, BubbleSortMixin, ReverseOrderMixin):
    """A class representing a singly linked list.

    This class provides functionality to create and manipulate a singly linked list
    data structure. Each node in the linked list contains a reference to the next
    node in the sequence.

    Attributes:
        _head (Optional[SinglyNode]): The head of the linked list.
        _tail (Optional[SinglyNode]): The tail of the linked list.
        _target (Optional[Any]): The target data or node instance.

    Examples:
        >>> linked_list = SinglyLinkedList()
        >>> linked_list
        SinglyLinkedList(head=None, tail=None, target=None)
    """

    __slots__ = ('_head', '_tail', '_target',)
    head = Head()
    tail = Tail()
    target = Target()
    def __init__(self, values=None) -> None:
        self._head: Optional[SinglyNode] = None
        self._tail: Optional[SinglyNode] = None
        self._target: Optional[Any|SinglyNode] = None
        if values:
            for value in values:
                self.tail = value

    def __add__(self, other):
        self.tail = other  # tail attr will validate

    def __repr__(self) -> str:
        #return f"{type(self).__name__}(head={type(self.head).__name__}, tail={self.tail})"
        if not self._head:
            return "SinglyLinkedList()"
        node = self._head
        nodes = []
        while node:
            nodes.append(repr(node.data))
            node = node.next
        return f"{type(self).__name__}([" + ', '.join(nodes) + "])"

    def __str__(self) -> str:
        if not self._head:
            return "Empty Singly Linked List"
        node = self._head
        nodes = []
        while node:
            nodes.append(str(node.data))
            node = node.next
        return ' -> '.join(nodes)

    def __dir__(self) -> list[str]:
        # Get the list of attributes and methods from the parent classes
        parent_dir = set(super().__dir__())
        # Filter out private attributes and methods
        excluded = {'_head', '_tail', '_target', 'reference_based_reverse_order', 'reference_based_bubble_sort','index_based_bubble_sort', 'index_based_reverse_order', 'index_based_insertion_sort', 'reference_based_insertion_sort'}
        parent_dir = {attr for attr in parent_dir if attr not in excluded}
        # Return a sorted list of all attributes and methods
        return sorted(parent_dir)

    def insertion_sort(self, ascending=True, key=None):
        """Sorts the nodes of a reference-based object using insertion sort.

        This method sorts a singly linked list using the insertion sort algorithm. It traverses the list,
        starting from the second element, and divides it into sorted and unsorted portions. Each element
        in the unsorted portion is iteratively placed in the correct position within the sorted portion.

        Args:
            ascending (bool): Determines the sort order. Defaults to True. If True, sorts in ascending order;
                if False, sorts in descending order.

        Raises:
            TypeError: If the method is used on data structures that do not support reference-based operations.
            ValueError: If the singly linked list is empty or contains only one node.

        Returns:
            None

        Example:
            >>> def by_length(s):
            ...     return len(s)

            >>> fruits = ['cherry', 'strawberry', 'fig', 'peach']
            >>> sllist = SinglyLinkedList(fruits)
            >>> sllist.insertion_sort(ascending=False, key=by_length)
            >>> sllist
            SinglyLinkedList(['strawberry', 'cherry', 'peach', 'fig']
        """
        return super().reference_based_insertion_sort(ascending, key)

    def bubble_sort(self, ascending=True, key=None):
        """Sorts the nodes of the singly linked data structure.

        Args:
            ascending (bool, optional): Specifies whether to sort the elements in ascending order (default) or descending order.

        Returns:
            None: This method modifies the original linked list in place.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.bubble_sort()
            >>> sllist
            SinglyLinkedList([2, 4, 5, 6, 8])
            >>> sllist.bubble_sort(ascending=False)
            >>> sllist
            SinglyLinkedList([8, 6, 5, 4, 2])

        Notes:
            - The comparison operation (`>`) is used for elements. For non-numeric data types,
            ensure that the `__gt__` method is defined appropriately for comparison.
            - Time Complexity:
                - Best Case: O(n), when the list is already sorted.
                - Worst Case: O(n^2), when the list is in reverse order.
                - Average Case: O(n^2).
        """
        return super().reference_based_bubble_sort(ascending)

    def reverse_order(self):
        """Reverses the order of elements in the singly linked data structure.

        Returns:
            None: This method modifies the original linked list in place.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.reverse_order()
            >>> sllist
            SinglyLinkedList([5, 4, 6, 2, 8])

        Notes:
            - Time Complexity: O(n), where n is the number of elements in the linked list.
        """
        return super().reference_based_reverse_order()

    def cycle_detection(self):
        """Detects if the singly linked list instance contains a cycle.

        This method checks whether the linked list contains a cycle using Floyd's Tortoise and Hare algorithm.

        Returns:
            bool: True if a cycle is detected, False otherwise.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.cycle_detection()
            False
            >>> setattr(sllist.head.next, '_next', sllist.head.next)
            >>> sllist.cycle_detection()
            True
        """
        return super().reference_based_cycle_detection()
