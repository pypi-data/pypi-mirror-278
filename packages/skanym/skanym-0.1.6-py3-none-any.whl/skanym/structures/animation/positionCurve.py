import numpy as np

from skanym.structures.animation.iCurve import ICurve  
from skanym.structures.data.vectorizedArray import VectorizedArray  
  
class PositionCurve(ICurve):
    """
    """
    def to_vectorized_array(self):
        lst = [key.as_array() for key in self.keys]
        arr = np.array(lst)
        return VectorizedArray(array=arr, labels=["time", "x", "y", "z"])


    def as_array(self) -> np.ndarray:
        """Returns the animation curve as a numpy array.

        Returns:
        ----------
        np.ndarray
            The animation curve as a numpy array.
        """
        if self.get_key_count() == 0:
            return np.array([
                [0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0]])
        elif self.get_key_count() == 1:
            return np.array([
                [0.0, self.keys[0].value[0], self.keys[0].value[1], self.keys[0].value[2]],
                [1.0, self.keys[0].value[0], self.keys[0].value[1], self.keys[0].value[2]]])
        else:
            return np.array([[key.time, key.value[0], key.value[1], key.value[2]] for key in self.keys])