from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.upload_repository import (
    UploadRepository
)
from app.services.upload_service import (
    UploadService
)
from app.config.aws import s3_client, AWS_S3_BUCKET


router = APIRouter()


def get_upload_service(
    db: Session = Depends(get_db)
):

    repository = UploadRepository(db)

    return UploadService(repository)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    # service: UploadService = Depends(
    #     get_upload_service
    # )
):

    try:

        # saved_file = await service.upload_file(
        #     file
        # )

        s3_key = f"uploads/{file.filename}"

        s3_client.upload_fileobj(
            file.file,
            AWS_S3_BUCKET,
            s3_key,
            ExtraArgs={"ContentType": file.content_type}
        )

        return {
            "message": "File uploaded successfully",
            # "id": saved_file.id,
            # "filename": saved_file.filename,
            # "content_type": saved_file.content_type,
            # "file_size": saved_file.file_size
            "filename": file.filename,
            "s3_key": s3_key
        }

    except ValueError as e:

        raise HTTPException(
            # status_code=400,
            # detail=str(e)
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )