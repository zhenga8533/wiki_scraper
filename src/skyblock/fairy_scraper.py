from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import *
from constants import FAIRY_SOUL_URL


def get_fairy_souls(html: str) -> dict:
    """
    Get the fairy souls from the HTML.

    :param html: The HTML to get the fairy souls from.
    :return: The fairy souls from the HTML.
    """

    fairy_souls = {}
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_="hp-tabcontent")

    for div in divs:
        # Find wiki table in the div
        table = div.find("table", class_="wikitable")
        if table is None:
            continue

        # Find the rows in the table
        rows = table.find_all("tr")[1:]
        div_id = div.get("id").rstrip("_")
        souls = []

        for row in rows:
            # Find the columns in the row
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            # Extract the fairy soul data from the columns
            x = cols[0].get_text(strip=True)
            y = cols[1].get_text(strip=True)
            z = cols[2].get_text(strip=True)
            zone = unidecode(cols[3].get_text(strip=True))

            souls.append([zone, x, y, z])

        if len(souls) > 0:
            fairy_souls[div_id] = souls

    return fairy_souls


if __name__ == "__main__":
    html = get_html(FAIRY_SOUL_URL)
    fairy_souls = get_fairy_souls(html)
    save_json(fairy_souls, "fairy_souls.json")
