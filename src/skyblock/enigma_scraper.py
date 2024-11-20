from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import *
from constants import ENIGMA_SOUL_URL


def get_enigma_souls(html: str) -> dict:
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
    html = get_html(ENIGMA_SOUL_URL)
    enigma_souls = get_enigma_souls(html)
    save_json(enigma_souls, "enigma_souls.json")
