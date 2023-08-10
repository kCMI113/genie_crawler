from ..document import ArtistDocument
from ..exception import NotFoundArtistException
from dto.model import Artist
from datetime import datetime
from mongoengine import QuerySet


class ArtistRepository:
    def create_artist(self, genie_id: str, name: str) -> Artist:
        artist = ArtistDocument(genie_id=genie_id, name=name)
        saved: ArtistDocument = artist.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        artist: ArtistDocument = ArtistDocument.objects(genie_id=genie_id).first()

        if not artist:
            raise NotFoundArtistException(f"Can't find artist document: genie_id={genie_id}")

        artist.delete()

    def find_by_genie_id(self, genie_id: str) -> Artist:
        artist: ArtistDocument = ArtistDocument.objects(genie_id=genie_id).first()

        if not artist:
            return None

        return artist.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Artist]:
        artists: QuerySet[ArtistDocument] = ArtistDocument.objects(upated_at__gte=query_dt)

        if not artists:
            return None

        return [artist.to_dto() for artist in artists]

    def find_all(self) -> list[Artist]:
        artists: QuerySet[ArtistDocument] = ArtistDocument.objects
        return [artist.to_dto() for artist in artists]
