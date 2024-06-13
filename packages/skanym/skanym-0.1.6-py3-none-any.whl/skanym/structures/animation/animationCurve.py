
import numpy as np

from skanym.structures.animation.iCurve import ICurve

class AnimationCurve:
    def __init__(self, curve: ICurve = None, id: int = None):
        self.curve = curve
        self.id = id

    def is_empty(self):
        return self.curve.is_empty()
    
    def is_constant(self):
        return self.curve.is_constant()
    
    def get_constant_value(self):
        return self.curve.get_constant_value()
    
    def to_vectorized_array(self):
        return self.curve.to_vectorized_array()

    

