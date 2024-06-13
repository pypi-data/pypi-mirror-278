from typing import List, Tuple
from enum import Enum

import numpy as np
import quaternion

from line_profiler import profile

from skanym.animators.baseAnimator import BaseAnimator
from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.utils.conversion import quaternionToRotationMatrix

class PlayMode(Enum):
    LOOP_ALL = 0
    WAIT_THEN_LOOP = 1
    NO_LOOP = 2

class BaseFkAnimator(BaseAnimator):
    """ """

    def __init__(self, skeleton: Skeleton, animations: List[Animation], play_mode: PlayMode = PlayMode.LOOP_ALL):
        self.nb_anims = None
        self.nb_joints = None

        self.vec_durations = None
        self.vec_pos_curves = None
        self.vec_rot_curves = None
        self.vec_pos_curve_ids = None
        self.vec_rot_curve_ids = None

        self.vec_output = None

        self.play_mode = play_mode

        super().__init__(skeleton, animations)

    def _initialize(self):
        self.vec_output = VectorizedArray.create_transform_matrix_vector(
            self.nb_anims * self.nb_joints
        )

        self.vec_durations = Animation.animations_as_duration_vector(self.animations)
        self.vec_durations = self.vec_durations.repeat(self.nb_joints)

        lst_pos_curve_ids = []
        self.lst_vec_pos_curves = []
        for anim_id in range(self.nb_anims):
            for curve in self.animations[anim_id].position_curves:
                if curve.is_empty():
                    continue
                pos_curve_id = curve.id + anim_id * self.nb_joints
                if curve.is_constant():
                    self.vec_output[pos_curve_id][:3, 3] = curve.get_constant_value()
                else:
                    # 2 or more keys => requires interpolation
                    lst_pos_curve_ids.append(pos_curve_id)
                    self.lst_vec_pos_curves.append(curve.to_vectorized_array())

        self.vec_pos_curve_ids = VectorizedArray(
            array=np.array(lst_pos_curve_ids, dtype=np.int32),
            labels=["curve_id"],
        )

        lst_rot_curve_ids = []
        self.lst_vec_rot_curves = []
        for anim_id in range(self.nb_anims):
            for curve in self.animations[anim_id].rotation_curves:
                if curve.is_empty():
                    continue
                rot_curve_id = curve.id + anim_id * self.nb_joints
                if curve.is_constant():
                    self.vec_output[rot_curve_id][:3, :3] = quaternionToRotationMatrix(
                        quaternion.from_float_array(curve.get_constant_value())
                    )
                else:
                    # 2 or more keys => requires interpolation
                    lst_rot_curve_ids.append(rot_curve_id)
                    self.lst_vec_rot_curves.append(curve.to_vectorized_array())

        self.vec_rot_curve_ids = VectorizedArray(
            array=np.array(lst_rot_curve_ids, dtype=np.int32),
            labels=["curve_id"],
        )

        self.vec_pos_curves = self.vectorize_lst_curve_vectors(self.lst_vec_pos_curves)
        self.vec_rot_curves = self.vectorize_lst_curve_vectors(self.lst_vec_rot_curves)

    # @profile
    def _execute(self):
        lst_output = []
        nb_transforms = self.nb_joints * self.nb_anims

        vec_delta_transform_matrices = self.vec_output
        vec_delta_transform_matrices.set_labels(["delta_local_transform"])

        vec_anim_times = self.real_to_anim_time(self.time, self.vec_durations)

        arr_pos_addends = (
            np.arange(1).repeat(len(self.vec_pos_curve_ids)) * nb_transforms
        )
        arr_pos_curve_ids = self.vec_pos_curve_ids.get()
        arr_pos_curve_ids += arr_pos_addends

        arr_rot_addends = (
            np.arange(1).repeat(len(self.vec_rot_curve_ids)) * nb_transforms
        )
        arr_rot_curve_ids = self.vec_rot_curve_ids.get()
        arr_rot_curve_ids += arr_rot_addends
        arr_anim_times = vec_anim_times.get()
        vec_pos_anim_times = VectorizedArray(arr_anim_times[arr_pos_curve_ids])
        vec_rot_anim_times = VectorizedArray(arr_anim_times[arr_rot_curve_ids])

        # COMPUTATION
        vec_pos_prev_keys, vec_pos_next_keys = self.get_prev_next_key(
            vec_pos_anim_times, self.vec_pos_curves
        )

        vec_position_interpolation_ratios = self.compute_interpolation_ratio(
            vec_pos_anim_times, vec_pos_prev_keys, vec_pos_next_keys
        )
       
        vec_delta_position = self.interpolate_position_linear(
            vec_pos_prev_keys, vec_pos_next_keys, vec_position_interpolation_ratios
        )

        vec_rot_prev_keys, vec_rot_next_keys = self.get_prev_next_key(
            vec_rot_anim_times, self.vec_rot_curves
        )

        vec_rotation_interpolation_ratios = self.compute_interpolation_ratio(
            vec_rot_anim_times, vec_rot_prev_keys, vec_rot_next_keys
        )

        vec_delta_rotation = self.interpolate_quaternion_linear(
            vec_rot_prev_keys, vec_rot_next_keys, vec_rotation_interpolation_ratios
        )

        vec_delta_transform_matrices[arr_pos_curve_ids, :3, 3] = vec_delta_position

        vec_delta_transform_matrices[arr_rot_curve_ids, :3, :3] = (
            quaternionToRotationMatrix(vec_delta_rotation.get())
        )

        lst_output.append(vec_delta_transform_matrices)
        return lst_output

    @staticmethod
    def vectorize_lst_curve_vectors(
        curve_vectors: List[VectorizedArray],
    ) -> VectorizedArray:
        max_len = max([len(curve_vector) for curve_vector in curve_vectors])
        for curve_vector in curve_vectors:
            while len(curve_vector) < max_len:
                curve_vector._array = np.vstack(
                    [curve_vector._array, curve_vector._array[-1]]
                )

        return VectorizedArray(array=np.array(curve_vectors), labels=["curve_vectors"])

    # @profile
    def real_to_anim_time(
        self, real_time: float, vec_durations: VectorizedArray
    ) -> VectorizedArray:
            
        if self.play_mode == PlayMode.NO_LOOP:
            arr_anim_time = real_time / vec_durations.get()
            arr_anim_time = np.clip(arr_anim_time, 0, 1)
            vec_anim_time = VectorizedArray(array=arr_anim_time, labels=["anim_time"])
            return vec_anim_time
    
        elif self.play_mode == PlayMode.WAIT_THEN_LOOP:
            real_time = real_time % vec_durations.get().max()
            arr_anim_time = real_time / vec_durations.get()
            arr_anim_time = np.clip(arr_anim_time, 0, 1)
            if np.allclose(arr_anim_time, 1.0, atol=1e-5):
                arr_anim_time = real_time / vec_durations.get() % 1.0            
            vec_anim_time = VectorizedArray(array=arr_anim_time, labels=["anim_time"])
            return vec_anim_time
        
        elif self.play_mode == PlayMode.LOOP_ALL:
            arr_anim_time = real_time / vec_durations.get() % 1.0
            vec_anim_time = VectorizedArray(array=arr_anim_time, labels=["anim_time"])
            return vec_anim_time


    @staticmethod
    # @profile
    def get_prev_next_key(
        vec_anim_times: VectorizedArray, curve_vectors: VectorizedArray
    ) -> Tuple[VectorizedArray, VectorizedArray]:
        # Make a new 2D vectorized array that only contains the first column of each curve_vector
        arr_curve_times = curve_vectors[:, :, 0]

        # Reshape the anim_times to match the shape of vec_curve_times
        arr_anim_times = np.tile(
            vec_anim_times.get().reshape(-1, 1), (1, arr_curve_times.shape[1])
        )

        # Subtract the two arrays
        arr_diff = arr_curve_times - arr_anim_times

        # Add 2 to negative values
        arr_diff[arr_diff <= 0] += 2

        # Find the indices of the first positive value in each row
        arr_next_keys_id = np.argmin(arr_diff, axis=1)

        arr_prev_keys_id = arr_next_keys_id - 1

        prev_keys = curve_vectors[np.arange(len(arr_prev_keys_id)), arr_prev_keys_id]
        next_keys = curve_vectors[np.arange(len(arr_next_keys_id)), arr_next_keys_id]

        vec_prev_keys = VectorizedArray(array=prev_keys, labels=["prev_keys"])

        vec_next_keys = VectorizedArray(array=next_keys, labels=["next_keys"])

        return vec_prev_keys, vec_next_keys

    @staticmethod
    def compute_interpolation_ratio(
        vec_anim_times: VectorizedArray,
        vec_prev_keys: VectorizedArray,
        vec_next_keys: VectorizedArray,
    ) -> VectorizedArray:
        prev_key_times = vec_prev_keys[:, 0]
        next_key_times = vec_next_keys[:, 0]
        return VectorizedArray(
            array=(vec_anim_times.get() - prev_key_times)
            / (next_key_times - prev_key_times),
            labels=["interpolation_ratio"],
        )

    @staticmethod
    def interpolate_position_linear(
        vec_prev_keys: VectorizedArray,
        vec_next_keys: VectorizedArray,
        vec_interpolation_ratio: VectorizedArray,
    ) -> VectorizedArray:
        return VectorizedArray(
            array=vec_prev_keys.get()[:, 1:]
            + vec_interpolation_ratio.get().reshape(-1, 1)
            * (vec_next_keys.get()[:, 1:] - vec_prev_keys.get()[:, 1:]),
            labels=["delta_pos_x", "delta_pos_y", "delta_pos_z"],
        )

    @staticmethod
    def interpolate_quaternion_linear(
        vec_prev_keys: VectorizedArray,
        vec_next_keys: VectorizedArray,
        vec_interpolation_ratio: VectorizedArray,
    ) -> VectorizedArray:
        prev_values = quaternion.as_quat_array(vec_prev_keys.get()[:, 1:])
        next_values = quaternion.as_quat_array(vec_next_keys.get()[:, 1:])
        return VectorizedArray(
            array=quaternion.slerp(
                prev_values, next_values, 0, 1, vec_interpolation_ratio.get()
            ),
            labels=["delta_q_w", "delta_q_x", "delta_q_y", "delta_q_z"],
        )
