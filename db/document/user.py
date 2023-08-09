from mongoengine import Document, StringField, DateTimeField
from ...dto.model import User


class UserDocument(Document):
    fingerprint = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    def to_dto(self) -> User:
        return User(
            str(self.id),
            self.fingerprint,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
