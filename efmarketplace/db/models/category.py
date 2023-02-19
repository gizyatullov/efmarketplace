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

    class Meta:
        table = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"Category ({self.name})"
