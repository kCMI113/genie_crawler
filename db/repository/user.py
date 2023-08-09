from ..document import UserDocument
from ..exception import NotFoundUserException
from ...dto.model import User
from datetime import datetime
from mongoengine import QuerySet


class UserRepository:
    def create_user(self, fingerprint: str, created_at: datetime) -> User:
        user = UserDocument(fingerprint=fingerprint, created_at=created_at, updated_at=created_at)
        saved: UserDocument = user.save()
        return saved.to_dto()

    def delete_by_fingerprint(self, fingerprint: str) -> None:
        user: UserDocument = UserDocument.objects(fingerprint=fingerprint)

        if not user:
            raise NotFoundUserException(f"Can't find user document: fingerprint={fingerprint}")

        user.delete()

    def find_by_fingerprint(self, fingerprint: str) -> User:
        user: UserDocument = UserDocument.objects(fingerprint=fingerprint).first()

        if not user:
            return None

        return user.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[User]:
        users: QuerySet[UserDocument] = UserDocument.objects(upated_at__gte=query_dt)

        if not users:
            return None

        return [user.to_dto() for user in users]

    def find_all(self) -> list[User]:
        users: QuerySet[UserDocument] = UserDocument.objects
        return [user.to_dto() for user in users]
