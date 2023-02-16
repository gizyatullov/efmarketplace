from tortoise import models, fields

from .category import Category

__all__ = [
    'Subcategory',
]


class Subcategory(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255,
                            unique=True,
                            index=True)
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        model_name='models.Category',
        related_name='subcategories')

    def __str__(self) -> str:
        return self.name
