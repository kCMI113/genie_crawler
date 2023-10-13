import os
from src.db import db
from src.config import GenieConfig
from src.migration import PlaylistCsvMigrate, SongCsvMigrate

config = GenieConfig()
PLAYLIST_PATH = os.path.join(config.input_path, config.pl_file)
SONG_PATH = os.path.join(config.input_path, config.song_file)


def main() -> None:
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
