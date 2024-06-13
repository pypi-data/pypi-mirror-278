from typing import List, Dict

import numpy as np

from line_profiler import profile

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.animators.baseFkAnimator import BaseFkAnimator, PlayMode


class LocalFkAnimator(BaseFkAnimator):
    """ """
    def __init__(self, skeleton: Skeleton, animations: List[Animation], play_mode: PlayMode = PlayMode.LOOP_ALL):        
        self.vec_bind_transform_matrices = None
        super().__init__(skeleton, animations, play_mode)     

    # @profile
    def _initialize(self):
        super()._initialize()       
        self.vec_bind_transform_matrices = self.skeleton.as_bind_transform_vector()        
        self.vec_bind_transform_matrices = self.vec_bind_transform_matrices.tile((self.nb_anims, 1, 1))

    # @profile
    def _execute(self):        
        lst_output = super()._execute()
        vec_delta_transform_matrices = lst_output[0]

        arr_local_transform_matrices = self.vec_bind_transform_matrices.get() @ vec_delta_transform_matrices.get()

        vec_local_transform_matrices = VectorizedArray(arr_local_transform_matrices, labels=["local_transform"])

        lst_output.append(vec_local_transform_matrices)
        return lst_output
