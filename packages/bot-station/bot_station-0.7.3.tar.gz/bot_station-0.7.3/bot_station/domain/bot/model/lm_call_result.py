from dataclasses import dataclass

from bot_station.domain.docs.model.document import Document
from bot_station.domain.bot.model.lm_chat_message import LMBotMessage


@dataclass
class CallResult:
    answer: LMBotMessage
    relevant_docs: list[Document]
