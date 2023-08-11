from mongoengine import Document, StringField, DateTimeField, URLField

from dto.model import Album
from .mixin.date import CreatedAtMixin, UpdatedAtMixin


class AlbumDocument(CreatedAtMixin, UpdatedAtMixin, Document):
    genie_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    img_url = URLField()
    released_date = DateTimeField(required=True)

    def to_dto(self) -> Album:
        return Album(
            id=str(self.id),
            genie_id=self.genie_id,
            name=self.name,
            img_url=self.img_url,
            released_date=self.released_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
