import uuid

from sqlalchemy import String, Float, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot_station.data.base.database.base_db_dto import BaseDBDto


class BotInfoDto(BaseDBDto):
    __tablename__ = "bot_meta_info"

    id: Mapped[str] = mapped_column("id", String(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    temperature: Mapped[float] = mapped_column(Float())
    prompt_intro: Mapped[str] = mapped_column(String())
    add_external_context_to_prompt: Mapped[bool] = mapped_column(Boolean())
    add_messages_history_to_prompt: Mapped[bool] = mapped_column(Boolean())
    min_extract_relevant_docs_score: Mapped[float] = mapped_column(Float())
    limit_extract_relevant_docs: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return (f"Bot("
                f"id={self.id!r}, "
                f"name={self.name!r}, "
                f"temperature={self.temperature!r}, "
                f"prompt={self.prompt_intro!r},"
                f"min_relevant_docs_score={self.min_extract_relevant_docs_score},"
                f"limit_extract_relevant_docs={self.limit_extract_relevant_docs}"
                f")")
