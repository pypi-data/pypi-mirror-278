import numpy as np

class Key:

    def __init__(self, time, value):
        """**Default constructor for the Key class.**

        Parameters:
        ----------
        time : int or float
            The time of the key.
        value : any
            The values of the key at a given time.
        """
        self.time = time
        self.value = value

    def as_array(self) -> np.ndarray:
        """Returns the key as a numpy array.

        Returns:
        ----------
        np.ndarray
            The key as a numpy array.
        """
        return np.array([self.time, *self.value])
        
    def __repr__(self) -> str:
        """Returns the string representation of the key.

        Returns:
        ----------
        str
            The string representation of the key.
        """
        return f"Key({self.time}, {self.value})"