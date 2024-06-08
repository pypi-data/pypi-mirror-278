from typing import Any

from flowi.utilities.singleton import Singleton


class GlobalState(metaclass=Singleton):
    def __init__(self):
        self._state = dict()

    def set(self, key: str, value: Any):
        self._state[key] = value

    def get(self, key: str):
        return self._state[key]
