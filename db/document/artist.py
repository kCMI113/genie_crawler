from mongoengine import Document, StringField, DateTimeField

from ...dto.model import Artist
from datetime import datetime


class ArtistDocument(Document):
    genie_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    updated_at = DateTimeField(required=True, default=datetime.utcnow)

    def to_dto(self) -> Artist:
        return Artist(id=str(self.id), genie_id=self.genie_id, name=self.name, created_at=self.created_at, updated_at=self.updated_at)
