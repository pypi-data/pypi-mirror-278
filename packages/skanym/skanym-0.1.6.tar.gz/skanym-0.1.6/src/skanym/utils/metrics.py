from typing import List
from pathlib import Path

import numpy as np
import quaternion
import matplotlib.pyplot as plt

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.structures.data.vectorizedArray import VectorizedArray
from skanym.animators.globalFkAnimator import GlobalFkAnimator
from skanym.loaders.assimpLoader import AssimpLoader
from skanym.utils import conversion


class PoseMetrics:
    """
    Class to compute various metrics for poses
    """

    def __init__(
        self,
        Y_pose: List[VectorizedArray],
        Y_hat_pose: List[VectorizedArray],
    ):
        self.Y_pose = Y_pose
        self.Y_hat_pose = Y_hat_pose

    def mseGlobalPosition(self):        
        return np.mean(np.square(self.Y_pose[2][:, :3, 3] - self.Y_hat_pose[2][:, :3, 3]))

    def mseLocalRotation(self):
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    conversion.transformMatrixToQuaternion(self.Y_pose[1]),
                    conversion.transformMatrixToQuaternion(self.Y_hat_pose[1]),
                )
            )
        )

    def mseSummary(self):
        print(f" - mseLocalRotation: {self.mseLocalRotation():.4f}")
        print(f" - mseGlobalPosition: {self.mseGlobalPosition():.4f}")

    def rmseSummary(self):
        print(f" - rmseLocalRotation: {np.sqrt(self.mseLocalRotation()):.4f}")
        print(f" - rmseGlobalPosition: {np.sqrt(self.mseGlobalPosition()):.4f}")


class AnimationMetrics:
    """
    Class to compute various metrics for animations
    """

    def __init__(
        self,
        skeleton: Skeleton,
        Y_anim: Animation,
        Y_hat_anim: Animation = None,
        frame_resolution: int = 30,
    ):
        self.frame_resolution = frame_resolution

        self.Y_animator = GlobalFkAnimator(skeleton, [Y_anim])
        self.Y_hat_animator = GlobalFkAnimator(skeleton, [Y_hat_anim])

        self._simulate_fk()

    def _simulate_fk(self):
        self.Y_delta_local_positions = np.empty((0, 3))
        self.Y_delta_local_rotations = np.empty((0,))
        self.Y_hat_delta_local_positions = np.empty((0, 3))
        self.Y_hat_delta_local_rotations = np.empty((0,))

        self.Y_local_positions = np.empty((0, 3))
        self.Y_local_rotations = np.empty((0,))
        self.Y_hat_local_positions = np.empty((0, 3))
        self.Y_hat_local_rotations = np.empty((0,))

        self.Y_global_positions = np.empty((0, 3))
        self.Y_global_rotations = np.empty((0,))
        self.Y_hat_global_positions = np.empty((0, 3))
        self.Y_hat_global_rotations = np.empty((0,))

        for i in np.linspace(0, 1, self.frame_resolution, endpoint=False):
            self.Y_animator.set_time(i)
            self.Y_hat_animator.set_time(i)
            Y_out = self.Y_animator.step()
            Y_hat_out = self.Y_hat_animator.step()

            self.Y_delta_local_positions = np.concatenate(
                [
                    self.Y_delta_local_positions,
                    conversion.transformMatrixToPosition(Y_out[0]),
                ],
                axis=0,
            )
            self.Y_delta_local_rotations = np.concatenate(
                [
                    self.Y_delta_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[0]),
                ],
                axis=0,
            )
            self.Y_hat_delta_local_positions = np.concatenate(
                [
                    self.Y_hat_delta_local_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[0]),
                ],
                axis=0,
            )
            self.Y_hat_delta_local_rotations = np.concatenate(
                [
                    self.Y_hat_delta_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[0]),
                ],
                axis=0,
            )

            self.Y_local_positions = np.concatenate(
                [
                    self.Y_local_positions,
                    conversion.transformMatrixToPosition(Y_out[1]),
                ],
                axis=0,
            )
            self.Y_local_rotations = np.concatenate(
                [
                    self.Y_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[1]),
                ],
                axis=0,
            )
            self.Y_hat_local_positions = np.concatenate(
                [
                    self.Y_hat_local_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[1]),
                ],
                axis=0,
            )
            self.Y_hat_local_rotations = np.concatenate(
                [
                    self.Y_hat_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[1]),
                ],
                axis=0,
            )

            self.Y_global_positions = np.concatenate(
                [
                    self.Y_global_positions,
                    conversion.transformMatrixToPosition(Y_out[2]),
                ],
                axis=0,
            )
            self.Y_global_rotations = np.concatenate(
                [
                    self.Y_global_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[2]),
                ],
                axis=0,
            )
            self.Y_hat_global_positions = np.concatenate(
                [
                    self.Y_hat_global_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[2]),
                ],
                axis=0,
            )
            self.Y_hat_global_rotations = np.concatenate(
                [
                    self.Y_hat_global_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[2]),
                ],
                axis=0,
            )

    def getLocalDeltaPositions(self):
        return self.Y_delta_local_positions

    def getLocalRotations(self):
        return self.Y_local_rotations

    def getGlobalPositions(self):
        return self.Y_global_positions

    def mseGlobalPosition(self):
        return np.mean(np.square(self.Y_global_positions - self.Y_hat_global_positions))

    def mseGlobalRotation(self):
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_global_rotations, self.Y_hat_global_rotations
                )
            )
        )

    def mseLocalPosition(self):
        return np.mean(np.square(self.Y_local_positions - self.Y_hat_local_positions))

    def mseLocalRotation(self):
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_local_rotations, self.Y_hat_local_rotations
                )
            )
        )

    def mseDeltaLocalPosition(self):
        return np.mean(
            np.square(self.Y_delta_local_positions - self.Y_hat_delta_local_positions)
        )

    def mseDeltaLocalRotation(self):
        """
        Mean squared error of delta local rotations, the error is the angle between the two quaternions
        """
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_delta_local_rotations, self.Y_hat_delta_local_rotations
                )
            )
        )

    def mseSummary(self):
        print(f" - mseLocalRotation: {self.mseLocalRotation():.4f}")
        print(f" - mseGlobalPosition: {self.mseGlobalPosition():.4f}")

    def rmseSummary(self):
        print(f" - rmseLocalRotation: {np.sqrt(self.mseLocalRotation()):.4f}")
        print(f" - rmseGlobalPosition: {np.sqrt(self.mseGlobalPosition()):.4f}")


class AnimationsMetrics:
    def __init__(
        self,
        skeleton: Skeleton,
        Y_anims: List[Animation],
        Y_hat_anims: List[Animation] = None,
        frame_resolution: int = 30,
    ):
        self.frame_resolution = frame_resolution

        self.Y_animator = GlobalFkAnimator(skeleton, Y_anims)
        self.Y_hat_animator = GlobalFkAnimator(skeleton, Y_hat_anims)

        self._simulate_fk()

    def _simulate_fk(self):
        self.Y_delta_local_positions = np.empty((0, 3))
        self.Y_delta_local_rotations = np.empty((0,))
        self.Y_hat_delta_local_positions = np.empty((0, 3))
        self.Y_hat_delta_local_rotations = np.empty((0,))

        self.Y_local_positions = np.empty((0, 3))
        self.Y_local_rotations = np.empty((0,))
        self.Y_hat_local_positions = np.empty((0, 3))
        self.Y_hat_local_rotations = np.empty((0,))

        self.Y_global_positions = np.empty((0, 3))
        self.Y_global_rotations = np.empty((0,))
        self.Y_hat_global_positions = np.empty((0, 3))
        self.Y_hat_global_rotations = np.empty((0,))

        for i in np.linspace(0, 1, self.frame_resolution, endpoint=False):
            self.Y_animator.set_time(i)
            self.Y_hat_animator.set_time(i)
            Y_out = self.Y_animator.step()
            Y_hat_out = self.Y_hat_animator.step()

            self.Y_delta_local_positions = np.concatenate(
                [
                    self.Y_delta_local_positions,
                    conversion.transformMatrixToPosition(Y_out[0]),
                ],
                axis=0,
            )
            self.Y_delta_local_rotations = np.concatenate(
                [
                    self.Y_delta_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[0]),
                ],
                axis=0,
            )
            self.Y_hat_delta_local_positions = np.concatenate(
                [
                    self.Y_hat_delta_local_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[0]),
                ],
                axis=0,
            )
            self.Y_hat_delta_local_rotations = np.concatenate(
                [
                    self.Y_hat_delta_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[0]),
                ],
                axis=0,
            )

            self.Y_local_positions = np.concatenate(
                [
                    self.Y_local_positions,
                    conversion.transformMatrixToPosition(Y_out[1]),
                ],
                axis=0,
            )
            self.Y_local_rotations = np.concatenate(
                [
                    self.Y_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[1]),
                ],
                axis=0,
            )
            self.Y_hat_local_positions = np.concatenate(
                [
                    self.Y_hat_local_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[1]),
                ],
                axis=0,
            )
            self.Y_hat_local_rotations = np.concatenate(
                [
                    self.Y_hat_local_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[1]),
                ],
                axis=0,
            )

            self.Y_global_positions = np.concatenate(
                [
                    self.Y_global_positions,
                    conversion.transformMatrixToPosition(Y_out[2]),
                ],
                axis=0,
            )
            self.Y_global_rotations = np.concatenate(
                [
                    self.Y_global_rotations,
                    conversion.transformMatrixToQuaternion(Y_out[2]),
                ],
                axis=0,
            )
            self.Y_hat_global_positions = np.concatenate(
                [
                    self.Y_hat_global_positions,
                    conversion.transformMatrixToPosition(Y_hat_out[2]),
                ],
                axis=0,
            )
            self.Y_hat_global_rotations = np.concatenate(
                [
                    self.Y_hat_global_rotations,
                    conversion.transformMatrixToQuaternion(Y_hat_out[2]),
                ],
                axis=0,
            )

    def getLocalDeltaPositions(self):
        return self.Y_delta_local_positions

    def getLocalRotations(self):
        return self.Y_local_rotations

    def getGlobalPositions(self):
        return self.Y_global_positions

    def mseGlobalPosition(self):
        return np.mean(np.square(self.Y_global_positions - self.Y_hat_global_positions))

    def mseGlobalRotation(self):
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_global_rotations, self.Y_hat_global_rotations
                )
            )
        )

    def mseLocalPosition(self):
        return np.mean(np.square(self.Y_local_positions - self.Y_hat_local_positions))

    def mseLocalRotation(self):
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_local_rotations, self.Y_hat_local_rotations
                )
            )
        )

    def mseDeltaLocalPosition(self):
        return np.mean(
            np.square(self.Y_delta_local_positions - self.Y_hat_delta_local_positions)
        )

    def mseDeltaLocalRotation(self):
        """
        Mean squared error of delta local rotations, the error is the angle between the two quaternions
        """
        return np.mean(
            np.square(
                quaternion.rotation_intrinsic_distance(
                    self.Y_delta_local_rotations, self.Y_hat_delta_local_rotations
                )
            )
        )

    def mseSummary(self):
        print(f" - mseLocalRotation: {self.mseLocalRotation():.4f}")
        print(f" - mseGlobalPosition: {self.mseGlobalPosition():.4f}")

    def rmseSummary(self):
        print(f" - rmseLocalRotation: {np.sqrt(self.mseLocalRotation()):.4f}")
        print(f" - rmseGlobalPosition: {np.sqrt(self.mseGlobalPosition()):.4f}")

    def meanDistanceSummary(self):
        matrix = self.getDistanceMatrix()
        print(f" - meanLocalRotationDistance: {np.mean(matrix[:, :, 0]):.4f}")
        print(f" - meanGlobalPositionDistance: {np.mean(matrix[:, :, 1]):.4f}")

    def getDistanceMatrix(self):
        """
        Compute the distance matrix
        """
        matrix = np.zeros(
            (len(self.Y_animator.animations), len(self.Y_animator.animations), 2)
        )

        nb_joints = self.Y_animator.nb_joints
        nb_anims = len(self.Y_animator.animations)
        pose_size = self.frame_resolution * nb_joints

        # Reorder the global positions
        self.Y_global_positions = np.reshape(
            self.Y_global_positions, (-1, nb_anims, nb_joints, 3)
        )
        self.Y_global_positions = np.swapaxes(self.Y_global_positions, 0, 1)
        self.Y_global_positions = np.reshape(self.Y_global_positions, (-1, 3))
        # Reorder the local rotations
        self.Y_local_rotations = np.reshape(
            self.Y_local_rotations, (-1, nb_anims, nb_joints)
        )
        self.Y_local_rotations = np.swapaxes(self.Y_local_rotations, 0, 1)
        self.Y_local_rotations = np.reshape(self.Y_local_rotations, (-1))

        for i in range(len(self.Y_animator.animations)):
            for j in range(len(self.Y_animator.animations)):
                local_rot = self.Y_local_rotations[i * pose_size : (i + 1) * pose_size]
                local_rot_hat = self.Y_local_rotations[
                    j * pose_size : (j + 1) * pose_size
                ]
                matrix[i, j, 0] = np.mean(
                    np.square(
                        quaternion.rotation_intrinsic_distance(local_rot, local_rot_hat)
                    )
                )
                global_pos = self.Y_global_positions[
                    i * pose_size : (i + 1) * pose_size
                ]
                global_pos_hat = self.Y_global_positions[
                    j * pose_size : (j + 1) * pose_size
                ]
                matrix[i, j, 1] = np.mean(np.square(global_pos - global_pos_hat))

        return matrix

    def plotDistanceMatrix(self, title="Distance matrix"):
        """
        Plot a distance matrix
        """

        matrix = self.getDistanceMatrix()

        local_rot_matrix = matrix[:, :, 0]
        global_pos_matrix = matrix[:, :, 1]

        # Plot local rotation matrix
        # Use animations names as labels
        plt.figure(figsize=(9, 9))
        plt.imshow(local_rot_matrix)
        plt.colorbar()
        plt.title("Local rotation " + title)
        plt.xticks(
            range(len(self.Y_animator.animations)),
            [a.name for a in self.Y_animator.animations],
            rotation=90,
        )
        plt.yticks(
            range(len(self.Y_hat_animator.animations)),
            [a.name for a in self.Y_hat_animator.animations],
        )
        # reverse the y-axis
        plt.gca().invert_yaxis()

        # Plot global position matrix
        plt.figure(figsize=(9, 9))
        plt.imshow(global_pos_matrix)
        plt.colorbar()
        plt.title("Global position " + title)
        plt.xticks(
            range(len(self.Y_animator.animations)),
            [a.name for a in self.Y_animator.animations],
            rotation=90,
        )
        plt.yticks(
            range(len(self.Y_hat_animator.animations)),
            [a.name for a in self.Y_hat_animator.animations],
        )
        # reverse the y-axis
        plt.gca().invert_yaxis()

        # plt.show()
