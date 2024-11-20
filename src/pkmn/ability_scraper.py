from bs4 import BeautifulSoup
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import *
from constants import ABILITY_URL


def get_ability_data(html: str) -> dict:
    """
    Get the data of all ability from the HTML.

    :param html: The HTML to get the data from.
    :return: The data of an ability.
    """

    soup = BeautifulSoup(html, "html.parser")
    abilities = {}

    # Locate the table containing the ability data
    table = soup.find("table", id="abilities")
    if not table:
        return abilities

    # Iterate through each row of the table and extract the required information
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        name = cells[0].text.strip()
        ability = {
            "name": name,
            "description": cells[2].text.strip(),
            "generation": int(cells[3].text.strip()),
        }
        abilities[name.lower()] = ability

    return abilities


if __name__ == "__main__":
    html = get_html(ABILITY_URL)
    data = get_ability_data(html)
    save_json(data, "abilities.json")
