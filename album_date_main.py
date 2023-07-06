import hydra
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from omegaconf import DictConfig
import os
from src.utils import getLogger
from src.album_date_crawler import crawlAlbumInfo


@hydra.main(version_base="1.2", config_path="configs", config_name="album_date.yaml")
def main(config: DictConfig = None) -> None:
    # log file setting
    log = getLogger()
    log.propagate = False

    # load base song info
    song_info_path = os.path.join(config.out_dir, config.song_info_filename)
    log.info("Load song_info files to retrieve song_id from %s", song_info_path)
    song_info_df = pd.read_csv(song_info_path, dtype={"ALBUM_ID": int})
    album_ids: list[int] = song_info_df["ALBUM_ID"].unique().tolist()

    # crawling playlists and songs
    log.info("Start album info crawling ...")
    album_infos = []
    failed_crawling_album_ids = []
    for album_id in tqdm(album_ids, position=0, leave=True):
        print(album_id)
        with logging_redirect_tqdm():
            try:
                album_info = crawlAlbumInfo(album_id, config.album_detail_url, log, config)
                album_infos.append(album_info)
            except Exception as e:
                log.exception(e)
                failed_crawling_album_ids.append(album_id)

    if failed_crawling_album_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_album_ids))

    csv_path = os.path.join(config.out_dir, config.album_info_filename)
    log.info("Save album_infos to %s", csv_path)
    album_infos_df = pd.DataFrame(album_infos)
    album_infos_df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    main()
