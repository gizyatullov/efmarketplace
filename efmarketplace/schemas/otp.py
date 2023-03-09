from pydantic import Field

from .base import BaseModel
from .user import UserName

__all__ = [
    "OTPFields",
    "OTP",
    "SetOTPWithUserNameCommand",
    "UnplugOTPCommand",
    "UnplugOTPWithUserNameCommand",
]

from efmarketplace.pkg.types import NotEmptyStr

qr_otp_in_base64 = "iVBORw0KGgoAAAANSUhEUgAAAcIAAAHCAQAAAABUY/ToAAADoElEQVR4nO2cW4rkOgyGPx0H6jGBXkAvJdnBLOnQO4uX0gsYSB4HXPznwZck1TUcmOmiLkhQJkn5ww4ISZbsmPgzif/8IQhOOumkk0466aSTj0dakQ5YzWxazfIf+ao+yzLdebZOPiQ5SpIWMBuCoE+YDWcDgmzqE5oJkiQdyXvM1smHJNdiXzT3v0zz2sG4BAFn00zImlNM1d1n6+RDk+NnB/E9AWuHZshXNt1uTCefmuwu7o1eGHQQB0xxAuKEifW7xnTyNcle0gxozuF0EOMCjErY1CdsAiSl7xvTyZcio5mZDWD/LlV9cji9nsT4ecqRkZmVBduTvqeTNyDRFclmKducPkE2S8c+83O9p5O3I7MO5TXYuARpzl6tLMSkJYhRqfarV65DTjapulEb+pSjoJoQqupDn9Dcl36uQ05WyesyxWEB1rek+CMI1rccADHOQUa/AAQZ1HDoyd7TyduR1TO1JPSoRLFIhKNXA829+zInL6XGQzX22VwWx2ZcQi6HuC9z8ii1BBakuYZCRWnU1Ecte9Qn1yEnL2SnQ2qWpuQYw8EO5bJs8JjayQup+Z6WC2qWRkvxb9kEbW7M4yEnD7LF1CU/VKPrcrU0Rap5R9chJ49S9QVqdrqqT2lgC6c9P+TkFdn5slxkXZrm5Gc10Tj3yWNqJ69JC3BqIWMha9PeGPX7cNp1yMlrZByAaCfZRJA+hrKFEfpfVrucTR/D2Yrje8r3dPIGZK51GBiKPxbImpOfhWRwEqxdsnEZAIJsnO81WycfkfwSD21r+5ysbpmiUe3WfZmTe9l0aBc6X2QbAbZtjb62d/IKWY+WnYqlie8J4hCkmbPtNoXEAWy682ydfEQy5xjjeyrnOgC2DbFE69CHnWoe6VvGdPJVyP0eNGi7OxYoFXzC7t8sHg85eZB9rWOrcNTjGzmpWK681uHkNSlr+1Eg1rdk4/IGcQLof1a31v/s9lsY/3JMJ1+LvDzXse03Iy/J2m1LUbsvc/IKuX33o2w1Yx8Z5cUZa5fPod19tk4+JDlKLSFE/uSHTZSG+L4d+GhF/qd8TydvQO72U9eNi6ntPNs3pbvX7Z38P1L6PMmmdj8uZ6tnPQ7Zo4eYrZOPQH797kf+nXOjOIUE60A1RCHZ347p5GuRuxxjqZJpO1oGXxo/X+bkF6lKA5Si/D5PXZvapZ1gdB1ysko5K93uVbNC23MdurTo+rne00knnXTSSSeddPJ38h+SuH7F25wOtAAAAABJRU5ErkJggg=="


class OTPFields:
    otp = Field(
        description="OTP key-secret", example="DJ6OERKWPG4YMKOLPZ3ETMGVGG6GDOER"
    )
    qr = Field(description="QR image in base64", example=qr_otp_in_base64)
    otp_code = Field(description="Generated OTP code", example="519452")


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


class UnplugOTPCommand(BaseOTP):
    otp_code: NotEmptyStr = OTPFields.otp_code


class UnplugOTPWithUserNameCommand(UnplugOTPCommand, UserName):
    pass
