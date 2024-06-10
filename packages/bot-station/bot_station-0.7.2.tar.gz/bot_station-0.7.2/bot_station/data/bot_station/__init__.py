from sqlalchemy import create_engine, Engine

from bot_station.data.base.database.base_db_dto import BaseDBDto
from bot_station.data.bot_station.model.bot_info_dto import BotInfoDto
from bot_station.domain.base.const import databases_path
from bot_station.domain.base.utils import ensure_data_folder_existence

ensure_data_folder_existence()
db_path = f"sqlite:///{databases_path}/bot_station.db"

engine: Engine = create_engine(db_path, echo=False, echo_pool=False)
BaseDBDto.metadata.create_all(bind=engine)
