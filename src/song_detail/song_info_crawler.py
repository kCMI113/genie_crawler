from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SONG_INFO_DATA_SELECTOR = "ul.info-data"
SONG_INFO_ITEM_ATTR_CLASS_NAME = "attr"
SONG_INFO_ITEM_VALUE_CLASS_NAME = "value"


def parseSongInfoData(song_info_data_el: WebElement) -> list[dict[str, str]]:
    """음악 정보 목록을 파싱합니다.

    Args:
        song_info_data_el (WebElement): ul.info-data 태그

    Returns:
        list[dict[str, str]]: 음악 정보 목록
    """
    song_info_item_els = song_info_data_el.find_elements(By.XPATH, "./li")
    song_info_data = []

    for song_info_item_el in song_info_item_els:
        attr, value = parseSongInfoItem(song_info_item_el)
        song_info_data.append({"attr": attr, "value": value})

    return song_info_data


def parseSongInfoItem(song_info_item_el: WebElement) -> tuple[str, str]:
    """음악 정보 아이템을 파싱합니다.
    아이템은 다음과 같은 것을 의미합니다.
    `아티스트    IVE (아이브)`
    `앨범명     I've IVE`

    Args:
        song_info_item_el (WebElement): ul.info-data > li

    Returns:
        tuple[str, str]: 속성 이미지url, 속성 값
    """
    attr_el = song_info_item_el.find_element(By.CLASS_NAME, SONG_INFO_ITEM_ATTR_CLASS_NAME)
    value_el = song_info_item_el.find_element(By.CLASS_NAME, SONG_INFO_ITEM_VALUE_CLASS_NAME)

    attr_content = parseSongInfoItemAttr(attr_el)
    value_content = parseSongInfoItemValue(value_el)

    return attr_content, value_content


def parseSongInfoItemValue(song_info_item_value_el: WebElement) -> str:
    if hasattr(song_info_item_value_el, "text") and song_info_item_value_el.text:
        return song_info_item_value_el.text
    else:
        value_a_el = song_info_item_value_el.find_element(By.TAG_NAME, "a")
        return value_a_el.text


def parseSongInfoItemAttr(song_info_item_attr_el: WebElement) -> str:
    attr_img_el = song_info_item_attr_el.find_element(By.TAG_NAME, "img")
    return attr_img_el.get_attribute("src")


def crawlSongInfo(driver: webdriver.Chrome) -> dict:
    song_info_data_el = driver.find_element(By.CSS_SELECTOR, SONG_INFO_DATA_SELECTOR)
    return parseSongInfoData(song_info_data_el)
