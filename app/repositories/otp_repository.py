from sqlalchemy.orm import Session

from app.models.otp import OTP


class OTPRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_otp(
        self,
        phone_number: str,
        otp: str,
        expires_at
    ):
        otp_record = OTP(
            phone_number=phone_number,
            otp=otp,
            expires_at=expires_at
        )

        self.db.add(otp_record)
        self.db.commit()
        self.db.refresh(otp_record)

        return otp_record

    def get_latest_otp(
        self,
        phone_number: str
    ):
        return (
            self.db.query(OTP)
            .filter(
                OTP.phone_number == phone_number,
                OTP.is_verified == False
            )
            .order_by(OTP.created_at.desc())
            .first()
        )

    def mark_as_verified(
        self,
        otp_record: OTP
    ):
        otp_record.is_verified = True

        self.db.commit()
        self.db.refresh(otp_record)

        return otp_record