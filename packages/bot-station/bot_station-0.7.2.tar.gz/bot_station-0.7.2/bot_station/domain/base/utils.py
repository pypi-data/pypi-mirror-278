from pathlib import Path

from bot_station.domain.base.const import (
    data_folder_path,
    databases_path,
    message_history_path,
)


def ensure_data_folder_existence():
    for path in [
        data_folder_path,
        databases_path,
        message_history_path,
    ]:
        path = Path(path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
