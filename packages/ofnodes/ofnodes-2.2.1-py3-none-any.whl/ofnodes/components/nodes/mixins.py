# ofnodes/components/nodes/mixins.py
#from ofnodes.nodes.singlynode import SinglyNode
class AddMixin:
    __slots__ = ()
    def __add__(self, other):
        """Add data to the node's data attribute.

        Args:
            other: The data to add to the node's data attribute.

        Raises:
            ValueError: If the provided data is invalid or if the node is not an instance of SinglyNode.

        Notes:
            This method adds the provided data to the node's data attribute after performing
            any necessary validation.

        Returns:
            None

        Examples:  TODO

        """
        if other:
            validated_data = other  # TODO: validate data
            self._data = self._data + validated_data
            return
        raise ValueError("Invalid data to add to SinglyNode.data")
