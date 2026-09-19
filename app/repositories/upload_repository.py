from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile


class UploadRepository:

    def __init__(self, db: Session):

        self.db = db

    def save_file(
        self,
        filename: str,
        content_type: str,
        file_size: int,
        file_data: bytes
    ):

        file_record = UploadedFile(
            filename=filename,
            content_type=content_type,
            file_size=file_size,
            file_data=file_data
        )

        self.db.add(file_record)

        self.db.commit()

        self.db.refresh(file_record)

        return file_record