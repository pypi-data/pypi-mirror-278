
from typing import List
from pathlib import Path
from abc import ABC, abstractmethod

from skanym.structures.character.skeleton  import Skeleton
from skanym.structures.animation.animation  import Animation

class IFileLoader(ABC):

    DEFAULT_FRAMERATE = 30

    def __init__(self, path: Path):
        self._path = path

    def set_path(self, path: Path):
        self._path = path

    @abstractmethod
    def load_skeleton(self) -> Skeleton:
        pass

    @abstractmethod
    def load_animation(self) -> Animation:
        pass

    @abstractmethod
    def load_animations(self) -> List[Animation]:
        pass


