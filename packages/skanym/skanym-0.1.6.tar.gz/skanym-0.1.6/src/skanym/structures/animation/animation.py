import numpy as np

from typing import List

from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.structures.animation.animationCurve import AnimationCurve

class Animation:
    def __init__(self,
                 name: str = "new_animation",
                 duration: float = 1.0,
                 shift: float = 0.0,
                 position_curves: List[AnimationCurve] = None,
                 rotation_curves: List[AnimationCurve] = None):
        self.name = name
        self.duration = duration
        self.shift = shift
        if position_curves is None:
            self.position_curves = []
        else:
            self.position_curves = position_curves

        if rotation_curves is None:
            self.rotation_curves = []
        else:
            self.rotation_curves = rotation_curves

    def get_position_curves_joint_ids(self) -> List[int]:
        return [curve.joint_id for curve in self.position_curves]
    
    def get_rotation_curves_joint_ids(self) -> List[int]:
        return [curve.joint_id for curve in self.rotation_curves]
        
    def get_position_curves_count(self) -> int:
        return len(self.position_curves)
    
    def get_rotation_curves_count(self) -> int:
        return len(self.rotation_curves)
    
    @staticmethod
    def animations_as_duration_vector(animations:List["Animation"]) -> VectorizedArray:
        lst_durations = [anim.duration for anim in animations]
        arr_durations = np.array(lst_durations)
        return VectorizedArray(array=arr_durations, labels=["duration"])
    
        

    