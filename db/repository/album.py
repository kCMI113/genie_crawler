from ..document import AlbumDocument
from ..exception import NotFoundAlbumException
from ...dto.model import Album
from datetime import datetime, date
from mongoengine import QuerySet


class AlbumRepository:
    def create_Album(self, genie_id: str, name: str, img_url: str, released_date: date, created_at: datetime) -> Album:
        Album = AlbumDocument(
            genie_id=genie_id, name=name, img_url=img_url, released_date=released_date, created_at=created_at, updated_at=created_at
        )
        saved: AlbumDocument = Album.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        Album: AlbumDocument = AlbumDocument.objects(genie_id=genie_id)

        if not Album:
            raise NotFoundAlbumException(f"Can't find Album document: genie_id={genie_id}")

        Album.delete()

    def find_by_genie_id(self, genie_id: str) -> Album:
        Album: AlbumDocument = AlbumDocument.objects(genie_id=genie_id).first()

        if not Album:
            return None

        return Album.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Album]:
        albums: QuerySet[AlbumDocument] = AlbumDocument.objects(upated_at__gte=query_dt)

        if not albums:
            return None

        return [album.to_dto() for album in albums]

    def find_all(self) -> list[Album]:
        Albums: QuerySet[AlbumDocument] = AlbumDocument.objects
        return [Album.to_dto() for Album in Albums]
