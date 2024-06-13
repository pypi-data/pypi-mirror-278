from typing import List

import numpy as np

from line_profiler import profile

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.animators.baseFkAnimator import PlayMode
from skanym.animators.localFkAnimator import LocalFkAnimator

class GlobalFkAnimator(LocalFkAnimator):
    """ """

    def __init__(self, skeleton: Skeleton, animations: List[Animation], play_mode: PlayMode = PlayMode.LOOP_ALL):
        self.vec_parent_ids = None
        super().__init__(skeleton, animations, play_mode)

    # @profile
    def _initialize(self):
        super()._initialize()
        vec_parent_ids = self.skeleton.as_parent_id_vector()
        self.vec_parent_ids = vec_parent_ids.tile(self.nb_anims)

    @profile
    def _execute(self):
        lst_output = super()._execute()
        vec_local_transform_matrices = lst_output[1]

        arr_parent_ids = self.vec_parent_ids.tile(1)
        arr_parent_ids_addends = (
            np.arange(self.nb_anims).repeat(self.nb_joints) * self.nb_joints
        )
        arr_parent_ids += arr_parent_ids_addends
        vec_parent_ids = VectorizedArray(arr_parent_ids, labels=["parent_id"])

        arr_local_transform_matrices = vec_local_transform_matrices.get()
        arr_global_transform_matrices = np.copy(arr_local_transform_matrices)
        for i in range(self.nb_anims * self.nb_joints):
            parent_id = vec_parent_ids[i]
            if parent_id >= 0:
                arr_global_transform_matrices[i] = (
                    arr_global_transform_matrices[parent_id]
                    @ arr_local_transform_matrices[i]
                )

        vec_global_transform_matrices = VectorizedArray(
            arr_global_transform_matrices, labels=["global_transform"]
        )

        lst_output.append(vec_global_transform_matrices)
        return lst_output
