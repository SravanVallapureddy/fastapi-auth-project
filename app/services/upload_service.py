from fastapi import UploadFile

from app.repositories.upload_repository import UploadRepository


class UploadService:

    def __init__(
        self,
        repository: UploadRepository
    ):

        self.repository = repository

    async def upload_file(
        self,
        file: UploadFile
    ):

        allowed_types = {
            "application/pdf",
            "image/jpeg",
            "image/png"
        }

        if file.content_type not in allowed_types:

            raise ValueError(
                "Unsupported file type"
            )

        # 1. Read file
        file_data = await file.read()

        # 2. Check if file is empty
        if not file_data:

            raise ValueError(
                "Uploaded file is empty"
            )

        # 3. Maximum file size = 5 MB
        max_size = 5 * 1024 * 1024

        if len(file_data) > max_size:

            raise ValueError(
                "File size cannot exceed 5 MB"
            )

        # 4. Get filename
        filename = file.filename

        # 5. Get content type
        content_type = file.content_type

        # 6. Save file
        saved_file = self.repository.save_file(
            filename=filename,
            content_type=content_type,
            file_size=len(file_data),
            file_data=file_data
        )

        return saved_file