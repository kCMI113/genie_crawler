from mongoengine import QuerySet
from ..document import AlbumDocument, ArtistDocument, PlaylistDocument, SongDocument, UserDocument
from ...dto.model import Album, Artist, Playlist, Song, User
from ..exception import NotFoundAlbumException, NotFoundArtistException, NotFoundPlaylistException, NotFoundSongException, NotFoundUserException


def find_album_doc_by_dto(album: Album) -> AlbumDocument:
    album: AlbumDocument = AlbumDocument.objects(genie_id=album.genie_id).first()

    if not album:
        raise NotFoundAlbumException(f"Can't find album document: {album}")

    return album


def find_artist_doc_by_dto(artist: Artist) -> ArtistDocument:
    artist: ArtistDocument = ArtistDocument.objects(genie_id=artist.genie_id).first()

    if not artist:
        raise NotFoundArtistException(f"Can't find artist document: {artist}")

    return artist


def find_playlist_doc_by_dto(playlist: Playlist) -> PlaylistDocument:
    playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=playlist.genie_id).first()

    if not playlist:
        raise NotFoundPlaylistException(f"Can't find playlist document: {playlist}")

    return playlist


def find_playlist_docs_by_dto(playlists: tuple[Playlist]) -> QuerySet[PlaylistDocument]:
    playlists_genie_ids = [playlists.genie_id for playlists in playlists]
    query_set: QuerySet[PlaylistDocument] = PlaylistDocument.objects(genie_id__in=playlists_genie_ids)

    if playlists and not query_set:
        raise NotFoundPlaylistException(f"Can't find playlist documents: {playlists}")

    if len(query_set) != len(playlists):
        not_found_playlists = []
        founds = list(query_set)

        for playlist in playlists:
            if playlist in founds:
                not_found_playlists.append(playlist)

        raise NotFoundPlaylistException(f"Can't find playlist documents: {not_found_playlists}")

    return query_set


def find_song_doc_by_dto(song: Song) -> SongDocument:
    song: SongDocument = SongDocument.objects(genie_id=song.genie_id).first()

    if not song:
        raise NotFoundSongException(f"Can't find song document: {song}")

    return song


def find_song_docs_by_dto(songs: tuple[Song]) -> QuerySet[SongDocument]:
    songs_genie_ids = [songs.genie_id for songs in songs]
    query_set: QuerySet[SongDocument] = SongDocument.objects(genie_id__in=songs_genie_ids)

    if songs and not query_set:
        raise NotFoundSongException(f"Can't find song documents: {songs}")

    if len(query_set) != len(songs):
        not_found_songs = []
        founds = list(query_set)

        for song in songs:
            if song in founds:
                not_found_songs.append(song)

        raise NotFoundSongException(f"Can't find song documents: {not_found_songs}")

    return query_set
