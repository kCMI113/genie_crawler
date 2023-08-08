from src.utils import tranlateSongInfoAttrToEng
from bs4 import BeautifulSoup, Tag, ResultSet

SONG_INFO_DATA_SELECTOR = "ul.info-data"
SONG_INFO_ITEM_ATTR_SELECTOR = "span.attr"
SONG_INFO_ITEM_VALUE_SELECTOR = "span.value"


def parseSongInfoData(song_info_data_el: Tag) -> list[dict[str, str]]:
    """음악 정보 목록을 파싱합니다.

    Args:
        song_info_data_el (Tag): ul.info-data 태그

    Returns:
        list[dict[str, str]]: 음악 정보 목록
    """
    song_info_item_els: ResultSet[Tag] = song_info_data_el.findChildren("li")
    song_info_data = {}

    for song_info_item_el in song_info_item_els:
        if not song_info_item_el.select(".attr"):
            continue

        attr, value = parseSongInfoItem(song_info_item_el)
        song_info_data[attr] = value

    return song_info_data


def parseSongInfoItem(song_info_item_el: Tag) -> tuple[str, str]:
    """음악 정보 아이템을 파싱합니다.
    아이템은 다음과 같은 것을 의미합니다.
    `아티스트    IVE (아이브)`
    `앨범명     I've IVE`

    Args:
        song_info_item_el (Tag): ul.info-data > li

    Returns:
        tuple[str, str]: 속성 이미지url, 속성 값
    """
    attr_el = song_info_item_el.select_one(SONG_INFO_ITEM_ATTR_SELECTOR)
    value_el = song_info_item_el.select_one(SONG_INFO_ITEM_VALUE_SELECTOR)

    attr_content_url = parseSongInfoItemAttr(attr_el)
    value_content = parseSongInfoItemValue(value_el)

    # tranlate attr from url to eng
    attr_content_eng = tranlateSongInfoAttrToEng(attr_content_url)

    return attr_content_eng, value_content


def parseSongInfoItemValue(song_info_item_value_el: Tag) -> str:
    return song_info_item_value_el.text


def parseSongInfoItemAttr(song_info_item_attr_el: Tag) -> str:
    attr_img_el = song_info_item_attr_el.find("img")
    return attr_img_el["src"]


def crawlSongInfo(soup: BeautifulSoup) -> list[dict[str, str]]:
    song_info_data_el = soup.select_one(SONG_INFO_DATA_SELECTOR)
    return parseSongInfoData(song_info_data_el)
