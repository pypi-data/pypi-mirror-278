import pickle
from pathlib import Path

class ObjectLoader:
    def __init__(self, path: Path):
        self._path = path

    def set_path(self, path: Path):
        self._path = path

    def load(self) -> object:
        with open(self._path, "rb") as f:
            return pickle.load(f)
        
    def save(self, obj: object):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "wb") as f:
            pickle.dump(obj, f)