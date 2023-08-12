import os
import db
from config.config import DBConfig
from migration.playlist import PlaylistCsvMigrate
from migration.song import SongCsvMigrate

INPUT_PATH = "/input"
PLAYLIST_PATH = os.path.join(INPUT_PATH, "playlists.csv")
SONG_PATH = os.path.join(INPUT_PATH, "songs.csv")


def main() -> None:
    config = DBConfig()
    db.connect(config.db_name, config.db_host, config.db_username, config.db_password)
    song_csv_migrate = SongCsvMigrate(SONG_PATH)
    playlist_csv_migrate = PlaylistCsvMigrate(PLAYLIST_PATH)

    song_csv_migrate.add_albums()
    song_csv_migrate.add_artists()
    song_csv_migrate.add_songs()
    playlist_csv_migrate.add_playlists()

    db.disconnect()


if __name__ == "__main__":
    main()
