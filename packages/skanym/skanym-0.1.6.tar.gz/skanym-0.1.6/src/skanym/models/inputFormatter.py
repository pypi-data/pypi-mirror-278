# Class to manage the formatting of input data for the VAE model.

# Steps:
# 1. Load skeleton and animation data from FBX files.
# 2. Extract relevant data from the file names.
# 3. Simulate forward kinematics to generate input data.
# 4a. -
# 4b. Introduce conditional parameters to the input data.
# 5. Scale input data.

from typing import List

import numpy as np
import quaternion
from sklearn.preprocessing import MinMaxScaler

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.animators.baseFkAnimator import BaseFkAnimator
from skanym.utils import conversion
from skanym.utils.animationUtils import normalizeAnimDuration


class InputFormatter:

    def __init__(
        self,
        skeleton: Skeleton,
        animations: List[Animation],
        nb_frames: int,
    ):
        self.nb_frames = nb_frames
        self.sampling_times = np.linspace(0, 1, self.nb_frames)
        normalizeAnimDuration(animations, 1.0)
        self.animator = BaseFkAnimator(skeleton, animations)

        self.input_data_scaler = MinMaxScaler()
        self.input_features_scaler = MinMaxScaler()

    def scaleInputData(self, data, inverse=False):
        original_shape = data.shape

        data = np.reshape(data, (original_shape[0], -1))

        if not inverse:
            data = self.input_data_scaler.fit_transform(data)
        else:
            data = self.input_data_scaler.inverse_transform(data)

        return np.reshape(data, (-1, original_shape[1], original_shape[2]))

    def scaleInputFeatures(self, features, inverse=False):
        if not inverse:
            features = self.input_features_scaler.fit_transform(features)
        else:
            features = self.input_features_scaler.inverse_transform(features)

        return features

    def labeliseData(self, data, features):
        features = np.reshape(features, (features.shape[0], 1, features.shape[1]))
        # repeat over axis 1 to match the number of frames
        features = np.repeat(features, data.shape[1], axis=1)
        return np.concatenate((data, features), axis=2)

    def simulateFk(self):
        self.animator.time = 0.0

        arr_delta_transform_matrices = np.empty((0, 4, 4))
        frame_0_data = self.animator.step(0)[0].get()
        arr_delta_transform_matrices = np.append(
            arr_delta_transform_matrices, frame_0_data, axis=0
        )

        for i in range(self.nb_frames - 1):
            frame_data = self.animator.step(1 / (self.nb_frames - 1))[0].get()
            arr_delta_transform_matrices = np.append(
                arr_delta_transform_matrices, frame_data, axis=0
            )

        arr_delta_positions = arr_delta_transform_matrices[:, :3, 3]
        arr_delta_rotations = quaternion.as_float_array(
            conversion.rotationMatrixToQuaternion(
                arr_delta_transform_matrices[:, :3, :3]
            )
        )

        neg_arr_delta_rotations = arr_delta_rotations[:, 0] < 0
        arr_delta_rotations[neg_arr_delta_rotations] *= -1

        input_data = np.concatenate((arr_delta_positions, arr_delta_rotations), axis=1)
        # Here in "input_data" is organized as follows :
        # - All rows contain values for these 7 dofs : [pos_x, pos_y, pos_z, q_w, q_x, q_y, q_z]
        # - Rows are organized first by joint, then by animation, then by frame :
        # [j0_a0_f0, j1_a0_f0, ..., jN_a0_f0, j0_a1_f0, j1_a1_f0, ..., jN_a1_f0, ..., jN_aN_f0, j0_a0_f1, ...]

        nb_pose = self.animator.nb_joints * self.animator.nb_anims

        # STEP 1 : separate by animation
        indices = (
            np.arange(nb_pose * self.nb_frames)
            .reshape(self.nb_frames, nb_pose)
            .T.ravel()
        )
        input_data = input_data[indices]
        input_data = input_data.reshape(
            (self.animator.nb_anims, -1, input_data.shape[1])
        ).astype(np.float32)

        # STEP 2 : separate by frame
        input_data = input_data.reshape(
            (self.animator.nb_anims, self.animator.nb_joints, -1, input_data.shape[2])
        ).astype(np.float32)
        input_data = (
            np.swapaxes(input_data, 1, 2)
            .reshape((self.animator.nb_anims, self.nb_frames, -1))
            .astype(np.float32)
        )
        # Here in "input_data" is organized as follows :
        # - first dimension : animation
        # - second dimension : frame
        # - third dimension : pose (7dof for j0, 7dof for j1, ..., 7dof for jN)

        # STEP 3 : remove position for non root joints
        base_indices = np.arange(0, 7)
        indices = np.arange(7, self.animator.nb_joints * 7)
        indices = indices[indices % 7 != 0]
        indices = indices[indices % 7 != 1]
        indices = indices[indices % 7 != 2]
        indices = np.concatenate([base_indices, indices])

        input_data = input_data[:, :, indices]

        return input_data

    def extractFeatures(self, nb_features = 3) -> np.ndarray:
        """
        Specific to 1 type of input data.
        """
        # remove non numeric and underscore characters from animation names
        anim_name_copy = [anim.name for anim in self.animator.animations]
        for anim in self.animator.animations:
            anim.name = "".join([c for c in anim.name if c.isnumeric() or c == "_"])
            anim.name = anim.name[1:]
        input_features = np.array(
            [anim.name.split("_") for anim in self.animator.animations]
        ).astype(np.float32)
        current_nb_features = input_features.shape[1]
        # while the number of features is less than the desired number of features, add a copy of the initial array
        while current_nb_features < nb_features:
            input_features = np.concatenate((input_features, input_features), axis=1)
            current_nb_features = input_features.shape[1]

        for anim, name in zip(self.animator.animations, anim_name_copy):
            anim.name = name

        return input_features[:, :nb_features]
