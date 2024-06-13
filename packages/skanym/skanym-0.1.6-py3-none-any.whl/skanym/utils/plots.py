from typing import List
from pathlib import Path

import numpy as np
import quaternion
import matplotlib.pyplot as plt


def barPlot(
    data: List[np.array],
    data_labels: List[str],
    labels: List[str] = None,
    title: str = "Bar Plot",
    ylabel: str = "Y",
    xlabel: str = "X",
):
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    x = np.arange(len(data_labels))
    width = 1 / (len(data) + 1)
    for i, d in enumerate(data):
        if labels is None:
            ax.bar(x + i * width, d, width, label=f"Serie {i}")
        else:
            ax.bar(x + i * width, d, width, label=f"{labels[i]}")
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(x)
    ax.set_xticklabels(data_labels)
    ax.legend()
    return fig


def plot3DLatentSpace(
    latent_space: np.array, log_var: np.array = None, labels: List[str] = None, title: str = "Latent Space"
):
    if log_var is None:
        fig = plt.figure()
        fig.suptitle(title)
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(latent_space[:, 0], latent_space[:, 1], latent_space[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        return fig
    else:
        mean = latent_space
        std = np.exp(log_var / 2)

        fig = plt.figure()
        fig.suptitle(title)
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(mean[:, 0], mean[:, 1], mean[:, 2])
        r = 15
        for i in range(latent_space.shape[0]):
            if labels is not None:
                ax.text(mean[i, 0], mean[i, 1], mean[i, 2], labels[i], color="black", alpha=0.4)
            u = np.linspace(0, 2 * np.pi, r)
            v = np.linspace(0, np.pi, r)
            x = std[i, 0] * np.outer(np.cos(u), np.sin(v)) + mean[i, 0]
            y = std[i, 1] * np.outer(np.sin(u), np.sin(v)) + mean[i, 1]
            z = std[i, 2] * np.outer(np.ones_like(u), np.cos(v)) + mean[i, 2]
            ax.plot_surface(x, y, z, color="b", alpha=0.02)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        return fig


if __name__ == "__main__":
    data_labels = [1, 2, 3, 5, 8, 16, 32]
    raw_pca_data = [0.1321, 0.1169, 0.0837, 0.0585, 0.0240, 0.0126, 0.0041]
    raw_vae_data = [0.0903, 0.0248, 0.0158, 0.0149, 0.0141, 0.0093, 0.0084]

    pca_data = np.degrees(raw_pca_data)
    vae_data = np.degrees(raw_vae_data)

    fig = barPlot(
        [pca_data, vae_data],
        data_labels,
        labels=["PCA", "VAE"],
        title="Local Rotation RMSE for animation reconstruction [°]",
        ylabel="RMSE",
        xlabel="Number of latent dimensions",
    )
    
    plt.show()