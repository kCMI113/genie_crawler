from tqdm import tqdm
import pandas as pd
from config.config import GenieConfig
from .src.utils import getLogger, getLastPlaylistId
from .playlist.playlist_crawler import getPlaylistInfo

PLAYLIST_ORIGIN_URL = "https://www.genie.co.kr/playlist/popular?sortOrd=RDD"
PLAYLIST_URL = "https://www.genie.co.kr/playlist/detailView?plmSeq="
config = GenieConfig()

def crawlPlaylist() -> (pd.DataFrame, pd.DataFrame):
    # logger setting
    log = getLogger()
    log.propagate = False

    # crawling playlists and songs
    log.info("Start playlist crawling ...")
    pl_list, songs_list = [], []

    # set searching playlist idx
    start_idx = config.start_idx

    # get last playlist id
    log.info("Check Last playlist item id ...")
    end_idx = getLastPlaylistId(PLAYLIST_ORIGIN_URL)
    log.info("-- Last playlist item id is %d !!!", end_idx)

    err_list = []

    # start searching
    for id in tqdm(range(start_idx-10, end_idx+10)):
        try:
            pl_url = PLAYLIST_URL + str(id)
            pl_info = getPlaylistInfo(id, pl_url, config, songs_list, log)
            pl_list.append(pl_info)
            log.info("playlist Id: %d", id)
        except AttributeError:
            err_list.append(id)
            log.warning("Cannot find playlist %d", id)
        except Exception as ex:
            err_list.append(id)
            log.warning("%s : Error is occured at id %d", ex, id)

    if err_list:
        log.warning("Failed crawling playlist ids : %s", err_list)

    pl_df = pd.DataFrame(pl_list)
    song_df = pd.DataFrame(songs_list)

    return pl_df, song_df
