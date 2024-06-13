# src/ofnodes/components/structures/descriptors.py

from ofnodes.nodes.singlynode import SinglyNode

class Head:
    __slots__ = ()
    def __get__(self, instance, owner):
        """Descriptor for managing the head/top of a data structure.

        This descriptor provides getter, setter, and deleter methods for managing the
        head/top of a data structure. It encapsulates the logic related to setting,
        getting, and deleting the head/top element of the data structure.

        Attributes:
            None

        Examples:
            This descriptor can be used in various data structures, such as linked lists,
            stacks, queues, etc., to manage the head/top element.

            >>> class Stack:
            ...     head = Head()
            ...
            >>> stack = Stack()
            >>> stack.head = 42
            >>> stack.head
            42
        """
        return instance._head

    def __set__(self, instance, value):
        """Setter method for the head/top of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.
            value: The value to be set as the head/top element.

        Returns:
            None

        Raises:
            None

        Examples:
            This method can be used in various data structures to set the head/top
            element.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 1, 5])
            >>> sllist
            SinglyLinkedList([8, 2, 1, 5]

            >>> stack = Stack([8, 2, 1, 5])
            >>> stack
            Stack([5, 1, 2, 8])
        """
        if isinstance(value, SinglyNode):
            node = value
        else:
            node = SinglyNode(value)

        match instance.__class__.__name__:
            case 'Stack':
                if instance._head is None:
                    instance._head = node
                    #instance._tail = node
                else:
                    setattr(node, '_next', instance._head)
                    instance._head = node
            case 'SinglyLinkedList':
                if instance._head is None:
                    instance._head = node
                    instance._tail = node
                else:
                    setattr(node, '_next', instance._head)
                    instance._head = node

    def __delete__(self, instance):
        """Deleter method for the head/top of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.

        Returns:
            None

        Raises:
            AttributeError: Deleting the `head` attribute is not allowed.

        Examples:
            This method can be used in various data structures to delete the head/top
            element.

        Examples:
            >>> llist = SinglyLinkedList()
            >>> del llist.head
            AttributeError: SinglyLinkedList's `head` attribute cannot be deleted.
        """
        raise AttributeError(
            f"{type(instance).__name__}'s `head` attribute " "cannot be deleted."
        )

class Tail:
    """Descriptor for managing the tail of a data structure.

    This descriptor provides getter, setter, and deleter methods for managing the
    tail of a data structure. It encapsulates the logic related to setting, getting,
    and deleting the tail node of the data structure.

    Attributes:
        None

    Examples:
        This descriptor can be used in various data structures, such as linked lists,
        stacks, queues, etc., to manage the tail/top element.

        >>> class SinglyLinkedList:
        ...     tail = Tail()
        ...
        >>> llist = SinglyLinkedList()
        >>> llist.tail = "first node"
        >>> llist.tail
        'first node'
    """
    __slots__ = ()
    def __get__(self, instance, owner):
        """Getter method for the tail of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.
            owner: The class that owns the instance.

        Returns:
            Any | None: The tail of the data structure, or None if the
                data structure is empty.

        Notes:
            The `tail` property allows access to the last node in the data structure.

        Examples:
            This method can be used in various data structures to retrieve the tail
            node.

            >>> llist = SinglyLinkedList()
            >>> llist.tail = "first node"
            >>> llist.tail
            'first node'
        """
        return instance._tail

    def __set__(self, instance, value):
        """Setter method for the tail of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.
            value: The value to be set as the tail.

        Returns:
            None

        Notes:
            Setting the `tail` property allows modification of the last node in the
            data structure.
        """
        if isinstance(value, SinglyNode):
            node = value
        else:
            node = SinglyNode(value)

        if instance._head is None:
            setattr(instance, "_head", node)
            setattr(instance, "_tail", node)
        else:
            setattr(instance._tail, "_next", node)
            setattr(instance, "_tail", node)

    def __delete__(self, instance):
        """Deleter method for the tail of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.

        Returns:
            None

        Raises:
            AttributeError: Deleting the `tail` attribute is not allowed.

        Examples:
            This method can be used in various data structures to delete the tail
            node.

            >>> llist = SinglyLinkedList()
            >>> del llist.tail
            AttributeError: The `tail` attribute cannot be deleted.
        """
        raise AttributeError(
            f"{type(instance).__name__}'s `tail` attribute cannot be deleted."
        )

class Target:
    """Descriptor for managing the target node data in a data structure.

    This descriptor provides getter, setter, and deleter methods for managing the
    target node data in a data structure. It encapsulates the logic related to
    comparing node data to the target data and assigning the first matching node
    instance to the target property.

    Attributes:
        None

    Examples:
        This descriptor can be used in various data structures, such as linked lists,
        stacks, queues, etc., to manage the target node data.

        >>> class SinglyLinkedList:
        ...     target = Target()
        ...
        >>> sllist = SinglyLinkedList()
        >>> sllist.target = '5 node'
        Empty SinglyLinkedList(). Target data is assigned to SinglyLinkedList's target property.
    """
    __slots__ = ()
    def __get__(self, instance, owner):
        """Getter method for the target node data of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.
            owner: The class that owns the instance.

        Returns:
            target: The first node instance of the data structure containing data
            matching the target. If no target match, the data is assigned as passed
            to target.

        Notes:
            Any data can be assigned as the target data. Each node in the data structure
            has its data compared to the target data. The first node instance data that
            match the target data is assigned to the `.target` property. If a match is
            not found, the target data is stored as is in the `.target` attribute.

        Examples:
            This method can be used in various data structures to retrieve the target
            node data.

            >>> sllist = SinglyLinkedList()
            >>> sllist.target = '5 node'
            Empty SinglyLinkedList(). Target data is assigned to SinglyLinkedList's target property.
        """
        return instance._target

    def __set__(self, instance, target_data):
        """Setter method for the target node data of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.
            target_data (Any): The data for which to match to node data.

        Returns:
            None

        Notes:
            Setting the `target` property allows modification of the target node data
            in the data structure.
        """
        if instance._head is None:
            raise ValueError(f"Cannot assign target data to empty {type(instance).__name__}.")

        if target_data:
            #  TODO: data validation
            instance._target = target_data
        else:
            raise ValueError("Target data unacceptable.")

    def __delete__(self, instance):
        """Deleter method for the target node data of the data structure.

        Args:
            instance: An instance of the class where the descriptor is used.

        Returns:
            None

        Raises:
            AttributeError: Deleting the `target` attribute is not allowed.

        Examples:
            This method can be used in various data structures to delete the target
            node data.

            >>> sllist = SinglyLinkedList()
            >>> del sllist.target
            AttributeError: SinglyLinkedList's `target` attribute cannot be deleted.
        """
        raise AttributeError(
            f"{type(instance).__name__}'s `target` attribute cannot be deleted."
        )
