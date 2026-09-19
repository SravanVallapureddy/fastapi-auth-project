from datetime import datetime, timedelta
import random

from app.repositories.otp_repository import OTPRepository


class OTPService:

    def __init__(self, repository: OTPRepository):
        self.repository = repository

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self, phone_number: str):

        # 1. Generate OTP
        otp = self.generate_otp()

        # 2. OTP valid for 5 minutes
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        # 3. Save OTP
        self.repository.create_otp(
            phone_number=phone_number,
            otp=otp,
            expires_at=expires_at
        )

        # In real application:
        # SMS provider would be called here.
        #
        # sms_provider.send(
        #     phone_number,
        #     f"Your OTP is {otp}"
        # )

        return {
            "message": "OTP sent successfully"
        }

    def verify_otp(
        self,
        phone_number: str,
        otp: str
    ):

        # 1. Get OTP from database
        otp_record = self.repository.get_latest_otp(
            phone_number
        )

        # 2. OTP doesn't exist
        if not otp_record:
            raise ValueError("OTP not found")

        # 3. Check expiration
        if datetime.utcnow() > otp_record.expires_at:
            raise ValueError("OTP expired")

        # 4. Check OTP value
        if otp_record.otp != otp:
            raise ValueError("Invalid OTP")

        # 5. Mark OTP as verified
        self.repository.mark_as_verified(
            otp_record
        )

        return {
            "message": "OTP verified successfully"
        }