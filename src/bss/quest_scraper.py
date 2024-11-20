from bs4 import BeautifulSoup
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import *
from constants import QUEST_GIVER_URL


def get_npc_links(html: str) -> list:
    """
    Get the links of all NPCs from the HTML.

    :param html: The HTML to get the NPCs from.
    :return: The links of NPCs.
    """

    soup = BeautifulSoup(html, "html.parser")
    base_url = "https://bee-swarm-simulator.fandom.com"
    links = []

    tables = soup.find_all("table", class_="article-table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            first_td = row.find("td")
            if first_td:
                a_tag = first_td.find("a", href=True)
                if a_tag:
                    full_url = base_url + a_tag["href"]
                    links.append(full_url)

    return links


def get_quest_givers(links: list) -> dict:
    """
    Get the quest givers from the links.

    :param links: The links to get the quest givers from.
    :return: The quest givers from the links.
    """

    quest_givers = {}

    for link in links:
        html = get_html(link)
        soup = BeautifulSoup(html, "html.parser")

        parser_output_div = soup.find("div", class_="mw-parser-output")
        if parser_output_div:
            infobox_table = parser_output_div.find("table", class_="infobox")
            if infobox_table:
                # Extract the name of the quest giver
                name_tag = infobox_table.find("td", colspan="2")
                name_b_tag = name_tag.find("b")
                name = name_b_tag.text.strip()

                # Extract the image URL
                image_tag = infobox_table.find("a", class_="image")
                image_url = image_tag["href"].split("/revision")[0]

                quest_givers[name] = {"image_url": image_url}

    return quest_givers


if __name__ == "__main__":
    html = get_html(QUEST_GIVER_URL)
    # save_html(html, "quest.html")
    links = get_npc_links(html)
    quest_givers = get_quest_givers(links)
    save_json(quest_givers, "quest_givers.json")
