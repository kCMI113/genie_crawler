from mongoengine import Document, StringField, ReferenceField, ListField, IntField, URLField, DateTimeField
from ...dto.model import Song
from .artist import ArtistDocument
from .album import AlbumDocument


class SongDocument(Document):
    genie_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    lyrics = StringField(required=True)
    album = ReferenceField(AlbumDocument, required=True)
    artist = ReferenceField(ArtistDocument, required=True)
    like_cnt = IntField(required=True)
    listener_cnt = IntField(required=True)
    play_cnt = IntField(required=True)
    genres = ListField(StringField(), required=True)
    spotify_url = URLField()
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    def to_dto(self) -> Song:
        return Song(
            id=str(self.id),
            genie_id=self.genie_id,
            title=self.title,
            lyrics=self.lyrics,
            album=self.album.to_dto(),
            artist=self.artist.to_dto(),
            like_cnt=self.like_cnt,
            listener_cnt=self.listener_cnt,
            play_cnt=self.play_cnt,
            genres=self.genres,
            spotify_url=self.spotify_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
