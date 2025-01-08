from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import STICKER_URL
from util.logger import Logger


def get_stickers(html: str) -> dict:
    """
    Get the stickers from the HTML.
    Currently does not work with updated wiki page.

    :param html: The HTML to get the stickers from.
    :return: The stickers from the HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    stickers = {}

    tables = soup.select("table.article-table.mw-collapsible")
    for table in tables:
        rows = table.find_all("tr")  # Skip the header row

        # Parse out the category
        th = rows[0].find("th")
        if th is None:
            continue
        a = th.find("a")
        if a is None:
            continue
        img = a.find("img")
        if img is None:
            continue

        category = img["alt"].split(" ")[-1].lower()
        if category not in stickers:
            stickers[category] = {}

        for row in rows[1:]:
            cells = row.find_all(["th", "td"])
            name = cells[1].text.strip()

            sticker_data = {
                "image_url": cells[0].find("a")["href"].split("/revision")[0],
                "description": cells[2].text.strip(),
                "stack_boost": cells[3].text.strip(),
                "stack_reward": cells[4].text.strip(),
                "where_from": cells[5].text.strip(),
            }
            stickers[category][name] = sticker_data

    return stickers


if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))

    # Initialize the logger
    logger = Logger("Sticker Scraper", "logs/sticker_scraper.log", LOG)

    # Scrape the stickers and save them to a JSON file
    html = get_html(STICKER_URL, RETRIES, logger)
    stickers = get_stickers(html)
    save_json(stickers, "stickers.json", logger)
