import re
from omegaconf import DictConfig
from logging import Logger

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.utils import resizeImg


def getSongInfo(song_list_wrap, config: DictConfig, log: Logger) -> list[dict]:
    list_wrap_table = song_list_wrap.find_element(By.CLASS_NAME, "list-wrap")
    table_tbody = list_wrap_table.find_element(By.TAG_NAME, "tbody")

    songs = []
    for tr in table_tbody.find_elements(By.TAG_NAME, "tr"):
        all_val = []

        # IMG_path
        td_img = tr.find_elements(By.TAG_NAME, "td")[2]
        path_img = td_img.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img").get_attribute("src")
        path_img = resizeImg(path_img[: path_img.find("/dims")], config.img_resize, config.max_resize)
        all_val.append(path_img)

        # [song, artist, album]
        td_info = tr.find_elements(By.TAG_NAME, "td")[4]
        for idx, td_a in enumerate(td_info.find_elements(By.TAG_NAME, "a")):
            onclick = td_a.get_attribute("onclick")
            start_idx = onclick.find("('")

            if idx == 0:
                val = td_a.get_attribute("title")
                end_idx = onclick.find("',")
            else:
                val = td_a.text
                end_idx = onclick.find("')")
            genie_id = onclick[start_idx + 2 : end_idx]
            all_val.extend([val, genie_id])
        info = {
            "IMG_PATH": all_val[0],
            "SONG_TITLE": all_val[1],
            "SONG_ID": all_val[2],
            "ARTIST_NAME": all_val[3],
            "ARTIST_ID": all_val[4],
            "ALBUM_TITLE": all_val[5],
            "ALBUM_ID": all_val[6],
        }
        songs.append(info)
    log.info("-- %d songs are added", len(songs))
    return songs


def getPlaylistInfo(id: int, link: str, config: DictConfig, songs_list: list[dict], log: Logger) -> dict:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")

    driver = webdriver.Chrome(options=op)
    driver.get(url=link)

    playlist_info = driver.find_element(By.CLASS_NAME, "playlist-info")
    info = playlist_info.find_element(By.CLASS_NAME, "info")

    # playlist title
    title = info.find_element(By.CLASS_NAME, "info__title").text
    log.info("title: %s", title)

    # playlist description
    title_sub = info.find_element(By.CLASS_NAME, "info__title--sub").text
    log.info("title_sub: %s", title_sub)

    info_data = info.find_element(By.CLASS_NAME, "info__data")
    info_data_list = info_data.find_elements(By.TAG_NAME, "dd")

    num_of_song = int((info_data_list[1].text.rstrip())[:-1])  # nums of playlist songs
    log.info("num_of_song: %d", num_of_song)

    view = info_data_list[2].text  # playlist views
    view = int(re.sub("[^0-9]", "", view))
    log.info("view: %d", view)

    # playlist tags
    tags = info_data.find_element(By.CLASS_NAME, "tags").find_elements(By.TAG_NAME, "a")
    tag_list = [tag.text[1:] for tag in tags]
    log.info("tag_list: %s", tag_list)

    # playlist cover image
    pl_img_tag = driver.find_element(By.XPATH, "/html/head/meta[10]")
    pl_img_url = resizeImg(pl_img_tag.get_attribute("content"), config.img_resize, config.max_resize)
    log.info("pl_img_url: %s", pl_img_url)

    # counts of playlist like
    info_buttons = info.find_element(By.CLASS_NAME, "info__buttons")
    sns_like = info_buttons.find_element(By.CLASS_NAME, "sns-like")
    like_radius = (sns_like.find_elements(By.TAG_NAME, "a"))[-1]
    like_count = like_radius.find_element(By.ID, "emLikeCount").text
    like_count = int(re.sub("[^0-9]", "", like_count))
    log.info("like_count: %d", like_count)

    # info of songs in playlist
    song_list_wrap = driver.find_element(By.CLASS_NAME, "music-list-wrap")
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

    driver.close()
    log.info("-- now nums of songs : %d", len(songs_list))

    return info
