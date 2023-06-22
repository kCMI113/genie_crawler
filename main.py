from tqdm import tqdm
from selenium.common.exceptions import UnexpectedAlertPresentException
from src.utils import set_logfile, get_last_playlist_id, save_songs_csv
from src.crawler import getPlaylistInfo
import pandas as pd

if __name__ == "__main__":
    # for DB
    # setUp()

    filename = set_logfile()
    f = open(filename, "w")

    # set driver
    playlist_origin_url = "https://www.genie.co.kr/playlist/popular?sortOrd=RDD"
    playlist_url = "https://www.genie.co.kr/playlist/detailView?plmSeq="

    print("---------- Check Last playlist item id ... ----------")
    last_pl_id = get_last_playlist_id(playlist_origin_url)
    f.write(f"[NOTICE] Last playlist item id is {last_pl_id} !!!\n")
    print(f"[NOTICE] Last playlist item id is {last_pl_id} !!!")

    print("---------- Start playlist crawling ... ----------")
    is_resize = False
    img_resize = 140
    songs_list = []

    # for id in tqdm(range(1, last_pl_id + 1)):
    # for id in tqdm(range(1, 10)):
    for id in tqdm(range(15525, 15531)):
        try:
            pl_url = playlist_url + str(id)
            getPlaylistInfo(pl_url, is_resize, img_resize, songs_list)
            f.write(f"playlist {id} is saved ...\n")
        except UnexpectedAlertPresentException:
            f.write(f">>> >>> Cannot find playlist {id} !!!\n")
            print(f">>> >>> Cannot find playlist {id} !!!")
        except Exception as ex:
            f.write(f">>> >>> {ex} : Error is occured at id {id} !!!\n")
            print(f">>> >>> {ex} : Error is occured at id {id} !!!")

    f.close()
    save_songs_csv(songs_list)

    df = pd.read_csv("outputs/song_info.csv")
    print(df)
