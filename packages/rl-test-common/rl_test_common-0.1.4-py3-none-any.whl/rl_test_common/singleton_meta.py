from threading import Lock
from typing import Any


class SingletonMeta(type):
    __instances: dict = {}

    __lock: Lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self.__lock:
            if self not in self.__instances:
                instance: Any = super().__call__(*args, **kwargs)
                self.__instances[self] = instance

        return self.__instances[self]
