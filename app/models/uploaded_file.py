from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from datetime import datetime

from app.db.database import Base


class UploadedFile(Base):

    __tablename__ = "uploaded_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    content_type = Column(
        String(100),
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    file_data = Column(
        LargeBinary,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )