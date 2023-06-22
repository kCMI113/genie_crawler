import re
import selenium
from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from src.utils import resize_img

def getSongInfo(song_list_wrap, img_resize:int) -> list[dict]:
    list_wrap_table = song_list_wrap.find_element(By.CLASS_NAME, "list-wrap")
    table_tbody = list_wrap_table.find_element(By.TAG_NAME, "tbody")

    songs = []
    for tr in table_tbody.find_elements(By.TAG_NAME, "tr"):
        all_val = []
        td_img = tr.find_elements(By.TAG_NAME, "td")[2]
        path_img = td_img.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img").get_attribute("src")
        path_img = resize_img(path_img[:path_img.find("/dims")], img_resize)        
        all_val.append(path_img)

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
            genie_id = onclick[start_idx + 2:end_idx]
            all_val.extend([val,genie_id])
        info = {
            "IMG_PATH":     all_val[0],
            "SONG_TITLE":   all_val[1],
            "SONG_ID":      all_val[2],
            "ARTIST_NAME":  all_val[3],
            "ARTIST_ID":    all_val[4],
            "ALBUM_TITLE":  all_val[5],
            "ALBUM_ID":     all_val[6],
        }
        songs.append(info)

    return songs


def getPlaylistInfo(link: str, is_resize: bool, img_resize: int) -> None:
    driver = webdriver.Chrome()
    driver.get(url=link)
    
    playlist_info = driver.find_element(By.CLASS_NAME, "playlist-info")
    covers = playlist_info.find_element(By.CLASS_NAME, "covers")
    info = playlist_info.find_element(By.CLASS_NAME, "info")
    
    # playlist title
    title = info.find_element(By.CLASS_NAME, "info__title").text
    print("title:", title)
    
    # playlist description
    title_sub = info.find_element(By.CLASS_NAME, "info__title--sub").text
    print("title_sub:", title_sub)
    
    info_data = info.find_element(By.CLASS_NAME, "info__data")
    info_data_list = info_data.find_elements(By.TAG_NAME, "dd")
    
    num_of_song = int((info_data_list[1].text.rstrip())[:-1])  # nums of playlist songs
    print("num_of_song:", num_of_song)
    
    view = info_data_list[2].text  # playlist views
    view = re.sub('[^0-9]', "", view)
    print("view:", view)
    
    # playlist tags
    tags = info_data.find_element(By.CLASS_NAME, "tags").find_elements(By.TAG_NAME, "a")
    tag_list = [tag.text[1:] for tag in tags]
    print("tag_list:", tag_list)
    
    # playlist cover image
    pl_img_tag = driver.find_element(By.XPATH, "/html/head/meta[10]")
    pl_img_url = resize_img(pl_img_tag.get_attribute("content"))
    print("pl_img_url:", pl_img_url)
    
    # counts of playlist like
    info_buttons = info.find_element(By.CLASS_NAME, "info__buttons")
    sns_like = info_buttons.find_element(By.CLASS_NAME, "sns-like")
    like_radius = (sns_like.find_elements(By.TAG_NAME, "a"))[-1]
    like_count = int(like_radius.find_element(By.ID, "emLikeCount").text)
    print("like_count:", like_count)
    
    # info of songs in playlist
    song_list_wrap = driver.find_element(By.CLASS_NAME, "music-list-wrap")
    song_info = getSongInfo(song_list_wrap, img_resize)
    print("-------------- SONG INFO --------------")
    for song in song_info:
        print(song)
    
    driver.close()