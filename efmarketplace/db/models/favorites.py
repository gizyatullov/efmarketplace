from tortoise import fields, models

from .user import User

__all__ = [
    "Favorites",
]


class Favorites(models.Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", related_name="favorites"
    )
    product_id = fields.IntField(index=True)

    class Meta:
        unique_together = (("user_id", "product_id"),)
        ordering = ["-id", ]

    def __str__(self) -> str:
        return f"Favorites {self.product_id}"
