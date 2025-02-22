from enum import Enum
from random import choice


class BaseEnum(Enum):
    """Класс модифицирующий Enum класс."""

    @classmethod
    def get_random_item(cls) -> "BaseEnum":
        """Получаем случайный пол."""
        return choice([item for item in cls])