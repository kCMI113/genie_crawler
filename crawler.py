import os
import pandas as pd
from src.config import GenieConfig
from src.db import db, PlaylistRepository, Playlist
from src.migration import CrawlerMigrate
from src.crawler import crawlAlbum, crawlPlaylist, crawlSong
from src.crawler.utils import getLogger


logger = getLogger()
config = GenieConfig()
PLAYLIST_PATH = os.path.join(config.input_path, config.pl_file)
SONG_PATH = os.path.join(config.input_path, config.song_file)
OUTPUT_PLAYLIST_PATH = os.path.join(config.output_path, config.output_pl_file)


def main() -> None:
    db.connect(config.db_name, config.db_host, config.db_username, config.db_password)

    logger.info("print config: " + str(config))

    if config.use_latest_start_idx:
        config.start_idx = int(PlaylistRepository().find_latest_created_playlist().genie_id) + 1
        print(f"start_idx: {config.start_idx}")

    pl_df, song_df = crawlPlaylist(config)
    song_df = pd.merge(song_df, crawlSong(list(song_df["SONG_ID"])), on="SONG_ID", how="inner")
    song_df = pd.merge(song_df, crawlAlbum(list(song_df["ALBUM_ID"])), on="ALBUM_ID", how="inner")

    crawler_migrate = CrawlerMigrate(song_df, pl_df)

    crawler_migrate.add_albums()
    crawler_migrate.add_artists()
    crawler_migrate.add_songs()
    crawler_migrate.add_playlists()

    if config.enable_output_csv:
        os.makedirs(config.output_path, exist_ok=True)

        logger.info("Get all playlists from DB")
        pl_dtos: list[Playlist] = PlaylistRepository().find_all()
        pl_dicts: list[dict] = []

        for pl_dto in pl_dtos:
            pl_dicts.append(
                {
                    "PLAYLIST_ID": int(pl_dto.genie_id),
                    "PLAYLIST_TITLE": pl_dto.title,
                    "PLAYLIST_SUBTITLE": pl_dto.subtitle,
                    "NUM_OF_SONGS": pl_dto.song_cnt,
                    "PLAYLIST_SONGS": [song.genie_id for song in pl_dto.songs],
                    "PLAYLIST_VIEW": pl_dto.view_cnt,
                    "PLAYLIST_TAGS": pl_dto.tags,
                    "PLAYLIST_IMG_URL": pl_dto.img_url,
                    "PLAYLIST_LIKECOUNT": pl_dto.like_cnt,
                }
            )

        logger.info("Dump crawled playlist to csv: %s", OUTPUT_PLAYLIST_PATH)
        all_pl_df = pd.DataFrame(pl_dicts)
        all_pl_df.to_csv(OUTPUT_PLAYLIST_PATH, index=False)

    db.disconnect()


if __name__ == "__main__":
    main()
