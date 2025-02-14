from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import BQUIP_URL
from util.logger import Logger


def get_beequip_links(html: str) -> list:
    """
    Get the links of all beequips from the HTML.

    :param html: The HTML to get the bee equips from.
    :return: The links of beequips.
    """

    soup = BeautifulSoup(html, "html.parser")
    links = []

    tabs = soup.select('[id^="flytabs_"]')
    for tab in tabs:
        for a in tab.find_all("a"):
            href = a.get("href")
            if href:
                links.append(href)

    return links


def get_beequips(links: list, retries: int, logger: Logger) -> list:
    """
    Get the beequips from the links.

    :param links: The links to get the beequips from.
    :param retries: The number of retries to make.
    :param logger: The logger to log to.
    :return: The beequips from the links.
    """

    beequips = []
    for link in links:
        html = get_html(link, retries, logger)
        soup = BeautifulSoup(html, "html.parser")

        card = soup.find("div", class_="mw-parser-output")
        table = card.find("table", class_="infobox")
        name = table.select("tr td p")[0].text.strip()
        image_url = table.find("a", class_="image").get("href").split("/revision")[0]

        # Extracting level, color, and limit
        details = table.select("table table td p")
        level = details[0].text.strip().split(": ")[1]
        color = details[1].text.strip().split(": ")[1]
        limit = details[2].text.strip().split(": ")[1]
        description = table.find("td", style="font-style:italic;").text.strip()

        # Extracting requirements and bees
        try:
            requirements = table.select("tr td div p")[0]
            requirement = requirements.text[requirements.text.find("Bee") :].strip() or "None"
            bees = [
                a.find("img").get("data-src").split("/revision")[0] for a in requirements.find_all("a", title=True)
            ]
        except:
            requirement = "None"
            bees = []

        # Finding possible stats
        stats_span = soup.select_one("span#Possible_Stats, span#Potential_Stats, span#Potential")
        if stats_span is None:
            stats = ["TODO: Scrape stats table"]
        else:
            stats_h2 = stats_span.find_parent("h2")
            stats_list = stats_h2.find_next_sibling("ul")
            stats = [li.text.strip() for li in stats_list.find_all("li")]

        beequips.append(
            {
                "name": name,
                "image_url": image_url,
                "level": level,
                "color": color,
                "limit": limit,
                "description": description,
                "bees": bees,
                "requirement": requirement,
                "stats": stats,
            }
        )

    return beequips


if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))

    # Initialize the logger
    logger = Logger("Beequip Scraper", "logs/beequip_scraper.log", LOG)

    # Scrape the beequips and save them to a JSON file
    html = get_html(BQUIP_URL, RETRIES, logger)
    links = get_beequip_links(html)
    beequips = get_beequips(links, RETRIES, logger)
    save_json(beequips, "beequips.json", logger)
