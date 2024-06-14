from enum import Enum


class CGCEntityList(Enum):
    """Base class for other lists"""

    @classmethod
    def get_list(cls) -> list[str]:
        return [el.value for el in cls]
