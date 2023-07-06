from bs4 import BeautifulSoup, Tag

SONG_DAILY_CHART_SELECTOR = ".daily-chart div.total"
SONG_DAILY_CHART_LISTENER_CNT_SELECTOR = "div:nth-child(1) p"
SONG_DAILY_CHART_PLAY_CNT_SELECTOR = "div:nth-child(2) p"


def parseListenerCnt(listener_cnt_el: Tag) -> int:
    return int(listener_cnt_el.text.replace(",", ""))


def parsePlayCnt(play_cnt_el: Tag) -> int:
    return int(play_cnt_el.text.replace(",", ""))


def crawlSongDailyChart(soup: BeautifulSoup) -> tuple[int, int]:
    song_daliy_chart_el = soup.select_one(SONG_DAILY_CHART_SELECTOR)

    # listener cnt
    listener_cnt_el = song_daliy_chart_el.select_one(SONG_DAILY_CHART_LISTENER_CNT_SELECTOR)
    listener_cnt = parseListenerCnt(listener_cnt_el)

    # play cnt
    play_cnt_el = song_daliy_chart_el.select_one(SONG_DAILY_CHART_PLAY_CNT_SELECTOR)
    play_cnt = parsePlayCnt(play_cnt_el)

    return listener_cnt, play_cnt
