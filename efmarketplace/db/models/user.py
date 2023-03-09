import bcrypt
import pyotp
from tortoise import fields, models

from efmarketplace import schemas

__all__ = [
    "User",
]


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True, index=True)
    password = fields.CharField(max_length=255)
    role_name = fields.CharEnumField(enum_type=schemas.UserRole)
    is_seller = fields.BooleanField(default=False)
    jwt_key = fields.CharField(max_length=255, null=True)
    btc_balance = fields.FloatField(null=True)
    btc_address = fields.CharField(max_length=255, null=True)
    otp = fields.CharField(max_length=255, null=True)
    city = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    is_banned = fields.BooleanField(default=False)
    user_ban_date = fields.DatetimeField(null=True)

    notification_statuses = fields.ReverseRelation["NotificationStatus"]

    class Meta:
        table = "users"
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"User ({self.username}) ({self.role_name})"

    async def set_password(self, password: str) -> None:
        password_bytes = password.encode("utf-8")
        self.password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    async def check_password(self, password: str) -> bool:
        password_bytes = password.encode("utf-8")
        hashed_bytes = self.password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    async def set_otp(self) -> str:
        k = pyotp.random_base32()
        self.otp = k
        return k

    async def check_otp(self, code: str) -> bool:
        totp = pyotp.TOTP(self.otp)
        return totp.verify(code)

    async def unplug_otp(self) -> None:
        self.otp = None
