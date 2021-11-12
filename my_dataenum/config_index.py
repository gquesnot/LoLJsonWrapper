import enum


@enum.unique
class ConfigIndex(int, enum.Enum):
    KEY = 0
    ID = 1
    NAME = 2
