from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np
from line_profiler import profile

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray

class BaseAnimator(ABC):
    """ """
    
    # Type alias for the output dictionary
    OutputDictType = Dict[str, Dict[str, List[float]]]
    # Description : Dict[joint_name, Dict[data_label, List[data_value]]]

    def __init__(self, skeleton: Skeleton, animations: List[Animation]):
        self.skeleton = skeleton
        self.animations = None
        self.time = 0.0
        
        self.nb_anims = len(animations)
        self.nb_joints = skeleton.get_nb_joints()
        self.set_animations(animations)
        

    def set_animations(self, animations: List[Animation]):
        self.animations = animations
        self._initialize()

    def set_time(self, time: float):
        self.time = time

    # @profile
    def step(self, delta_time: float = 0.0) -> List[VectorizedArray]:
        self.time += delta_time
        return self._execute()
    
    @abstractmethod
    def _initialize(self):
        pass

    @abstractmethod
    def _execute(self):
        pass

    # @profile
    def output_to_dict(self, lst_output_vector: List[VectorizedArray]) -> List[OutputDictType]:
        lst_output_dict = []
        lst_label = [output_vector.get_labels()[0] for output_vector in lst_output_vector]
        lst_joint_name = [joint.name for joint in self.skeleton.as_joint_list()]
        lst_output_list = [list(output_vector.get()) for output_vector in lst_output_vector]
        nb_output = len(lst_output_list)

        global_id = 0

        for a_id in range(self.nb_anims):
            output_dict = {}
            for j_id in range(self.nb_joints):
                j_name = lst_joint_name[j_id]
                if j_name not in output_dict.keys():
                    output_dict[j_name] = {}
                for l_id in range(nb_output):
                    label = lst_label[l_id]
                    output_dict[j_name][label] = list(lst_output_list[l_id][global_id])
                            
                global_id += 1

            lst_output_dict.append(output_dict)
            
        return lst_output_dict
