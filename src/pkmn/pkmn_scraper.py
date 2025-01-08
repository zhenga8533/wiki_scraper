from bs4 import BeautifulSoup
from dotenv import load_dotenv
import argparse
import time
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.core import *
from util.constants import PKDX_URL
from util.logger import Logger


def get_pkmn_links(html: str) -> list:
    """
    Get the links of all Pokemon from the HTML.

    :param html: The HTML to get the Pokemon from.
    :return: The links of Pokemon.
    """

    soup = BeautifulSoup(html, "html.parser")
    links = []

    i = 1
    while True:
        h2 = soup.find("h2", id=f"gen-{i}")
        if h2 is None:
            break

        links.append([])
        generation = h2.find_next("div", class_="infocard-list infocard-list-pkmn-lg")
        for div in generation.find_all("div", class_="infocard"):
            pokemon = div.find("span", class_="infocard-lg-img").find("a").get("href").split("/")[-1]
            links[i - 1].append(f"{PKDX_URL}{pokemon}")
        i += 1

    return links


def get_pkmn_data(html: str, pokemon: str) -> list:
    """
    Get the data of a Pokemon from the HTML.

    :param html: The HTML to get the data from.
    :param pokemon: The name of the Pokemon.
    :return: The data of a Pokemon.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Initialize the data fields to fetch
    sprite = ""
    name = soup.find("h1").text.strip()
    category = soup.find("th", text="Species").find_next_sibling("td").text.strip()
    number = int(soup.find("th", text="National №").find_next_sibling("td").text.strip())
    stats = {"HP": 0, "Attack": 0, "Defense": 0, "Sp. Atk": 0, "Sp. Def": 0, "Speed": 0, "Total": 0}
    abilities = [a.text.strip() for a in soup.find("th", text="Abilities").find_next_sibling("td").find_all("a")]
    types = [t.text.strip() for t in soup.find("th", text="Type").find_next_sibling("td").find_all("a")]
    moves = []

    # Get sprites in order of priority
    sprite_table = soup.find("table", class_="sprites-table")
    if sprite_table:
        sprite_priority = [
            "black-white",
            "diamond-pearl",
            "ruby-sapphire",
            "sun-moon",
            "ultra-sun-ultra-moon",
            "sword-shield",
            "scarlet-violet",
            "x-y",
            "silver",
            "red-blue",
        ]

        for gen in sprite_priority:
            pattern = re.compile(f"https://img.pokemondb.net/sprites/{gen}/normal.*{pokemon}.*")
            img_tag = soup.find("img", src=pattern)
            if img_tag:
                sprite = img_tag["src"]
                break

    # Get base stats
    stats_table = soup.find("h2", text="Base stats").find_next("table")
    for row in stats_table.find_all("tr"):
        stat_name = row.find("th").text.strip()
        stat_value = int(row.find_all("td")[0].text.strip())
        stats[stat_name] = stat_value

    # Get all moves
    moves = []
    moves_headings = [
        "Moves learnt by level up",
        "Moves learnt by TM",
        "Egg moves",
        "Moves learnt by transfer from another game",
        "Tutor moves",
        "Previous moves",
    ]
    for heading in moves_headings:
        moves_heading = soup.find("h3", text=heading)
        if moves_heading:
            moves_table = moves_heading.find_next("table")
            for row in moves_table.find_all("tr")[1:]:
                move_cell = row.find("td", class_="cell-name")
                if move_cell:
                    move_name = move_cell.text.strip()
                    if move_name not in moves:
                        moves.append(move_name)
    moves.sort()

    return {
        "name": name,
        "sprite": sprite,
        "category": category,
        "number": number,
        "stats": stats,
        "abilities": abilities,
        "types": types,
        "moves": moves,
    }


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    RETRIES = int(os.getenv("RETRIES"))
    START = int(os.getenv("START")) or 1
    END = int(os.getenv("END")) or 99

    # Initialize logger
    logger = Logger("Pokemon Scraper", "logs/pkmn_scraper.log", LOG)

    # Scrape Pokemon and save them to JSON files
    html = get_html(PKDX_URL + "national/", RETRIES, logger)
    links = get_pkmn_links(html)

    for i, generation in enumerate(links[START - 1 : END]):
        data = {}

        for link in generation:
            pokemon = link.split("/")[-1]

            html = get_html(link, RETRIES, logger)
            stats = get_pkmn_data(html, pokemon)
            data[pokemon] = stats
            time.sleep(0.5)

        save_json(data, f"pkmn_gen{i + START}.json", logger)
