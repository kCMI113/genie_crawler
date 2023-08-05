import hydra
from tqdm import tqdm
from omegaconf import DictConfig

from src.utils import getLogger, getLastPlaylistId, saveInfoDict2Csv
from playlist.playlist_crawler import getPlaylistInfo


@hydra.main(version_base="1.2", config_path="configs", config_name="playlist.yaml")
def main(config: DictConfig = None) -> None:
    # logger setting
    log = getLogger()
    log.propagate = False

    # crawling playlists and songs
    log.info("Start playlist crawling ...")
    pl_list, songs_list = [], []

    # set searching playlist idx
    start_idx = config.start_idx
    if config.end_idx:
        end_idx = config.end_idx
    else:
        # get last playlist id
        log.info("Check Last playlist item id ...")
        end_idx = getLastPlaylistId(config.playlist_origin_url)
        log.info("-- Last playlist item id is %d !!!", end_idx)
    err_list = []

    # start searching
    for id in tqdm(range(start_idx, end_idx + 1)):
        try:
            pl_url = config.playlist_url + str(id)
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

    # save crwaling results
    saveInfoDict2Csv(pl_list, songs_list, config, start_idx, end_idx)


if __name__ == "__main__":
    main()
