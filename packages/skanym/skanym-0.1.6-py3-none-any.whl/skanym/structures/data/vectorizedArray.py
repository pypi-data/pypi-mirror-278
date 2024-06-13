import numpy as np


class VectorizedArray:
    def __init__(self, array, labels=None):
        if not isinstance(array, np.ndarray):
            raise ValueError("Input must be a NumPy ndarray")
        self._array = array

        self._labels = labels
        if self._labels is None:
            if self._array.ndim == 1:
                self._labels = ["col_0"]
            else:
                self._labels = [f"col_{i}" for i in range(self._array.shape[1])]

    @classmethod
    def copy(cls, vectorized_array):
        return cls(
            array=np.copy(vectorized_array.get()),
            labels=vectorized_array.get_labels().copy(),
        )

    def get(self):
        return self._array

    def tile(self, n_tuple):
        tiled_vectorized_array = VectorizedArray.copy(self)
        tiled_vectorized_array._array = np.tile(self._array, n_tuple)
        return tiled_vectorized_array

    def repeat(self, n):
        repeated_vectorized_array = VectorizedArray.copy(self)
        repeated_vectorized_array._array = np.repeat(self._array, n, axis=0)
        return repeated_vectorized_array
    
    def pop(self, index):
        popped_value = self._array[index]
        self._array = np.delete(self._array, index, axis=0)
        return popped_value

    def get_labels(self):
        return self._labels

    def set_labels(self, labels):
        self._labels = labels

    def validate_shape(self, expected_shape):
        if self._array.shape != expected_shape:
            raise ValueError(
                f"Expected shape {expected_shape} but got {self._array.shape}"
            )

    @staticmethod  
    def create_transform_matrix_vector(N: int) -> "VectorizedArray":
        return VectorizedArray(
            array=np.tile(np.eye(4), (N, 1, 1)), labels=["transform_matrix"]
        )

    def __len__(self):
        return self._array.shape[0]

    def __str__(self):
        str_value = ""
        str_value += str(self._labels) + "\n"
        str_value += str(self._array) + "\n"
        str_value += str(self._array.shape) + "\n"
        return str_value

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        self._array[key] = value
