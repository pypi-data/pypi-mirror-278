# components/nodes/descriptors.py

class Data:
    """Descriptor for managing data attribute in nodes.

    This descriptor ensures data validation when setting the data attribute
    of a node instance.

    Attributes:
        None

    Methods:
        __get__(self, instance, owner): Getter method for retrieving the value of the data attribute.
        __set__(self, instance, value): Setter method for setting the value of the data attribute.
        __delete__(self, instance): Deleter method for deleting the data attribute.

    """
    __slots__ = ()
    def __get__(self, instance, owner):
        """Getter method for retrieving the value of the data attribute."""
        return instance._data

    def __set__(self, instance, value):
        """Setter method for setting the value of the data attribute."""
        if value:  # TODO: perform data validation
            validated_data = value
        setattr(instance, '_data', validated_data)

    def __delete__(self, instance):
        """Deleter method for deleting the data attribute."""
        raise AttributeError(
            f"{type(instance).__name__}'s `data` attribute cannot be deleted."
        )


class Next:
    """Descriptor for managing next attribute in nodes.

    This descriptor restricts direct setting and deletion of the next attribute
    to enforce proper modification of linked list structure.

    Attributes:
        None

    Methods:
        __get__(self, instance, owner): Getter method for retrieving the value of the next attribute.
        __set__(self, instance, value): Setter method for setting the value of the next attribute.
        __delete__(self, instance): Deleter method for deleting the next attribute.

    """
    __slots__ = ()
    def __get__(self, instance, owner):
        """Getter property for the next node in the singly linked list.

        Note:
            This property allows access to the next node in the linked list.
            Modifying the next node should be done using linked list methods
            for consistency and to maintain the integrity of the linked list structure.
        """
        return instance._next

    def __set__(self, instance, value):
        """Setter method for setting the value of the next attribute."""
        raise AttributeError("Cannot set 'next' attribute directly. Use linked list methods for modification.")

    def __delete__(self, instance):
        """Deleter property for the next attribute of the singly node.

        Raises:
            AttributeError: Deleting the `next` attribute is not allowed.
        """
        raise AttributeError(
            f"{type(instance).__name__}'s `next` attribute cannot be deleted."
        )
