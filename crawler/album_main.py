import pandas as pd
from tqdm import tqdm
from config.config import GenieConfig
from tqdm.contrib.logging import logging_redirect_tqdm
from .src.utils import getLogger
from .album.album_info_crawler import crawlAlbumInfo

ALBUM_DETAIL_URL = "https://www.genie.co.kr/detail/albumInfo?axnm="
config = GenieConfig()

def crawlAlbum(album_ids: list[str]) -> pd.DataFrame:
    # log file setting
    log = getLogger()
    log.propagate = False

    # crawling playlists and songs
    log.info("Start album info crawling ...")
    album_infos = []
    failed_crawling_album_ids = []
    
    for album_id in tqdm(album_ids, position=0, leave=True):
        with logging_redirect_tqdm():
            try:
                album_info = crawlAlbumInfo(album_id, config, ALBUM_DETAIL_URL, log)
                album_infos.append(album_info)
            except Exception as e:
                log.exception(e)
                failed_crawling_album_ids.append(album_id)

    if failed_crawling_album_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_album_ids))

    album_infos_df = pd.DataFrame(album_infos)

    return album_infos_df

