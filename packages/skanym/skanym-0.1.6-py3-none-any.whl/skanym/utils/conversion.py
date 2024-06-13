import numpy as np
import quaternion

VALIDATION_DICT = {
    "positionToTransformMatrix": {
        "arg_name": "positions", "row_shape" : (3,), "dtype" : [np.float32, np.float64]},
    "transformMatrixToPosition": {
        "arg_name": "transform_matrices", "row_shape" : (4,4), "dtype" : [np.float32, np.float64]},
    "quaternionToRotationMatrix": {
        "arg_name": "quaternions", "row_shape" : (1,), "dtype" : np.quaternion},
    "rotationMatrixToQuaternion": {
        "arg_name": "rotation_matrices", "row_shape" : (3,3), "dtype" : [np.float32, np.float64]}    
    }

def safe(func):
    """
    Decorator method to check the validity of the input before conversion.
    """
    def wrapper(*args, **kwargs):
        # Get name of the function
        func_name = func.__name__
        # Get the input argument name
        arg_name = VALIDATION_DICT[func_name]["arg_name"]
        # Get the input argument value
        if args:
            arg_value = args[0]
        else:
            arg_value = kwargs[arg_name]
        # Get the row size of the input argument
        row_shape = VALIDATION_DICT[func_name]["row_shape"]
        # Get the data type of the input argument
        dtypes = VALIDATION_DICT[func_name]["dtype"]

        # Check the validity of the input argument
        if arg_value.ndim == 1:
            # If a single position is provided, convert it to a 2D array
            arg_value = np.expand_dims(arg_value, axis=0)
        if arg_value.shape[1:] != row_shape:
            expected_shape = (arg_value.shape[0],) + row_shape
            error_msg = f"Input {arg_name} array must have shape {row_shape} or {expected_shape} not {arg_value.shape}"
            raise ValueError(error_msg)
        if arg_value.dtype not in dtypes:
            error_msg = f"Input {arg_name} array must have data type {dtypes} not {arg_value.dtype}"
            raise ValueError(error_msg)  
             
        return func(*args, **kwargs)

    return wrapper

# @safe
def positionToTransformMatrix(positions):
    """
    Converts 3D positions transformation matrices.

    Parameters:
    - positions: NumPy array representing a single 3D position (shape: (3,))
                 or an array of 3D positions (shape: (n, 3))

    Returns:
    - transform_matrices: NumPy array representing transformation matrices
                          (shape: (n, 4, 4) for an array of positions, or (4, 4) for a single position)
    """
    if positions.ndim == 1:
        # If a single position is provided, convert it to a 2D array
        positions = np.expand_dims(positions, axis=0)

    # if positions.shape[1] != 3:
    #     raise ValueError("Input positions array must have shape (n, 3) or (3,)")

    # Create a 4x4 identity matrix for each position
    transform_matrices = np.tile(np.eye(4), (positions.shape[0], 1, 1))

    # Set the translation components in the transformation matrices
    transform_matrices[:, :3, 3] = positions

    return transform_matrices

# @safe
def transformMatrixToPosition(transform_matrices):
    """
    Converts transformation matrices to 3D positions.

    Parameters:
    - transform_matrices: NumPy array representing transformation matrices
                          (shape: (n, 4, 4))

    Returns:
    - positions: NumPy array representing 3D positions (shape: (n, 3))
    """
    # if transform_matrices.ndim != 3 or transform_matrices.shape[1:] != (4, 4):
    #     raise ValueError("Input transform_matrices array must have shape (n, 4, 4)")]
    
    return transform_matrices[:, :3, 3]

# @safe
def quaternionToRotationMatrix(quaternions):
    """
    Converts quaternions to rotation matrices.

    Parameters:
    - quaternions: NumPy array representing quaternions (shape: (n, 4))
    
    Returns:
    - rotation_matrices: NumPy array representing rotation matrices (shape: (n, 3, 3))
    """
    if quaternions.ndim == 0:
        # If a single quaternion is provided, convert it to a 2D array
        quaternions = np.expand_dims(quaternions, axis=0)
    
    # # Make a decorator class for validation
    # if quaternions.ndim != 2 or quaternions.shape[1] != 1:
    #     raise ValueError("Input quaternions array must have shape (n, 1)")
        
    # Assumes the quaternions are normalized
    m = np.empty(quaternions.shape + (3, 3))
    q = quaternion.as_float_array(quaternions)
    m[..., 0, 0] = 1.0 - 2*(q[..., 2]**2 + q[..., 3]**2)
    m[..., 0, 1] = 2*(q[..., 1]*q[..., 2] - q[..., 3]*q[..., 0])
    m[..., 0, 2] = 2*(q[..., 1]*q[..., 3] + q[..., 2]*q[..., 0])
    m[..., 1, 0] = 2*(q[..., 1]*q[..., 2] + q[..., 3]*q[..., 0])
    m[..., 1, 1] = 1.0 - 2*(q[..., 1]**2 + q[..., 3]**2)
    m[..., 1, 2] = 2*(q[..., 2]*q[..., 3] - q[..., 1]*q[..., 0])
    m[..., 2, 0] = 2*(q[..., 1]*q[..., 3] - q[..., 2]*q[..., 0])
    m[..., 2, 1] = 2*(q[..., 2]*q[..., 3] + q[..., 1]*q[..., 0])
    m[..., 2, 2] = 1.0 - 2*(q[..., 1]**2 + q[..., 2]**2)

    return m

# @safe
def rotationMatrixToQuaternion(rotation_matrices):
    """
    Converts rotation matrices to quaternions.

    Parameters:
    - rotation_matrices: NumPy array representing rotation matrices (shape: (n, 3, 3))

    Returns:
    - quaternions: NumPy array representing quaternions (shape: (n, 4))
    """
    if rotation_matrices.ndim == 2:
        # If a single rotation matrix is provided, convert it to a 3D array
        rotation_matrices = np.expand_dims(rotation_matrices, axis=0)
    
    # if rotation_matrices.ndim != 3 or rotation_matrices.shape[1:] != (3, 3):
    #     raise ValueError("Input rotation_matrices array must have shape (n, 3, 3)")
        
    rot = np.array(rotation_matrices, copy=False)
    shape = rot.shape[:-2]

    diagonals = np.empty(shape+(4,))
    diagonals[..., 0] = rot[..., 0, 0]
    diagonals[..., 1] = rot[..., 1, 1]
    diagonals[..., 2] = rot[..., 2, 2]
    diagonals[..., 3] = rot[..., 0, 0] + rot[..., 1, 1] + rot[..., 2, 2]

    indices = np.argmax(diagonals, axis=-1)

    q = diagonals  # reuse storage space
    indices_i = (indices == 0)
    if np.any(indices_i):
        if indices_i.shape == ():
            indices_i = Ellipsis
        rot_i = rot[indices_i, :, :]
        q[indices_i, 0] = rot_i[..., 2, 1] - rot_i[..., 1, 2]
        q[indices_i, 1] = 1 + rot_i[..., 0, 0] - rot_i[..., 1, 1] - rot_i[..., 2, 2]
        q[indices_i, 2] = rot_i[..., 0, 1] + rot_i[..., 1, 0]
        q[indices_i, 3] = rot_i[..., 0, 2] + rot_i[..., 2, 0]
    indices_i = (indices == 1)
    if np.any(indices_i):
        if indices_i.shape == ():
            indices_i = Ellipsis
        rot_i = rot[indices_i, :, :]
        q[indices_i, 0] = rot_i[..., 0, 2] - rot_i[..., 2, 0]
        q[indices_i, 1] = rot_i[..., 1, 0] + rot_i[..., 0, 1]
        q[indices_i, 2] = 1 - rot_i[..., 0, 0] + rot_i[..., 1, 1] - rot_i[..., 2, 2]
        q[indices_i, 3] = rot_i[..., 1, 2] + rot_i[..., 2, 1]
    indices_i = (indices == 2)
    if np.any(indices_i):
        if indices_i.shape == ():
            indices_i = Ellipsis
        rot_i = rot[indices_i, :, :]
        q[indices_i, 0] = rot_i[..., 1, 0] - rot_i[..., 0, 1]
        q[indices_i, 1] = rot_i[..., 2, 0] + rot_i[..., 0, 2]
        q[indices_i, 2] = rot_i[..., 2, 1] + rot_i[..., 1, 2]
        q[indices_i, 3] = 1 - rot_i[..., 0, 0] - rot_i[..., 1, 1] + rot_i[..., 2, 2]
    indices_i = (indices == 3)
    if np.any(indices_i):
        if indices_i.shape == ():
            indices_i = Ellipsis
        rot_i = rot[indices_i, :, :]
        q[indices_i, 0] = 1 + rot_i[..., 0, 0] + rot_i[..., 1, 1] + rot_i[..., 2, 2]
        q[indices_i, 1] = rot_i[..., 2, 1] - rot_i[..., 1, 2]
        q[indices_i, 2] = rot_i[..., 0, 2] - rot_i[..., 2, 0]
        q[indices_i, 3] = rot_i[..., 1, 0] - rot_i[..., 0, 1]

    q /= np.linalg.norm(q, axis=-1)[..., np.newaxis]

    return quaternion.as_quat_array(q)

def transformMatrixToQuaternion(transform_matrices):
    """
    Converts transformation matrices to quaternions.

    Parameters:
    - transform_matrices: NumPy array representing transformation matrices (shape: (n, 4, 4))

    Returns:
    - quaternions: NumPy array representing quaternions (shape: (n, 4))
    """
    rotation_matrices = transform_matrices[:, :3, :3]
    return rotationMatrixToQuaternion(rotation_matrices)

def quaternionFromAxisAngle(axis, angle):
    """
    Creates a quaternion from an axis and an angle.

    Parameters:
    - axis: NumPy array representing the axis (shape: (3,))
    - angle: Angle in radians

    Returns:
    - quaternion: NumPy array representing the quaternion (shape: (4,))
    """
    # Normalize the axis
    axis = axis / np.linalg.norm(axis)

    # Create the quaternion
    half_angle = angle / 2
    return np.quaternion(np.cos(half_angle), *np.sin(half_angle) * axis)

def positionAndQuaternionToTransformMatrix(positions, quaternions):
    """
    Converts 3D positions and quaternions to transformation matrices.

    Parameters:
    - positions: NumPy array representing 3D positions (shape: (n, 3))
    - quaternions: NumPy array representing quaternions (shape: (n, 4))

    Returns:
    - transform_matrices: NumPy array representing transformation matrices (shape: (n, 4, 4))
    """
    # Convert positions and quaternions to transformation matrices
    transform_matrices = positionToTransformMatrix(positions)
    rotation_matrices = quaternionToRotationMatrix(quaternions)
    transform_matrices[:, :3, :3] = rotation_matrices

    return transform_matrices

if __name__ == "__main__":
    # Test the conversion functions

    # Single input
    print("____Single input")

    position = np.array([-5., 0., 3.])
    transform_matrix = positionToTransformMatrix(position)
    print("Transform matrix:", transform_matrix)

    rotation = quaternion.quaternion(np.sqrt(2)/2, 0, 0, np.sqrt(2)/2)
    rotation_matrix = quaternionToRotationMatrix(rotation)
    print("Rotation matrix:", rotation_matrix)

    transform_matrix = np.eye(4)
    transform_matrix[:3, 3] = position
    transform_matrix[:3, :3] = rotation_matrix

    position = transformMatrixToPosition(transform_matrix)
    print("Position:", position)

    rotation = rotationMatrixToQuaternion(rotation_matrix)
    print("Rotation:", rotation)

    # Multiple inputs
    print("____Multiple input")
    
    positions = np.array([[-5., 0., 3.], [0., 1., 2.]])
    transform_matrices = positionToTransformMatrix(positions)
    print("Transform matrices:", transform_matrices)

    rotations = np.array(
        [np.quaternion(np.sqrt(2)/2, 0, 0, np.sqrt(2)/2),
            np.quaternion(0, np.sqrt(2)/2, 0, np.sqrt(2)/2)],
        dtype=np.quaternion)
    rotation_matrices = quaternionToRotationMatrix(rotations)
    print("Rotation matrices:", rotation_matrices)

    transform_matrices = np.empty((2, 4, 4))
    transform_matrices[:, :3, 3] = positions
    transform_matrices[:, :3, :3] = rotation_matrices

    positions = transformMatrixToPosition(transform_matrices)
    print("Positions:", positions)

    rotations = rotationMatrixToQuaternion(rotation_matrices)
    print("Rotations:", rotations)

