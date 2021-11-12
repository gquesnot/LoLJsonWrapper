import enum


@enum.unique
class TraitType(str, enum.Enum):
    ORIGIN = "origin"
    CLASS = "class"
