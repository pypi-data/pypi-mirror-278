from abc import ABC, abstractmethod

import numpy as np
import quaternion

class ITransform(ABC):
    """
    Interface for transform objects.
    """

    @abstractmethod
    def getPosition(self) -> np.ndarray:
        """
        Returns the position of the transform.
        """
        pass

    @abstractmethod
    def getRotation(self) -> np.quaternion:
        """
        Returns the rotation of the transform.
        """
        pass

    @abstractmethod
    def getTransformMatrix(self) -> np.ndarray:
        """
        Returns the transform matrix.
        """
        pass
    
    @abstractmethod
    def getRotationMatrix(self) -> np.ndarray:
        """
        Returns the rotation matrix.
        """
        pass