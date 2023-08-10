from pydantic import BaseModel
from datetime import datetime


class Artist(BaseModel):
    id: str
    genie_id: str
    name: str
    created_at: datetime
    updated_at: datetime
