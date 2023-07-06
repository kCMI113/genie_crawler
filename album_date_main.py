import hydra
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from omegaconf import DictConfig
import os

from src.utils import getLogger
from src.song_detail_crawler import crawlSongDetail


@hydra.main(version_base="1.2", config_path="configs", config_name="album_date.yaml")
def main(config: DictConfig = None) -> None:
    # log file setting
    log = getLogger()
    log.propagate = False

    # load base song info
    song_info_path = os.path.join(config.out_dir, config.song_info_filename)
    log.info("Load song_info files to retrieve song_id from %s", song_info_path)
    song_info_df = pd.read_csv(song_info_path, dtype={"SONG_ID": int})
    album_ids: list[int] = song_info_df["ALBUM_ID"].unique().to_list()

    # crawling playlists and songs
    log.info("Start album date crawling ...")
    album_dates = []
    failed_crawling_album_ids = []
    for song_id in tqdm(album_ids, position=0, leave=True):
        with logging_redirect_tqdm():
            try:
                date_info = crawlSongDetail(song_id, config.song_detail_url, log)
                album_dates.append(date_info)
            except Exception as e:
                log.exception(e)
                failed_crawling_album_ids.append(song_id)

    if failed_crawling_album_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_album_ids))

    print(album_dates)


if __name__ == "__main__":
    main()
