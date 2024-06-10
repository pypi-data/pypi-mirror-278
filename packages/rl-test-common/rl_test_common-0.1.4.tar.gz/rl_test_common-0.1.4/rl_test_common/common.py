import os

from .singleton_meta import SingletonMeta


class Common(metaclass=SingletonMeta):
    def get_type(self, obj: object) -> str:
        return type(obj).__name__

    def clear_screen(self) -> None:
        if os.name == 'nt':
            os.system('cls')

        else:
            os.system('clear')
