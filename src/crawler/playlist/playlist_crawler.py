import re
import requests
from logging import Logger
from bs4 import BeautifulSoup
from ..utils import resizeImg


def validate_iamge_ext(img_path: str) -> bool:
    return img_path.endswith(".jpg") or img_path.endswith(".jpeg") or img_path.endswith(".png")


def getSongInfo(song_list_wrap, config, log: Logger) -> list[dict]:
    list_wrap_table = song_list_wrap.select_one(".list-wrap")
    table_tbody = list_wrap_table.find("tbody")

    songs = []
    for tr in table_tbody.find_all("tr"):
        all_val = []

        # IMG_path
        td_img = tr.find_all("td")[2]

        path_img = td_img.find("a").find("img")["src"]
        path_img = path_img[: path_img.find("/dims")]

        if not validate_iamge_ext(path_img):
            continue

        path_img = "https:" + resizeImg(path_img, config.img_resize, config.max_resize)
        all_val.append(path_img)

        # [song, artist, album]
        td_info = tr.find_all("td")[4]
        for idx, td_a in enumerate(td_info.find_all("a")):
            onclick = td_a["onclick"]
            start_idx = onclick.find("('")

            if idx == 0:
                val = td_a["title"]
                end_idx = onclick.find("',")
            else:
                val = td_a.text
                end_idx = onclick.find("')")
            genie_id = onclick[start_idx + 2 : end_idx]
            all_val.extend([val, genie_id])
        info = {
            "IMG_PATH": all_val[0],
            "SONG_TITLE": all_val[1],
            "SONG_ID": str(all_val[2]),
            "ARTIST_NAME": all_val[3],
            "ARTIST_ID": str(all_val[4]),
            "ALBUM_TITLE": all_val[5],
            "ALBUM_ID": all_val[6],
        }
        songs.append(info)
    log.info("-- %d songs are added", len(songs))
    return songs


def getPlaylistInfo(id: int, url: str, config, songs_list: list[dict], log: Logger) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    playlist_info = soup.select_one(".playlist-info")
    info = playlist_info.select_one(".info")

    # playlist title
    title = info.select_one(".info__title").text
    log.info("title: %s", title)

    # playlist description
    title_sub = info.select_one(".info__title--sub").text.strip()
    log.info("title_sub: %s", title_sub)

    info_data = info.select_one(".info__data")
    info_data_list = info_data.find_all("dd")

    num_of_song = int((info_data_list[1].text.rstrip())[:-1])  # nums of playlist songs
    log.info("num_of_song: %d", num_of_song)

    view = info_data_list[2].text  # playlist views
    view = int(re.sub("[^0-9]", "", view))
    log.info("view: %d", view)

    # playlist tags
    tags = info_data.select_one(".tags").find_all("a")
    tag_list = [tag.text[1:] for tag in tags]
    log.info("tag_list: %s", tag_list)

    # playlist cover image
    pl_img_url = soup.find("meta", {"property": "og:image:secure_url"})["content"]
    pl_img_url = resizeImg(pl_img_url, config.img_resize, config.max_resize)
    log.info("pl_img_url: %s", pl_img_url)

    # counts of playlist like
    info_buttons = info.select_one(".info__buttons")
    sns_like = info_buttons.select_one(".sns-like")
    like_radius = (sns_like.find_all("a"))[-1]
    like_count = like_radius.find("em").text
    like_count = int(re.sub("[^0-9]", "", like_count))
    log.info("like_count: %d", like_count)

    # info of songs in playlist
    song_list_wrap = soup.select_one(".music-list-wrap")
    song_info = getSongInfo(song_list_wrap, config, log)
    songs_list += song_info
    song_ids = [song["SONG_ID"] for song in song_info]

    info = {
        "PLAYLIST_ID": str(id),
        "PLAYLIST_TITLE": title,
        "PLAYLIST_SUBTITLE": title_sub,
        "NUM_OF_SONGS": num_of_song,
        "PLAYLIST_SONGS": song_ids,
        "PLAYLIST_VIEW": view,
        "PLAYLIST_TAGS": tag_list,
        "PLAYLIST_IMG_URL": pl_img_url,
        "PLAYLIST_LIKECOUNT": like_count,
    }

    log.info("-- now nums of songs : %d", len(songs_list))

    return info
