from dataclasses import dataclass, field


@dataclass
class WebAppConfig:
    version: str = field(default="0.1.0")
    title: str = field(default="Bot Station API")
    debug: bool = field(default=True)
