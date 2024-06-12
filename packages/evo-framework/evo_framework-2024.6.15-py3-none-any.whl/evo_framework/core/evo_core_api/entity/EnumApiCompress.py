from enum import Enum

class EnumApiCompress(Enum):
    NONE = 0
    GZIP = 1
    LZ4 = 2
    ZIP = 3