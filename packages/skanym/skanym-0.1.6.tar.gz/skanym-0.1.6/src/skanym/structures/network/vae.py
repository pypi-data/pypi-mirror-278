import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU usage
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable OneDNN optimizations
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Disable Tensorflow warnings

import tensorflow as tf
from tensorflow.keras import layers


class VAE(tf.keras.Model):
    """Variational Autoencoder model"""

    def __init__(self, input_shape, latent_dim, feature_dim=0, **kwargs):
        super(VAE, self).__init__()
        self.input_shape = input_shape
        self.output_shape = (input_shape[0], input_shape[1] - feature_dim)
        self.latent_dim = latent_dim
        self.feature_dim = feature_dim
        # intermediate_dim = max(latent_dim * 2, 64)
        intermediate_dim = 64
        self.encoder = tf.keras.Sequential(
            [
                layers.InputLayer(shape=self.input_shape),
                layers.Flatten(),
                # layers.Dense(intermediate_dim, activation="leaky_relu"),
                # layers.Dropout(0.32),
                # layers.Dense(latent_dim + latent_dim, activation="leaky_relu"),                
                layers.Dense(intermediate_dim, activation="leaky_relu"),
                layers.Dropout(0.32),
                layers.Dense(latent_dim + latent_dim),
            ]
        )
        self.decoder = tf.keras.Sequential(
            [
                layers.InputLayer(shape=(latent_dim + feature_dim,)),
                # layers.Dropout(0.16),
                # layers.Dense(
                    # units=(latent_dim + feature_dim), activation=tf.nn.leaky_relu
                # ),
                
                layers.Dense(units=intermediate_dim, activation=tf.nn.leaky_relu),
                layers.Dropout(0.16),
                layers.Dense(units=(self.output_shape[0] * self.output_shape[1])),
                layers.Reshape(
                    target_shape=(self.output_shape[0], self.output_shape[1])
                ),
            ]
        )

    @tf.function
    def sample(self, eps=None):
        if eps is None:
            eps = tf.random.normal(shape=(100, self.latent_dim))
        return self.decode(eps)

    def encode(self, x):
        mean, logvar = tf.split(self.encoder(x), num_or_size_splits=2, axis=1)
        return mean, logvar

    def reparameterize(self, mean, logvar):
        eps = tf.random.normal(shape=mean.shape)
        return eps * tf.exp(logvar * 0.5) + mean

    def decode(self, z):
        logits = self.decoder(z)
        return logits

    def get_config(self):
        base_config = super().get_config()
        config = {
            "input_shape": self.input_shape,
            "output_shape": self.output_shape,
            "latent_dim": self.latent_dim,
            "feature_dim": self.feature_dim,
        }
        return {**base_config, **config}

    @classmethod
    def from_config(cls, config):
        return cls(**config)
