__docformat__ = "restructuredtext"

import logging
from ofnodes.nodes.singlynode import SinglyNode
from ofnodes.structures.singlylinkedlist import SinglyLinkedList
from ofnodes.structures.randomaccessarray import RandomAccessArray
from ofnodes.structures.stack import Stack



__doc__ = """
ofnodes - an illustration of node-based objects and algorithms in Python
========================================================================
**ofnodes** is a Python Package providing examples of the Author's ability
to implement data structures and algorithms in Python. It is not a substitute
for built-in or other third-party implementations of the same data structures
and algorithms. It aims to illustrate the author's ability to produce a
distributable package of objects behind a thoughtful user interface.

Main Features
-------------
Here is what ofnodes can do:
    - implement a node object with a unidirectional pointer
    - implement and manipulate a linked list object of unidirectional,
    i.e., 'singly linked' nodes.

Included in the library is a Tail descriptor designed to manage the tail attribute of
linked data structures. While the primary purpose of the Tail descriptor is to
facilitate efficient management of the data structure's tail node, its implementation
also aligns with best practices for preventing cyclic dependencies within linked data
structures. By adhering to these design principles, the library promotes safe and
reliable usage of linked data structures, reducing the risk of unintended cyclic
references and associated issues.
"""
__all__ = ['SinglyNode','SinglyLinkedList', 'RandomAccessArray', 'Stack']