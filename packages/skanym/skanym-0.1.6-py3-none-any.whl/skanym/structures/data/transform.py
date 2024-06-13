import numpy as np
import quaternion

from skanym.structures.data.iTransform import ITransform
from skanym.utils import conversion

class Transform(ITransform):
    """
    Simple concrete transform class defined by a position and a rotation.
    """
    def __init__(
            self,
            position: np.ndarray = np.array([0.0, 0.0, 0.0]),
            rotation: np.quaternion = quaternion.one):
        """
        Constructor.
        """
        self.position = position
        self.rotation = rotation

    def getPosition(self):
        """
        Returns the position of the transform.
        """
        return self.position

    def getRotation(self):
        """
        Returns the rotation of the transform.
        """
        return self.rotation

    def getTransformMatrix(self):
        """
        Returns the transform matrix.
        """        
        return conversion.positionAndQuaternionToTransformMatrix(self.position, self.rotation)

    def getRotationMatrix(self):
        """
        Returns the rotation matrix.
        """
        return conversion.quaternionToRotationMatrix(self.rotation)

    def __str__(self):
        return "Position: " + str(self.getPosition()) + ", Rotation: " + str(self.getRotation())
    