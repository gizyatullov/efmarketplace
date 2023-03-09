from pydantic import Field

from .base import BaseModel
from .user import UserName

__all__ = [
    "OTPFields",
    "OTP",
    "SetOTPWithUserNameCommand",
]

from efmarketplace.pkg.types import NotEmptyStr


class OTPFields:
    otp = Field(description="OTP key", example="")
    qr = Field(description="QR image in base64", example="")


class BaseOTP(BaseModel):
    """Base model for OTP."""

    class Config:
        orm_mode = True


class OTP(BaseOTP):
    otp: NotEmptyStr = OTPFields.otp
    qr: NotEmptyStr = OTPFields.qr
    type_qr_image: NotEmptyStr = "png"


# Command
class SetOTPCommand(BaseOTP):
    pass


class SetOTPWithUserNameCommand(BaseOTP, UserName):
    pass


class UpdateOTPCommand(BaseOTP):
    otp: NotEmptyStr = OTPFields.otp
