from tortoise import models, fields

__all__ = [
    'Category',
]


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255,
                            unique=True,
                            index=True)

    subcategories = fields.ReverseRelation['Subcategory']

    def __str__(self) -> str:
        return self.name
