import numpy as np

from skanym.structures.data.iTransform import ITransform
from skanym.utils import conversion

class TransformMatrix(ITransform):
    """
    Concrete Transform class defined only by its transform matrix.
    """
    def __init__(self, transformMatrix: np.ndarray = np.identity(4)):
        """
        Constructor.
        """
        self.transformMatrix = transformMatrix

    def getPosition(self):
        """
        Returns the position of the transform.
        """
        return conversion.transformMatrixToPosition(self.transformMatrix)

    def getRotation(self):
        """
        Returns the rotation of the transform.
        """
        return conversion.rotationMatrixToQuaternion(self.getRotationMatrix())

    def getTransformMatrix(self):
        """
        Returns the transform matrix.
        """
        return self.transformMatrix

    def getRotationMatrix(self):
        """
        Returns the rotation matrix.
        """
        return self.transformMatrix[0:3, 0:3]

    def __str__(self):
        return "Position: " + str(self.getPosition()) + ", Rotation: " + str(self.getRotation())