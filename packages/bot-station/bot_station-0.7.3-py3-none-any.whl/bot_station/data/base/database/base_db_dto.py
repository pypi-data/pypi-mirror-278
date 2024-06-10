from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase

from bot_station.data.base.database.UUID import uuid_id_column


class BaseDBDto(DeclarativeBase):
    __abstract__ = True

    id = uuid_id_column()
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
