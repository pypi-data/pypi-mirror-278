import os
import time
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

from skanym.structures.animation.animation import Animation
from skanym.models.inputFormatter import InputFormatter
from skanym.loaders.objectLoader import ObjectLoader
from skanym.models.baseVae import BaseVAE
from skanym.structures.network.vae import VAE


class CVAE(BaseVAE):
    def __init__(
        self,
        input_formatter: InputFormatter,
        latent_dim,
        features_dim,
        train_split=0.8,
        batch_size=3,
        epochs=10,
        beta=0.1,
        init_learning_rate=1e-4,
        no_summary=False,
    ):
        self.latent_dim = latent_dim
        self.features_dim = features_dim
        self.input_formatter = input_formatter

        self.train_split = train_split
        self.batch_size = batch_size
        self.epochs = epochs
        self.beta = beta
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            init_learning_rate, decay_steps=4000, decay_rate=0.96, staircase=True
        )

        self.learning_rate = lr_schedule
        self.optimizer = tf.keras.optimizers.Adam(self.learning_rate)

        self.raw_data = self.input_formatter.simulateFk()
        self.scaled_data = self.input_formatter.scaleInputData(self.raw_data)
        self.raw_features = self.input_formatter.extractFeatures(
            nb_features=self.features_dim
        )
        self.scaled_features = self.input_formatter.scaleInputFeatures(
            self.raw_features
        )
        self.labelised_data = self.input_formatter.labeliseData(
            self.scaled_data, self.scaled_features
        )
        print(f"Labelised data shape: {self.labelised_data.shape}")

        self.model = VAE(
            self.labelised_data.shape[1:], self.latent_dim, self.features_dim
        )
        if not no_summary:
            self.model.encoder.summary()
            self.model.decoder.summary()

    def preprocess(self):
        train_size = int(self.labelised_data.shape[0] * self.train_split)
        test_size = self.labelised_data.shape[0] - train_size

        train_anims = self.labelised_data[:train_size]
        test_anims = self.labelised_data[train_size:]

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

    def compute_loss(self, x):
        mean, logvar = self.model.encode(x)
        z = self.model.reparameterize(mean, logvar)
        z_extended = tf.concat([z, x[:, 0, -self.features_dim :]], axis=1)

        x_logit = self.model.decode(z_extended)

        mse = tf.reduce_sum(
            tf.square(x[:, :, : -self.features_dim] - x_logit), axis=[1, 2]
        )

        mean_extended = tf.concat([mean, x[:, 0, -self.features_dim :]], axis=1)

        logvar_extended = tf.concat(
            [
                logvar,
                tf.constant(
                    0.0, dtype=tf.float32, shape=(logvar.shape[0], self.features_dim)
                ),
            ],
            axis=1,
        )

        kl_divergence = -0.5 * tf.reduce_sum(
            1 + logvar - tf.square(mean) - tf.exp(logvar),
            axis=1,
        )

        # Calculate the total loss
        total_loss = tf.reduce_mean(mse + self.beta * kl_divergence)

        return total_loss

    def generate(self, features: np.ndarray) -> Animation:
        mean_vector = tf.zeros((1, self.latent_dim))
        logvar_vector = tf.zeros((1, self.latent_dim))
        latent_vector = self.model.reparameterize(mean_vector, logvar_vector)
        # latent_vector = tf.concat([latent_vector, features], axis=1) # Which makes more sense?
        latent_vector = tf.concat([mean_vector, features], axis=1)
        generated_input = self.model.sample(latent_vector)
        rescaled_input = self.input_formatter.scaleInputData(
            generated_input, inverse=True
        )
        return self._anim_from_vector(rescaled_input[0])

    def regenerate(self, id: int, verbose: bool = False):
        mean, logvar = self.model.encode(self.labelised_data[id : id + 1])
        if verbose:
            print(
                f"Regenerating {self.input_formatter.animator.animations[id].name} with mean: {mean} and logvar: {logvar}"
            )
            print(f"Features: {self.scaled_features[id]}")
        return self.generate(self.scaled_features[id : id + 1]), mean, logvar
