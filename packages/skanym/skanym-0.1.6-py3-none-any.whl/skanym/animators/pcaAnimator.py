from typing import List

import numpy as np
import quaternion
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from line_profiler import profile

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.animation.animationCurve import AnimationCurve
from skanym.structures.animation.positionCurve import PositionCurve
from skanym.structures.animation.quaternionCurve import QuaternionCurve
from skanym.structures.animation.key import Key
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.animators.baseFkAnimator import BaseFkAnimator
from skanym.utils import conversion


class PcaAnimator(BaseFkAnimator):
    """ """

    def __init__(
        self,
        skeleton: Skeleton,
        animations: List[Animation],
        nb_components: int,
        nb_frames: int,
    ):
        self.nb_components = nb_components
        self.nb_frames = nb_frames
        self.pca_values = np.full(self.nb_components, 0.5)
        self.sampling_times = np.linspace(0, 1, self.nb_frames)

        self.vec_bind_transform_matrices = None
        self.vec_parent_ids = None
        super().__init__(skeleton, animations)

    def set_pca_values(self, pca_values: np.ndarray):
        self.pca_values = pca_values

    # @profile
    def _initialize(self):
        input_data = self._simulate_fk()

        input_data = input_data.reshape((self.nb_anims, -1, input_data.shape[1]))
        input_data = input_data.reshape((-1, input_data.shape[1] * input_data.shape[2]))
        # PCA
        self.input_scaler = StandardScaler()
        self.output_scaler = MinMaxScaler()
        self.model = PCA(n_components=self.nb_components)

        scaled_input_data = self.input_scaler.fit_transform(input_data)
        output_data = self.model.fit_transform(scaled_input_data)
        self.scaled_output_data = self.output_scaler.fit_transform(output_data)

        self.vec_parent_ids = self.skeleton.as_parent_id_vector()

        self.nb_anims = 1

    # @profile
    def _execute(self):
        rescaled_values = self.output_scaler.inverse_transform(
            self.pca_values.reshape(1, -1)
        )
        generated_input = self.model.inverse_transform(rescaled_values)
        rescaled_input = self.input_scaler.inverse_transform(generated_input)   

        arr_pos_x = rescaled_input[:, 0::7]
        arr_pos_y = rescaled_input[:, 1::7]
        arr_pos_z = rescaled_input[:, 2::7]

        arr_rot_w = rescaled_input[:, 3::7]
        arr_rot_x = rescaled_input[:, 4::7]
        arr_rot_y = rescaled_input[:, 5::7]
        arr_rot_z = rescaled_input[:, 6::7]

        arr_pos = np.stack((arr_pos_x, arr_pos_y, arr_pos_z), axis=2)
        arr_rot = np.stack((arr_rot_w, arr_rot_x, arr_rot_y, arr_rot_z), axis=2)

        arr_pos = arr_pos.reshape(arr_pos.shape[1], arr_pos.shape[2])
        arr_rot = arr_rot.reshape(arr_rot.shape[1], arr_rot.shape[2])
        
        # Re normalize quaternions
        norms = np.linalg.norm(arr_rot, axis=1)
        arr_rot = arr_rot / norms[:, np.newaxis]

        arr_key_times = np.tile(self.sampling_times, self.nb_joints)
        arr_pos_key = np.concatenate(
            (arr_key_times.reshape(-1, 1), arr_pos), axis=1
        )
        arr_rot_key = np.concatenate(
            (arr_key_times.reshape(-1, 1), arr_rot), axis=1
        )

        arr_pos_key = arr_pos_key.reshape(self.nb_joints, self.nb_frames, 4)
        arr_rot_key = arr_rot_key.reshape(self.nb_joints, self.nb_frames, 5)

        vec_pos_curve = VectorizedArray(arr_pos_key, labels=["pos_curve"])
        vec_rot_curve = VectorizedArray(arr_rot_key, labels=["rot_curve"])

        vec_anim_times = self.real_to_anim_time(self.time, self.vec_durations)
        vec_anim_times._array = vec_anim_times[0:self.nb_joints]

        # COMPUTATION
        vec_pos_prev_keys, vec_pos_next_keys = self.get_prev_next_key(
            vec_anim_times, vec_pos_curve
        )

        vec_position_interpolation_ratios = self.compute_interpolation_ratio(
            vec_anim_times, vec_pos_prev_keys, vec_pos_next_keys
        )

        vec_delta_position = self.interpolate_position_linear(
            vec_pos_prev_keys, vec_pos_next_keys, vec_position_interpolation_ratios
        )

        vec_rot_prev_keys, vec_rot_next_keys = self.get_prev_next_key(
            vec_anim_times, vec_rot_curve
        )

        vec_rotation_interpolation_ratios = self.compute_interpolation_ratio(
            vec_anim_times, vec_rot_prev_keys, vec_rot_next_keys
        )

        vec_delta_rotation = self.interpolate_quaternion_linear(
            vec_rot_prev_keys, vec_rot_next_keys, vec_rotation_interpolation_ratios
        )

        vec_delta_transform_matrices = VectorizedArray.create_transform_matrix_vector(
           1 * self.nb_joints
        )

        vec_delta_transform_matrices[:, :3, 3] = vec_delta_position

        vec_delta_transform_matrices[:, :3, :3] = conversion.quaternionToRotationMatrix(
            vec_delta_rotation.get()
        )

        lst_output = [vec_delta_transform_matrices]

        arr_local_transform_matrices = self.vec_bind_transform_matrices.get() @ vec_delta_transform_matrices.get()

        vec_local_transform_matrices = VectorizedArray(arr_local_transform_matrices, labels=["local_transform"])

        lst_output.append(vec_local_transform_matrices)

        arr_local_transform_matrices = vec_local_transform_matrices.get()
        arr_global_transform_matrices = np.copy(arr_local_transform_matrices)
        for i in range(self.nb_joints):
            parent_id = self.vec_parent_ids[i]
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

    def _simulate_fk(self):
        for anim in self.animations:
            anim.duration = 1.0
        super()._initialize()
        self.vec_bind_transform_matrices = self.skeleton.as_bind_transform_vector()

        # Input data generation
        real_time = self.time # To avoid losing the original time if set before _initialize

        vec_delta_transform_matrices = VectorizedArray.create_transform_matrix_vector(
            self.nb_joints * self.nb_anims * self.nb_frames
        )
        for sample_time_id in range(self.nb_frames):
            sample_time = self.sampling_times[sample_time_id]
            self.set_time(sample_time)
            start_idx = sample_time_id * self.nb_joints * self.nb_anims
            end_idx = (sample_time_id + 1) * self.nb_joints * self.nb_anims
            vec_delta_transform_matrices[start_idx:end_idx, :, :] = super()._execute()[0]
        
        self.set_time(real_time)

        arr_delta_positions = vec_delta_transform_matrices[:, :3, 3]
        arr_delta_rotations = quaternion.as_float_array(
            conversion.rotationMatrixToQuaternion(
                vec_delta_transform_matrices[:, :3, :3]
            )
        )

        neg_arr_delta_rotations = arr_delta_rotations[:, 0] < 0
        arr_delta_rotations[neg_arr_delta_rotations] *= -1
        input_data = np.concatenate((arr_delta_positions, arr_delta_rotations), axis=1)

        nb_pose = self.nb_joints * self.nb_anims

        indices = (
            np.arange(nb_pose * self.nb_frames)
            .reshape(self.nb_frames, nb_pose)
            .T.ravel()
        )
        return input_data[indices]

    def _anim_from_vector(self, rescaled_input: np.ndarray) -> Animation:

        arr_pos_x = rescaled_input[:, 0::7]
        arr_pos_y = rescaled_input[:, 1::7]
        arr_pos_z = rescaled_input[:, 2::7]

        arr_rot_w = rescaled_input[:, 3::7]
        arr_rot_x = rescaled_input[:, 4::7]
        arr_rot_y = rescaled_input[:, 5::7]
        arr_rot_z = rescaled_input[:, 6::7]

        arr_pos = np.stack((arr_pos_x, arr_pos_y, arr_pos_z), axis=2)
        arr_rot = np.stack((arr_rot_w, arr_rot_x, arr_rot_y, arr_rot_z), axis=2)

        arr_pos = arr_pos.reshape(arr_pos.shape[1], arr_pos.shape[2])
        arr_rot = arr_rot.reshape(arr_rot.shape[1], arr_rot.shape[2])
        
        arr_rot = arr_rot / np.linalg.norm(arr_rot, axis=1)[:, np.newaxis]

        p_anim_curves = []
        r_anim_curves = []

        idx = 0
        for j_idx in range(self.nb_joints):
            p_keys = []
            r_keys = []
            for t_idx in range(self.nb_frames):
                p_keys.append(Key(self.sampling_times[t_idx], arr_pos[idx]))
                r_keys.append(Key(self.sampling_times[t_idx], arr_rot[idx]))
                idx += 1

            p_curve = PositionCurve(p_keys)
            r_curve = QuaternionCurve(r_keys)
            p_anim_curves.append(AnimationCurve(p_curve, j_idx))
            r_anim_curves.append(AnimationCurve(r_curve, j_idx))

        return Animation(position_curves=p_anim_curves, rotation_curves=r_anim_curves)