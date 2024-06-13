
import numpy as np

from skanym.core.animate.curve.iCurve import ICurve
  
class ScalarCurve(ICurve):
    """
    """
    def as_array(self) -> np.ndarray:
        """Returns the animation curve as a numpy array.

        Returns:
        ----------
        np.ndarray
            The animation curve as a numpy array.
        """
        if self.get_key_count() == 0:
            return np.array([
                [0.0, 0.0],
                [1.0, 1.0]])
        elif self.get_key_count() == 1:
            return np.array([
                [0.0, self.keys[0].value],
                [self.keys[0].time, self.keys[0].value],
                [1.0, self.keys[0].value]])
        else:
            return np.array([[key.time, key.value] for key in self.keys])