from mongoengine import Document, StringField, DateTimeField

from dto.model import Artist
from .mixin.date import CreatedAtMixin, UpdatedAtMixin


class ArtistDocument(CreatedAtMixin, UpdatedAtMixin, Document):
    genie_id = StringField(required=True, unique=True)
    name = StringField(required=True)

    def to_dto(self) -> Artist:
        return Artist(id=str(self.id), genie_id=self.genie_id, name=self.name, created_at=self.created_at, updated_at=self.updated_at)
