# Write a method using the skanym package that takes as arguments a skeleton and an animation and removes
# all the joints for the fingers and their corresponding keyframes from the animation.

from typing import List

from skanym.structures.animation.animation import Animation


def normalizeAnimDuration(
    animation: List[Animation] = None, duration: float = 1.0
) -> None:
    """
    Set the duration of all animation to the given time in second.
    Done in place.
    """
    if animation is None:
        return

    for anim in animation:
        anim.duration = duration
