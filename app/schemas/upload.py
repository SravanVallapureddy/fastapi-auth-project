from pydantic import BaseModel


class UploadResponse(BaseModel):

    id: int
    filename: str
    content_type: str
    file_size: int
    message: str