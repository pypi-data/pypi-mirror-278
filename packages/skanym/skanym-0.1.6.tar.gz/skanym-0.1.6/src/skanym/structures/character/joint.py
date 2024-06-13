import warnings
import copy
from typing import List

import numpy as np

from skanym.structures.data.iTransform import ITransform
from skanym.structures.data.transform import Transform

class Joint:
    """A class to represent a joint.

    A joint is considered a root if it has no parent.

    Attributes
    ----------
    id : int
        Unique id of the joint.
    name : str
        Name given to the joint. Not necessarily unique.
    parent : Joint
        Parent of the joint.
    children : (Joint) list
        List of children joints.
    local_bind_transform : Transform
        Initial transform of the joint in the parent's local coordinate system.
    """

    def __init__(self, name="new joint", parent=None, children = None, local_bind_transform: ITransform=None):
        """**Default constructor for the Joint class.**

        Parameters
        ----------
        name : str, optional
            Name of the joint, by default "new joint".
        local_bind_transform : Transform, optional
            Initial transform relative to the parent, by default identity transform.
        """
        self.name = name
        self.parent: Joint = None
        self.children: List[Joint] = []
        if local_bind_transform is None:
            self.local_bind_transform = Transform()
        else:
            self.local_bind_transform = local_bind_transform


    def add_child(self, joint: 'Joint'):
        """Makes the given joint a child of the current joint.

        Note
        ----
        The joint's parent is updated automatically.

        Parameters
        ----------
        joint : Joint
            The joint to be added as a child.

        Raises
        --------
        If the addition of the joint makes the tree cyclic, an error is raised.
        """
        if joint.parent is None:
            joint.parent = self
            self.children.append(joint)
        elif joint.parent != self:
            old_parent = joint.parent
            old_parent.children.remove(joint)
            joint.parent = self
            self.children.append(joint)
        if self.is_cyclic():
            warnings.warn(
                "Cyclic joint hierarchy detected. The add_child operation has been canceled.", UserWarning
            )
            self.remove_child(joint)

    def add_children(self, joints: List['Joint']):
        """Makes the given joints children of the current joint.

        Note
        ----
        The joints' parents are updated automatically.

        Parameters
        ----------
        joints : (Joint) list
            The joints to be added as children.
        """
        for joint in joints:
            self.add_child(joint)

    def remove_child(self, joint: 'Joint'):
        """Removes the given joint from the children of the current joint.

        Note
        ----
        If the joint is not a child of the current joint, then nothing happens.
        The joint's parent is updated automatically.

        Parameters
        ----------
        joint : Joint
            The joint to be removed.
        """
        if joint in self.children:
            self.children.remove(joint)
            joint.parent = None

    def remove_children(self, joints: List['Joint']):
        """Removes the given joints from the children of the current joint.

        Note
        ----
        The joints' parents are updated automatically.

        Parameters
        ----------
        joints : (Joint) list
            The joints to be removed.
        """
        for joint in joints:
            self.remove_child(joint)

    def remove_all_children(self):
        """Removes all the children of the current joint.

        Note
        ----
        The removed joints' parents are updated automatically.
        """
        self.remove_children(copy.copy(self.children))

    def is_cyclic(self):
        """Checks for cyclicity in the joint hierarchy for the current joint.

        Note: The joint hierarchy is considered cyclic only if a joint is the parent of one of its ancestors.

        Examples
        -------
        >>> root = Joint()
        >>> child1 = Joint()
        >>> child2 = Joint()
        >>> child3 = Joint()
        >>> root.add_children([child1, child2])
        >>> child1.add_child(child3)
        # The joint hierarchy is now:
        #   root -> child1 -> child3
        #        -> child2
        >>> root.is_cyclic()
        False
        >>> child3.add_child(child1)
        # The joint hierarchies are now:
        # root -> child2  and  ... -> child1 -> child3 -> child1 -> child3 -> child1 -> ...
        >>> root.is_cyclic()
        False
        >>> child1.is_cyclic()
        True

        Returns
        -------
        bool
            True if the joint hierarchy is cyclic, False otherwise.
        """

        # List of visited nodes.
        visited = []
        # Stack to keep track of the current node.
        stack = []
        stack.append(self)

        # Run till stack is empty or cycle is found.
        while stack:
            node = stack.pop()
            for child in node.children:
                if child in visited:
                    return True
                else:
                    stack.append(child)
                    visited.append(node)

        # If we reach here, then there is no cycle
        return False
