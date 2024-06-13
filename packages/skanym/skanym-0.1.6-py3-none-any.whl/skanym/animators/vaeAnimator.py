# Data:
# 1. root joint position as vector (x, y, z)
# 2. all joints rotation as quaternion (w, x, y, z)
# repeat for each frame
# 2D array of shape (n_sample, n_frame * (3 + 4 * n_joint)),

import os
from typing import List, Tuple

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Disable Tensorflow warnings

import numpy as np
import quaternion
import tensorflow as tf

from skanym.structures.character.skeleton import Skeleton
from skanym.structures.animation.animation import Animation
from skanym.animators.baseFkAnimator import BaseFkAnimator, PlayMode
from skanym.animators.localFkAnimator import LocalFkAnimator
from skanym.loaders.objectLoader import ObjectLoader
from skanym.models.baseVae import BaseVAE
from skanym.models.conditionalVae import CVAE
from skanym.models.inputFormatter import InputFormatter


class VaeAnimator(BaseFkAnimator):
    """"""

    def __init__(
        self,
        skeleton: Skeleton,
        animations: List[Animation],        
        latent_dim: int,
        nb_frames: int,
        model_path: str = None,
    ):
        self.nb_frames = nb_frames
        self.latent_dim = latent_dim
        self.vae_values = np.zeros((1, self.latent_dim))
        self.sampling_times = np.linspace(0, 1, self.nb_frames)
        self.model_path = model_path

        self.vec_bind_transform_matrices = None
        self.vec_parent_ids = None
        super().__init__(skeleton, animations)

    def set_vae_values(self, vae_values: np.ndarray):
        self.vae_values[0] = vae_values

    def _initialize(self):
        if self.model_path is not None:
            # self.model = BaseVAE.load(self.model_path)
            self.model = CVAE.load(self.model_path)
        else:
            input_formatter = InputFormatter(
                self.skeleton, self.animations, self.nb_frames
            )

            self.model = CVAE(
                latent_dim=self.latent_dim, features_dim=3, input_formatter=input_formatter, epochs=600
            )
            self.model.train()
        
        self.nb_anims = 1

    def _execute(self):
        mean = tf.convert_to_tensor(self.vae_values, dtype=tf.float32)
        self.anim = self.model.generate(mean)
        self.anim.name = "Generated"
        animator = LocalFkAnimator(self.skeleton, [self.anim])
        animator.set_time(self.time)
        output_lst = animator.step(0.0)      
        return output_lst
