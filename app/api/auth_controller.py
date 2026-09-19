from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.otp import (
    SendOTPRequest,
    VerifyOTPRequest,
    OTPResponse
)

from app.repositories.otp_repository import OTPRepository
from app.services.otp_service import OTPService


router = APIRouter()


def get_otp_service(
    db: Session = Depends(get_db)
):

    repository = OTPRepository(db)

    return OTPService(repository)


@router.post(
    "/send-otp",
    response_model=OTPResponse
)
def send_otp(
    request: SendOTPRequest,
    service: OTPService = Depends(get_otp_service)
):

    try:

        return service.send_otp(
            request.phone_number
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/verify-otp",
    response_model=OTPResponse
)
def verify_otp(
    request: VerifyOTPRequest,
    service: OTPService = Depends(get_otp_service)
):

    try:

        return service.verify_otp(
            request.phone_number,
            request.otp
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )