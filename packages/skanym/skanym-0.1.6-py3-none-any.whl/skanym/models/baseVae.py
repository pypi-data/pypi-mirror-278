import os
import sys
from typing import List, Tuple
from pathlib import Path
from copy import deepcopy
import pickle

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU usage
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable OneDNN optimizations
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Disable Tensorflow warnings

import numpy as np
import quaternion
import tensorflow as tf
from tensorflow.keras import layers, models

from skanym.models.inputFormatter import InputFormatter
from skanym.structures.animation.animation import Animation
from skanym.structures.animation.animationCurve import AnimationCurve
from skanym.structures.animation.positionCurve import PositionCurve
from skanym.structures.animation.quaternionCurve import QuaternionCurve
from skanym.structures.animation.key import Key
from skanym.loaders.objectLoader import ObjectLoader
from skanym.structures.network.vae import VAE


class BaseVAE:
    def __init__(
        self,
        input_formatter: InputFormatter,
        latent_dim,
        train_split=0.8,
        batch_size=3,
        epochs=10,
        beta=0.1,
        init_learning_rate=1e-4,
        no_summary=False,
    ):
        self.latent_dim = latent_dim
        self.input_formatter = input_formatter

        self.train_split = train_split
        self.batch_size = batch_size
        self.epochs = epochs
        self.beta = beta
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            init_learning_rate, decay_steps=1000, decay_rate=0.96, staircase=True
        )

        self.learning_rate = lr_schedule
        self.optimizer = tf.keras.optimizers.Adam(self.learning_rate)

        self.raw_data = self.input_formatter.simulateFk()
        self.scaled_data = self.input_formatter.scaleInputData(self.raw_data)

        self.model = VAE(self.scaled_data.shape[1:], self.latent_dim)
        if not no_summary:
            self.model.encoder.summary()
            self.model.decoder.summary()

        # OH ok scaled data is used instead of labelised data

    def preprocess(self):
        train_size = int(self.scaled_data.shape[0] * self.train_split)
        test_size = self.scaled_data.shape[0] - train_size

        train_anims = self.scaled_data[:train_size]
        test_anims = self.scaled_data[train_size:]

        train_dataset = (
            tf.data.Dataset.from_tensor_slices(train_anims)
            .take(train_size)
            .shuffle(train_size)
            .batch(self.batch_size)
        )
        test_dataset = (
            tf.data.Dataset.from_tensor_slices(test_anims)
            .take(test_size)
            .shuffle(test_size)
            .batch(self.batch_size)
        )

        return train_dataset, test_dataset

    def train(self, verbose=True):
        # Training
        train_dataset, test_dataset = self.preprocess()

        for epoch in range(1, self.epochs + 1):
            train_loss = tf.keras.metrics.Mean()
            for train_x in train_dataset:
                train_loss(self.train_step(train_x))
            train_elbo = -train_loss.result()

            val_loss = tf.keras.metrics.Mean()
            for test_x in test_dataset:
                val_loss(self.compute_loss(test_x))
            elbo = -val_loss.result()
            if verbose:
                print_rate = 5000
                refresh_rate = 10
                if epoch % refresh_rate == 0:
                    new_text = f"Epoch: {epoch}/{self.epochs}, Train loss: {train_elbo:.3f}, Val loss: {elbo:.3f}, lrate: {self.optimizer.learning_rate:.5f}"
                    if epoch % print_rate == 0:
                        print("\r" + new_text)
                    else:
                        sys.stdout.write("\r" + new_text)
                        sys.stdout.flush()

    def log_normal_pdf(self, sample, mean, logvar, raxis=1):
        log2pi = tf.math.log(2.0 * np.pi)
        return tf.reduce_sum(
            -0.5 * ((sample - mean) ** 2.0 * tf.exp(-logvar) + logvar + log2pi),
            axis=raxis,
        )

    def compute_loss(self, x):
        mean, logvar = self.model.encode(x)
        z = self.model.reparameterize(mean, logvar)
        x_logit = self.model.decode(z)

        # Compute the MSE reconstruction loss
        mse = tf.reduce_sum(tf.square(x - x_logit), axis=[1, 2])

        # Compute the KL divergence
        kl_divergence = -0.5 * tf.reduce_sum(
            1 + logvar - tf.square(mean) - tf.exp(logvar), axis=1
        )

        # Calculate the total loss
        total_loss = tf.reduce_mean(mse + self.beta * kl_divergence)

        return total_loss

    @tf.function
    def train_step(self, x):
        with tf.GradientTape() as tape:
            loss = self.compute_loss(x)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return loss

    def generate(
        self, mean_vector: np.ndarray, logvar_vector: np.ndarray
    ) -> np.ndarray:
        latent_vector = self.model.reparameterize(mean_vector, logvar_vector)
        generated_input = self.model.sample(latent_vector)
        rescaled_input = self.input_formatter.scaleInputData(
            generated_input, inverse=True
        )
        return self._anim_from_vector(rescaled_input[0])

    def generate_random(self) -> np.ndarray:
        random_mean = tf.random.normal(shape=(1, self.latent_dim))
        random_logvar = tf.random.normal(shape=(1, self.latent_dim))
        return self.generate(random_mean, random_logvar)

    def regenerate(self, id: int, verbose: bool = False) -> np.ndarray:
        mean, logvar = self.model.encode(self.scaled_data[id : id + 1])
        if verbose:
            print(
                f"Regenerating {self.input_formatter.animator.animations[id].name} with mean: {mean} and logvar: {logvar}"
            )
        return self.generate(mean, logvar), mean, logvar

    def _anim_from_vector(self, v: np.ndarray) -> Animation:

        root_pos_x = v[:, 0]
        root_pos_y = v[:, 1]
        root_pos_z = v[:, 2]

        arr_rot_w = v[:, 3::4]
        arr_rot_x = v[:, 4::4]
        arr_rot_y = v[:, 5::4]
        arr_rot_z = v[:, 6::4]

        arr_pos = np.stack((root_pos_x, root_pos_y, root_pos_z), axis=1)
        arr_rot = np.stack((arr_rot_w, arr_rot_x, arr_rot_y, arr_rot_z), axis=2)

        # Quaternion array of shape (nb_frames, nb_joints, 4)
        # Verify that all quaternion are positive
        neg_arr_rot = arr_rot[:, :, 0] < 0
        arr_rot[neg_arr_rot] *= -1

        # Make sure all quaternions are normalized
        for i in range(arr_rot.shape[0]):
            for j in range(arr_rot.shape[1]):
                arr_rot[i, j] /= np.linalg.norm(arr_rot[i, j])

        p_anim_curves = []
        r_anim_curves = []

        for j_idx in range(self.input_formatter.animator.nb_joints):
            p_keys = []
            r_keys = []
            for t_idx in range(self.input_formatter.nb_frames):
                if j_idx == 0:
                    p_keys.append(
                        Key(self.input_formatter.sampling_times[t_idx], arr_pos[t_idx])
                    )

                r_keys.append(
                    Key(
                        self.input_formatter.sampling_times[t_idx],
                        arr_rot[t_idx, j_idx],
                    )
                )

            p_curve = PositionCurve(p_keys)
            p_anim_curves.append(AnimationCurve(p_curve, j_idx))

            r_curve = QuaternionCurve(r_keys)
            r_anim_curves.append(AnimationCurve(r_curve, j_idx))

        return Animation(position_curves=p_anim_curves, rotation_curves=r_anim_curves)

    def save(self, path_stem: str):
        save_path = path_stem + ".pkl"
        self.model_path = path_stem + "_layers.keras"
        self.model.save(self.model_path)
        self.model = None
        self.optimizer = None

        with open(save_path, "wb") as f:
            pickle.dump(self, f)
        self.model = tf.keras.models.load_model(path_stem + "_layers.keras")
        self.optimizer = tf.keras.optimizers.Adam(self.learning_rate)

    @staticmethod
    def load(path_stem: str):
        with open(path_stem + ".pkl", "rb") as f:
            model = pickle.load(f)

        model.model = tf.keras.models.load_model(path_stem + "_layers.keras")
        model.optimizer = tf.keras.optimizers.Adam(model.learning_rate)
        return model
