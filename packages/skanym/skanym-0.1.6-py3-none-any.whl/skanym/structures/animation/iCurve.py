from typing import List
from abc import ABC, abstractmethod

import numpy as np

from skanym.structures.animation.key import Key

class ICurve(ABC):
    """An interface for curve classes."""
    def __init__(self, keys: List[Key] = None):
        """**Default constructor for the PositionCurve class.**"""
        self.keys = []
        if keys is not None:
            for key in keys:
                self.add_key(key)
            
    def get_key_count(self) -> int:
        """Returns the number of keys in the animation curve.

        Returns:
        ----------
        int
            The number of keys in the animation curve.
        """
        return len(self.keys)

    # @profile
    def add_key(self, key: Key):       
        if not 0.0 <= key.time <= 1.0:
            raise ValueError(
                f"Invalid key time {key.time}. Key time must be between 0.0 and 1.0 inclusive."
            )
        
        # self.validate_key_value(key.value)  

        self.keys.append(key)
        self.keys.sort(key=lambda key: key.time)

    def is_empty(self) -> bool:
        """Returns whether the animation curve is empty.

        Returns:
        ----------
        bool
            Whether the animation curve is empty.
        """
        return len(self.keys) == 0
    
    def is_constant(self) -> bool:
        """Returns whether the animation curve is constant.

        Returns:
        ----------
        bool
            Whether the animation curve is constant.
        """
        return len(self.keys) == 1
    
    def get_constant_value(self) -> Key:
        """Returns the constant key of the animation curve.

        Returns:
        ----------
        Key
            The constant key of the animation curve.
        """
        if not self.is_constant():
            raise ValueError("The animation curve is not constant.")
        return self.keys[0].value

    @abstractmethod
    def as_array(self) -> np.ndarray:
        pass

