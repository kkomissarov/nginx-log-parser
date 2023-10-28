from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogData:
    hash: str
    created: datetime
    ip: str
    method: str
    url: str
    response_code: int
    response_size: int
    referer: str | None
    user_agent: str
