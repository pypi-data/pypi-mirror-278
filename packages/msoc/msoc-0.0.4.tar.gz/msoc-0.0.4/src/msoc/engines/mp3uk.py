import aiohttp
from bs4 import BeautifulSoup

from msoc.sound import Sound


URL = "https://mp3uks.ru/index.php?do=search"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://mp3uks.ru/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://mp3uks.ru',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=1',
}


def get_name(track):
    track_title = track.find("div", {"class": "track-title"})
    try:
        return track_title.find("span").text
    except:
        return track_title.text
    

def get_url(track):
    unclean_url = track.find("a", {"class": "track-dl"})["href"]
        
    if "/dl.php?" in unclean_url:
        url = "https://mp3uk.net" + unclean_url
    else:
        url = "https:" + unclean_url

    return url



async def search(query):
    data = f"do=search&subaction=search&search_start=0&full_search=0&result_from=1&story={query}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.post(URL, data=data) as response:
            text = await response.text()

    html = BeautifulSoup(text, "html.parser")

    for track in html.find_all("div", {"class": "track-item"}):
        name = get_name(track)
        url = get_url(track)

        yield Sound(name, url)
