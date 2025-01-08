from bs4 import BeautifulSoup
from dotenv import load_dotenv
from unidecode import unidecode
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import ENIGMA_SOUL_URL
from util.logger import Logger


def get_enigma_souls(html: str) -> dict:
    """
    Scrape the enigma souls from the HTML.

    :param html: The HTML to get the enigma souls from.
    :return: The enigma souls from the HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    enigma_souls = []

    # Find the Locations header
    locations_header = soup.find("span", {"id": "Locations"})

    # Find the next table after the Locations header
    table = locations_header.find_next("table", class_="wikitable")

    if table is not None:
        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 7:
                continue

            name = cols[1].get_text(strip=True)
            x = cols[2].get_text(strip=True)
            y = cols[3].get_text(strip=True)
            z = cols[4].get_text(strip=True)
            zone = unidecode(cols[5].get_text(strip=True))
            description = " ".join(t.strip() for t in cols[6].stripped_strings)

            enigma_souls.append([name, zone, description, x, y, z])

    return enigma_souls


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))

    # Initialize logger
    logger = Logger("Enigma Soul Scraper", "logs/enigma_scraper.log", LOG)

    # Scrape enigma souls and save them to a JSON file
    html = get_html(ENIGMA_SOUL_URL, RETRIES, logger)
    enigma_souls = get_enigma_souls(html)
    save_json(enigma_souls, "enigma_souls.json", logger)
