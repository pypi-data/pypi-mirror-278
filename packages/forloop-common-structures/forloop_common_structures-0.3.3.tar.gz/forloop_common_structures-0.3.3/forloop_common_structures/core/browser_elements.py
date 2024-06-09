from dataclasses import dataclass
from typing import Optional


@dataclass
class Screenshot:
    screenshot: str
    prototype_job_uid: str
    uid: Optional[str] = None


@dataclass
class Elements:
    elements: list[dict]
    prototype_job_uid: str
    uid: Optional[str] = None
