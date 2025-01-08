from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import MOVES_URL
from util.logger import Logger


def get_moves_data(html: str) -> list:
    """
    Get the data of a move from the HTML.

    :param html: The HTML to get the data from.
    :return: The data of a move.
    """

    soup = BeautifulSoup(html, "html.parser")
    moves = {}

    # Locate the table containing the move data
    table = soup.find("table", class_="data-table")
    if not table:
        return moves

    # Iterate through each row of the table and extract the required information
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        name = cells[0].text.strip()
        cat = cells[2].img
        move = {
            "name": name,
            "type": cells[1].text.strip(),
            "category": cat.get("title") if cat else "-",
            "power": cells[3].text.strip(),
            "accuracy": cells[4].text.strip(),
            "pp": cells[5].text.strip(),
            "effect": cells[6].text.strip(),
        }
        moves[name.lower()] = move

    return moves


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))

    # Initialize logger
    logger = Logger("Move Scraper", "logs/move_scraper.log", LOG)

    # Scrape moves and save them to a JSON file
    html = get_html(MOVES_URL, RETRIES, logger)
    moves = get_moves_data(html)
    save_json(moves, "moves.json", logger)
