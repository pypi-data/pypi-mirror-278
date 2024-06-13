from typing import List

import numpy as np

from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.structures.character.joint import Joint

class Skeleton:
    """A class to represent a skeleton (or rig).

    Attributes
    ----------
    name : str
        Name given to the skeleton. Not necessarily unique.
    root : Joint
        Root joint of the hierarchy for the skeleton.
    """

    def __init__(self, root: Joint, name: str = "new skeleton"):
        """**Default constructor for the Skeleton class.**

        Parameters
        ----------
        root : Joint
            Root joint of the hierarchy for the skeleton.
        name : str, optional
            Name of the skeleton, by default "new skeleton".
        """
        self.name = name
        self.root = root
   
    def as_joint_list(self) -> List[Joint]:
        """Returns the skeleton as a list of joints.

        Note
        ----
        The list is in depth-first order starting from the root.

        Returns
        -------
        (Joint) list
            List of joints in the skeleton.
        """
        adjacency_list = []
        stack = [self.root]
        while stack:
            joint = stack.pop()
            adjacency_list.append(joint)
            stack.extend(reversed(joint.children))
        return adjacency_list
    
    def as_joint_dict(self) -> dict:
        """Returns the skeleton as a dictionary of joints.

        Note
        ----
        The dictionary is in depth-first order starting from the root.

        Returns
        -------
        dict
            Dictionary of joints in the skeleton.
        """
        joint_dict = {}
        for joint in self.as_joint_list():
            joint_dict[self.get_joint_id(joint)] = joint.name
        return joint_dict

    def as_hierarchy_list(self) -> List[Joint]:
        """Returns the skeleton as a list of joints.

        Note
        ----
        The list is in breadth-first order starting from the root.

        Returns
        -------
        (Joint) list
            List of joints in the skeleton.
        """
        hierarchy_list = []
        current_level = [self.root]
        while current_level:
            hierarchy_list.append(current_level)
            next_level = []
            for joint in current_level:
                next_level.extend([child for child in joint.children])
            current_level = next_level
        return hierarchy_list  
    
    def as_bind_transform_vector(self) -> VectorizedArray:
        local_bind_matrices = []
        for joint in self.as_joint_list():
            local_bind_matrices.append(joint.local_bind_transform.getTransformMatrix())
        arr_local_bind_matrices = np.array(local_bind_matrices).reshape(-1, 4, 4)
        return VectorizedArray(
            array=arr_local_bind_matrices,
            labels=["local_bind_matrix"],
        )
    
    def as_parent_id_vector(self) -> VectorizedArray:
        parent_ids_list = [-(2 ** 31)]
        for joint in self.as_joint_list()[1:]:  # skip the root joint
            parent_id = self.get_joint_id(joint.parent)
            parent_ids_list.append(parent_id)
        return VectorizedArray(
            array=np.array(parent_ids_list, dtype=np.int32),
            labels=["parent_id"],
        )

    def get_joint_by_name(self, name):
        """Returns the joint with the given name.

        Parameters
        ----------
        name : str
            Name of the joint to return.

        Returns
        -------
        Joint
            Joint with the given name. None if not found.
        """
        for joint in self.as_joint_list():
            if joint.name == name:
                return joint
        return None

    def get_nb_joints(self):
        return len(self.as_joint_list())
    
    def get_joint_by_id(self, id):
        return self.as_joint_list()[id]
    
    def get_joint_id(self, joint: Joint):
        return self.as_joint_list().index(joint)
    

    def __repr__(self):
        return "Skeleton: " + self.name + ", Root: " + self.root.name
    