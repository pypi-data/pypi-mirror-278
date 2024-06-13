#src/ofnodes/sorting/mixins.py

import logging
from ofnodes.nodes.singlynode import SinglyNode

logger = logging.getLogger(__name__)

class BubbleSortMixin:
    """Mixin class providing bubble sort functionality for data structures."""
    __slots__ = ()
    def reference_based_bubble_sort(self, ascending=True):
        """Sorts the nodes of the singly linked data structure using bubble sort.

        This method sorts the nodes of the singly linked list in place using the
        bubble sort algorithm. It supports both ascending and descending order
        based on the `ascending` parameter.

        Args:
            ascending (bool, optional): Specifies whether to sort the elements in ascending order (default) or descending order.

        Returns:
            None: This method modifies the original linked list in place.

        Raises:
            TypeError: If the elements in the list are not homogeneous (i.e., not all of the same type).

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.reference_based_bubble_sort()
            >>> sllist
            SinglyLinkedList([2, 4, 5, 6, 8])
            >>> sllist.reference_based_bubble_sort(ascending=False)
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
        if not hasattr(self, '_head'):
            raise TypeError("reference_based_bubble_sort can only be used on reference-based data structures like linked lists.")
        if not self._head or not self._head.next:  # it's a zero node or one node list
            return

        # check for homogenous types
        types = set()
        current = self._head
        while current:
            types.add(type(current.data))
            current = current.next
        if len(types) > 1:
            raise TypeError("All elements in the data structure must be of the same type.")

        unsorted = True
        while unsorted:
            unsorted = False
            current = self._head
            while current.next:  # find a node to right sort
                if ascending:
                    if current._data > current.next._data: # sort the data right
                        current._data, current.next._data = current.next._data, current._data
                        unsorted = True
                else:  # it's descending
                    if current._data < current.next._data:
                        current._data, current.next._data = current.next._data, current._data
                        unsorted = True
                current = current.next


    def index_based_bubble_sort(self, ascending=True):
        """Sorts the elements of the index-based data structure using bubble sort.

        This method sorts the elements of the index-based data structure in place
        using the bubble sort algorithm. It supports both ascending and descending
        order based on the `ascending` parameter.

        Each iteration of the inner loop starts at the first index and ends one index
        before the last unsorted index. This ensures that with each pass, the largest
        unsorted element is moved to its correct position in ascending order, or
        the smallest unsorted element is moved to its correct position in descending order.

        The outer loop acts as a counter for the number of passes through the structure.
        It doesn't directly visit each index but instead reduces the range of the inner loop
        with each pass.

        If any iteration of the inner loop results in zero swaps, the structure is
        considered sorted and the method exits early to optimize performance.

        Args:
            ascending (bool): If True, sorts the elements in ascending order.
                If False, sorts the elements in descending order. Defaults to True.

        Raises:
            TypeError: If the data structure does not support index-based access,
                or if the elements are not homogenous (i.e., not all of the same type).

        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.index_based_bubble_sort()
            >>> raarray
            RandomAccessArray([2, 4, 5, 6, 8])
            >>> raarray.index_based_bubble_sort(ascending=False)
            >>> raarray
            RandomAccessArray([8, 6, 5, 4, 2])
        """
        # Check instance for enabled indexing
        if not hasattr(self, '__getitem__'):
            raise TypeError("index_based_bubble_sort can only be used on data structures that support index-based access.")

        n = len(self)

        if n in (0, 1):  # no need to sort
            return

        # Check for  homogenous elements
        types = {type(i) for i in self}
        if len(types) > 1:
                raise TypeError("All elements in the data structure must be of the same type.")

        # perform bubble sort
        for i in range(n):
            unsorted = False
            for j in range(n - i - 1):
                if (ascending and self[j] > self[j + 1]) or (not ascending and self[j] < self[j + 1]):
                    self[j], self[j + 1] = self[j + 1], self[j]
                    unsorted = True
            if not unsorted:
                break

class InsertionSortMixin:
    """Mixin class providing insertion sort functionality for data structures."""
    __slots__ = ()
    def reference_based_insertion_sort(self, ascending=True, key=None):
        """Sorts the nodes of a reference-based object using insertion sort.

        The insertion sort algorithm traverses the singly linked list, starting from the second element
        (the head is considered to be the first element). It divides the list into a sorted and an
        unsorted portion. For each element in the unsorted portion, it iterates over the sorted portion
        to find the correct position to insert the element.

        The outer loop traverses the entire singly linked list, except for the head. It sets `j` to the
        head during each iteration, representing the starting point of the sorted portion. `j` is used
        to traverse the sorted portion until it reaches the current node. The outer loop advances `prev`
        and `current` down the singly linked list.

        The inner loop exits with either `j` being `current` or `j` being the node that should point to
        the current node. If `j` is `current`, the current node is already in its sorted place, and the
        algorithm advances to the next unsorted node. If `j` is not `current`, it should point to `current`.
        The node `current` persists in the key `current` after it's bypassed, i.e., removed from,
        the referenced-based structure.

        If `j` should point to the head of the reference-based object, the current node should be inserted
        at the new head. In other words, the current node is inserted before the first node of the sorted
        portion, and the head of the list is updated to point to the current node.

        Raises:
            TypeError: If the insertion_sort method is used on data structures that do not support
                reference-based operations.
            ValueError: If the singly linked list is empty or contains only one node.

        Example:
            >>> sllist = SinglyLinkedList([2, 4, 3, 1, 5])
            >>> sllist.insertion_sort()
            >>> sllist
            SinglyLinkedList([1, 2, 3, 4, 5])
        """
        if 'head' not in dir(self):
            raise TypeError("insertion_sort can only be used on reference-based data structures like linked lists.")
        if not self._head or not self._head.next:  # it's a zero node or one node list
            return

        # check for homogenous types
        types = set()
        current = self._head
        while current:
            types.add(type(current.data))
            current = current.next
        if len(types) > 1:
            raise TypeError("All elements in the data structure must be of the same type.")

        _sorted = self._head
        unsorted = self._head._next

        while unsorted:
            j = self._head
            key_unsorted = key(unsorted._data) if key else unsorted._data
            while j is not unsorted:
                key_j = key(j._data) if key else j._data
                key_j_next = key(j._next._data) if key else j._next._data
                match ascending:
                    case True:
                        if j is self._head and key_j > key_unsorted:  # then new head
                            _sorted._next = unsorted._next  # bypass
                            self.head = unsorted  # insert
                            break
                        if key_j_next > key_unsorted:
                            _sorted._next = unsorted._next  # bypass
                            j._next, unsorted._next = unsorted, j._next  # insert
                            break
                    case False:
                        if j is self._head and key_j < key_unsorted:  # then new head
                            _sorted._next = unsorted._next  # bypass
                            self.head = unsorted  # insert
                            break
                        if key_j_next < key_unsorted:
                            _sorted._next = unsorted._next  # bypass
                            j._next, unsorted._next = unsorted, j._next  # insert
                            break
                    case _:
                        raise ValueError(f"Unexpected value: {ascending}. Only True or False are allowed.")
                j = j._next
            _sorted, unsorted = unsorted, unsorted._next


    def index_based_insertion_sort(self, ascending=True, key=None):
        """Sorts the elements of the data structure using the insertion sort algorithm with index-based access.

        This method is suitable for short lists or lists that are mostly sorted.

        Raises:
            TypeError: If the data structure does not support index-based access.

        Examples:
            >>> raarray = RandomAccessArray([2, 4, 5, 6, 8])
            >>> raarray
            RandomAccessArray([2, 4, 5, 6, 8])

            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]

            >>> raarray.index_based_insertion_sort()
            >>> raarray
            RandomAccessArray([2, 4, 5, 6, 8])

        Notes:
            - The method modifies the original data structure in place.
            - Time Complexity: O(n^2), where n is the number of elements in the data structure.
        """
        # Check instance for enabled indexing
        if not hasattr(self, '__getitem__'):
            raise TypeError("index_based_insertion_sort can only be used on data structures that support index-based access.")

        if len(self) in (0, 1):  # no need to sort
            return

        for unsorted in range(1, len(self)):
            value = self[unsorted]  # persist the value found using the first key, `i`.
            key_value = key(value) if key else value
            j = unsorted - 1  # compute the first index of the sorted subarray

            logger.debug("Array state: %s", self._data)
            logger.debug("The value %s found at index %s will be inserted at a new position", value, unsorted)
            logger.debug("Sorted portion: %s", self._data[:unsorted])
            logger.debug("Unsorted portion: %s", self._data[unsorted:])

            while j >= 0 and self[j] is not None:
                key_j = key(self[j]) if key else self[j]
                if (ascending and key_value < key_j) or (not ascending and key_value > key_j):
                    self[j + 1] = self[j]  # shift the value of the sorted subarray one to the right
                    j -= 1  # compute the next index of the sorted subarray
                    logger.debug("Array state: %s", self._data)
                    logger.debug("Moved value %s to position %s", self[j + 1], j + 1)
                    logger.debug("Sorted portion: %s", self._data[:unsorted])
                    logger.debug("Unsorted portion: %s", self._data[unsorted:])
                else:
                    logger.debug("j>=0: %s", j>=0)
                    logger.debug("self[j] is not None: %s", self[j] is not None)
                    break

            self[j + 1] = value  # insert the value one to the right of the minimum value


        logger.debug("Array state: %s", self._data)
        logger.debug("The value %s found at index %s will be inserted at a new position", value, unsorted)
        logger.debug("Sorted portion: %s", self._data[:unsorted])
        logger.debug("Unsorted portion: %s", self._data[unsorted:])

class ReverseOrderMixin:
    """Mixin class supporting node order reversal for linked node structures."""
    __slots__ = ()
    def reference_based_reverse_order(self):
        """Reverses the order of elements in the singly linked data structure.

        Returns:
            None: This method modifies the original linked list in place.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.reference_based_reverse_order()
            >>> sllist
            SinglyLinkedList([5, 4, 6, 2, 8])

        Notes:
            - Time Complexity: O(n), where n is the number of elements in the linked list.
        """
        if 'head' not in dir(self):
            raise TypeError("reference_based_reverse_order can only be used on reference-based data structures like linked lists.")
        if not self.head or not self.head.next:  # it's a zero node or one node list
            raise ValueError("Cannot reverse an empty linked list.")
        ## it's more than one node list
        # set the head
        self.head = SinglyNode(self.tail.data)  # trigger the setter
        self.remove_tail()  # remove the node you moved data from
        # complete node order reversal
        current = self._head
        while current is not self.tail:  # or while head_to_tail.next is not None
            node = SinglyNode(self._tail.data)
            node._next, current._next = current._next, node
            self.remove_tail()
            current = current.next

    def index_based_reverse_order(self):
        """Reverses the order of elements in the index-based data structure.

        Returns:
            None: This method modifies the original data structure in place.

        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.index_based_reverse_order()
            >>> raarray
            RandomAccessArray([5, 4, 6, 2, 8])

        Notes:
            - Time Complexity: O(n), where n is the number of elements in the data structure.
        """
        if '__getitem__' not in dir(self):
            raise TypeError("index_based_reverse_order can only be used on data structures that support index-based access.")
        n = len(self)
        for i in range(n // 2):
            # Swap elements symmetrically across the middle
            self[i], self[n - i - 1] = self[n - i - 1], self[i]