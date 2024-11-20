from bs4 import BeautifulSoup
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import *
from constants import BEE_URL


def get_bee_links(html: str) -> list:
    """
    Get the links of all bees from the HTML.

    :param html: The HTML to get the bees from.
    :return: The links of bees.
    """

    soup = BeautifulSoup(html, "html.parser")
    links = []

    table = soup.find("table", class_="wikitable")
    for row in table.find_all("tr")[2:]:
        href = row.find("td").find("a").get("href")
        link = "https://bee-swarm-simulator.fandom.com" + href
        links.append(link)

    return links


def get_bees(links: list) -> dict:
    """
    Get the bees from the links.

    :param links: The links to get the bees from.
    :return: The bees from the links.
    """

    bees = {}
    return bees


if __name__ == "__main__":
    html = get_html(BEE_URL)
    # save_html(html, "bee.html")
    links = get_bee_links(html)
    print(links)
