from dataclasses import dataclass

from bot_station.domain.base.const import default_prompt_intro


@dataclass
class BotMetaInfo:
    id: str
    name: str
    description: str
    prompt_intro: str = default_prompt_intro
    add_external_context_to_prompt: bool = True
    add_messages_history_to_prompt: bool = False
    temperature: float = 0.6
    min_extract_relevant_docs_score: float = 0.7
    limit_extract_relevant_docs: int = 3
