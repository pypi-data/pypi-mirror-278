from dataclasses import dataclass


@dataclass
class YandexCloudConfig:
    api_key: str
    folder_id: str
    model_name: str
    model_version: str
