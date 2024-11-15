from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from core import *
from constants import PKMN_URL
import time


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
            links[i - 1].append(f"{PKMN_URL}{pokemon}")
        i += 1

    return links


def get_pkmn_data(html: str) -> list:
    """
    Get the data of a Pokemon from the HTML.

    :param html: The HTML to get the data from.
    :return: The data of a Pokemon.
    """

    # Initialize the data fields to fetch
    category = ""
    number = 0
    stats = {"HP": 0, "Attack": 0, "Defense": 0, "Sp. Atk": 0, "Sp. Def": 0, "Speed": 0}
    abilities = []
    types = []
    moves = []

    return {
        "category": category,
        "number": number,
        "stats": stats,
        "abilities": abilities,
        "types": types,
        "moves": moves,
    }


if __name__ == "__main__":
    html = get_html(PKMN_URL + "national/")
    links = get_pkmn_links(html)

    for generation in links:
        data = {}

        for link in generation:
            pokemon = link.split("/")[-1]
            print(f"Getting stats for {pokemon}...")

            html = get_html(link)
            stats = get_pkmn_data(html)
            data[pokemon] = stats
            break
        break
