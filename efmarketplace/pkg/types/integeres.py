from pydantic.types import ConstrainedInt

__all__ = [
    "PositiveIntWithZero",
    "CustPositiveInt",
]


class PositiveIntWithZero(ConstrainedInt):
    # no doc
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    ge = 0


class CustPositiveInt(ConstrainedInt):
    ge = 1
