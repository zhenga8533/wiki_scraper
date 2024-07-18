from bs4 import BeautifulSoup
from core import *
from constants import STICKER_URL


def get_stickers(html: str) -> dict:
    """
    Get the stickers from the HTML.

    :param html: The HTML to get the stickers from.
    :return: The stickers from the HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    stickers = {}

    return stickers


if __name__ == "__main__":
    html = get_html(STICKER_URL)
    save_html(html, "sticker.html")
    stickers = get_stickers(html)
    save_json(stickers, "stickers.json")
