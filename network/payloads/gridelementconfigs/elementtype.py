from enum import IntEnum

class ElementType(IntEnum):
    NODE = 1,
    POINT = 2,
    SEGMENT = 3,
    CONVERTER = 4,
    BREAKER = 5,
    FENSWITCHGEAR = 6
    SOURCE = 7
    SCIBREAKBREAKER = 8