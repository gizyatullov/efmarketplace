from pydantic import Field

__all__ = [
    "ForPaginationFields",
]


class ForPaginationFields:
    total = Field(description="Total items in the selection.", example=101)
    page = Field(description="Current page.", example=2)
    size = Field(description="Requested number of items per page.", example=10)
