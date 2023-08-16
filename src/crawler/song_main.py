import pandas as pd
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from ..config import GenieConfig
from .utils import getLogger
from .song import crawlSongDetail

SONG_DETAIL_URL = "https://www.genie.co.kr/detail/songInfo?xgnm="
config = GenieConfig()


def crawlSong(song_ids: list[str]) -> pd.DataFrame:
    # log file setting
    log = getLogger()
    log.propagate = False

    # crawling playlists and songs
    log.info("Start song detail crawling ...")
    song_details = []
    failed_crawling_song_ids = []

    for song_id in tqdm(song_ids, position=0, leave=True):
        with logging_redirect_tqdm():
            try:
                song_detail = crawlSongDetail(song_id, SONG_DETAIL_URL, log)
                song_details.append(song_detail)
            except Exception as e:
                log.exception(e)
                failed_crawling_song_ids.append(song_id)

    if failed_crawling_song_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_song_ids))

    song_details_df = pd.DataFrame(song_details)

    return song_details_df
