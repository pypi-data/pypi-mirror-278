import numpy as np

from skanym.structures.animation.iCurve import ICurve  
from skanym.structures.data.vectorizedArray import VectorizedArray 
  
class QuaternionCurve(ICurve):
    """
    """
    def to_vectorized_array(self):
        lst = [key.as_array() for key in self.keys]
        arr = np.array(lst)
        return VectorizedArray(array=arr, labels=["time", "w", "x", "y", "z"])

    def as_array(self) -> np.ndarray:
        """Returns the animation curve as a numpy array.

        Returns:
        ----------
        np.ndarray
            The animation curve as a numpy array.
        """
        if self.get_key_count() == 0:
            return np.array([
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0, 0.0]])
        elif self.get_key_count() == 1:
            return np.array([
                [0.0, self.keys[0].value.w, self.keys[0].value.x, self.keys[0].value.y, self.keys[0].value.z],
                [1.0, self.keys[0].value.w, self.keys[0].value.x, self.keys[0].value.y, self.keys[0].value.z]])
        else:
            return np.array([[key.time, key.value.w, key.value.x, key.value.y, key.value.z] for key in self.keys])