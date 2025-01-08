from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import BEE_URL
from util.logger import Logger


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
    # TODO: Implement this function
    return bees


if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))

    # Initialize the logger
    logger = Logger("Bee Scraper", "logs/bee_scraper.log", LOG)

    # Scrape the bees and save them to a JSON file
    html = get_html(BEE_URL, RETRIES, logger)
    # save_html(html, "bee.html")
    links = get_bee_links(html)
    print(links)
