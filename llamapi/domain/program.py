from dataclasses import dataclass
from typing import List, Any

from pydantic import BaseModel

from llamapi.domain.track import Track


class Program(BaseModel):
    genre: str
    name: str
    animator_profile: str


@dataclass
class CollectionProgram:
    name: str
    path: str
