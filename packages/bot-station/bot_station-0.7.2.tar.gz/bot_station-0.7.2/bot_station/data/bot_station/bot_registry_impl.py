import logging
from typing import List

from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session

from bot_station.data.bot_station import db_path
from bot_station.data.bot_station.model.bot_info_dto import BotInfoDto
from bot_station.domain.bot_station.bot_registry import BotRegistry
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo


class BotRegistryImpl(BotRegistry):
    __engine = create_engine(db_path, echo=False)
    __storage = {}

    async def create(self, config: BotMetaInfo) -> BotMetaInfo:
        logging.debug(f"create {config}")
        session = Session(self.__engine)
        dto = self.__map_to_dto(config)
        session.add(dto)
        session.commit()
        return self.__map_from_dto(dto)

    async def get(self, bot_id: str) -> BotMetaInfo | None:
        session = Session(self.__engine)
        dto = self.__select_dto(bot_id=bot_id, session=session)
        if dto is None:
            return None
        else:
            return self.__map_from_dto(dto)

    async def get_all(self) -> List[BotMetaInfo]:
        session = Session(self.__engine)
        stmt = select(BotInfoDto)
        dtos = session.scalars(stmt).all()
        return list(map(lambda dto: self.__map_from_dto(dto), dtos))

    async def update(self, meta: BotMetaInfo):
        session = Session(self.__engine)
        dto = self.__select_dto(bot_id=meta.id, session=session)
        if dto is not None:
            dto.name = meta.name
            dto.description = meta.description
            dto.temperature = meta.temperature
            dto.prompt_intro = meta.prompt_intro
            dto.add_external_context_to_prompt = meta.add_external_context_to_prompt
            dto.add_messages_history_to_prompt = meta.add_messages_history_to_prompt
            dto.limit_extract_relevant_docs=meta.limit_extract_relevant_docs
            dto.min_extract_relevant_docs_score=meta.min_extract_relevant_docs_score

            session.commit()

    def __select_dto(self, bot_id: str, session: Session) -> BotInfoDto | None:
        stmt = select(BotInfoDto).where(BotInfoDto.id.is_(bot_id))
        return session.scalars(stmt).one_or_none()

    async def delete(self, bot_id: str):
        session = Session(self.__engine)
        sql = delete(BotInfoDto).where(BotInfoDto.id == bot_id)
        session.execute(sql)
        session.commit()

    @staticmethod
    def __map_from_dto(dto: BotInfoDto) -> BotMetaInfo:
        return BotMetaInfo(
            id=str(dto.id),
            name=dto.name,
            description=dto.description,
            prompt_intro=dto.prompt_intro,
            add_external_context_to_prompt=dto.add_external_context_to_prompt,
            add_messages_history_to_prompt=dto.add_messages_history_to_prompt,
            temperature=dto.temperature,
            limit_extract_relevant_docs=dto.limit_extract_relevant_docs,
            min_extract_relevant_docs_score=dto.min_extract_relevant_docs_score
        )

    @staticmethod
    def __map_to_dto(info: BotMetaInfo) -> BotInfoDto:
        return BotInfoDto(
            id=info.id,
            name=info.name,
            description=info.description,
            prompt_intro=info.prompt_intro,
            add_external_context_to_prompt=info.add_external_context_to_prompt,
            add_messages_history_to_prompt=info.add_messages_history_to_prompt,
            temperature=info.temperature,
            limit_extract_relevant_docs=info.limit_extract_relevant_docs,
            min_extract_relevant_docs_score=info.min_extract_relevant_docs_score
        )
