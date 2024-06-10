from typing import AsyncGenerator, Any
from aiohttp import ClientSession
import bs4
from os.path import basename

from msoc.sound import Sound


URL = "https://zaycev.net"
API_URL = URL + "/api/external/track"
SEARCH_URL = URL + "/search?query_search="

DATA_TEMPLATE_TRACKS_META = { 
    "trackIds": [],
    "subscription": False
}


def get_id(li: bs4.Tag) -> str:
    href = li.select_one("div:nth-child(1) > div:nth-child(1) > article:nth-child(2) > a:nth-child(1)").attrs.get("href")

    track_id = basename(href).split(".")[0]
    return track_id


async def get_tracks_download_hashes(session: ClientSession, track_ids: list[str]) -> AsyncGenerator[int, str]:
    data = DATA_TEMPLATE_TRACKS_META.copy()
    data['trackIds'] = track_ids

    async with session.post(url=API_URL + "/filezmeta", data=data) as response:
        json_data = await response.json()

    for track_meta in json_data["tracks"]:
        track_id = track_meta["id"]
        download_hash = track_meta["download"]

        yield track_id, download_hash


async def get_url(session: ClientSession, download_hash: str) -> str:
    async with session.get(API_URL + "/download/" + download_hash) as response:
        url = await response.text()
        return url


def get_name(li: bs4.Tag) -> str:   
   span = li.select_one("div:nth-child(1) > div:nth-child(1) > article:nth-child(2) > a:nth-child(1) > span:nth-child(1)")

   return span.text


async def search(query: str):
    async with ClientSession() as session:
        async with session.get(SEARCH_URL + query) as response:
            html_text = await response.text()

        html = bs4.BeautifulSoup(html_text, "html.parser")
        ul = html.find("ul", attrs={"class", "xm4ofx-1 itNyE"})
            
        track_names = dict()
        for li in ul.find_all("li"):
            name = get_name(li)
            track_id = get_id(li)

            track_names[track_id] = name

        async for track_id, download_hash in get_tracks_download_hashes(session, track_names.keys()):
            name = track_names[str(track_id)]
            url = await get_url(session, download_hash)

            yield Sound(name, url)
