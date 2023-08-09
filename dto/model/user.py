from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: str
    fingerprint: str
    created_at: datetime
    updated_at: datetime
