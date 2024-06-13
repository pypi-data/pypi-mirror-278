# Write a method using the skanym package that takes as arguments a skeleton and an animation and removes
# all the joints for the fingers and their corresponding keyframes from the animation.

from typing import List, Tuple

from skanym.structures.animation.animation import Animation
from skanym.structures.character.skeleton import Skeleton
from skanym.structures.character.joint import Joint

def remove_fingers(skeleton: Skeleton, animation: Animation = None) -> Tuple[Skeleton, Animation]:
    """
    """
    # List of joints keywords to remove
    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky', 'finger', 'toe_end']

    joint_list = skeleton.as_joint_list()

    # joints to remove
    joints_to_remove = []

    for joint_id in range(len(joint_list)):
        j = joint_list[joint_id]
        for finger in fingers:
            if finger in j.name.lower() and j.parent is not None:
                j.parent.remove_child(j)
                joints_to_remove.append(joint_id)

    if animation is None:
        return skeleton, None

    # Remove curves for the joints to remove
    animation.position_curves = [curve for curve in animation.position_curves if curve.id not in joints_to_remove]
    animation.rotation_curves = [curve for curve in animation.rotation_curves if curve.id not in joints_to_remove] 

    # update joint ids in curves
    for j_id in range(len(skeleton.as_joint_list())):
        animation.position_curves[j_id].id = j_id
        animation.rotation_curves[j_id].id = j_id

    return skeleton, animation