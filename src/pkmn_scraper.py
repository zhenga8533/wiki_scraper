from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from core import *
from constants import PKDX_URL, PKMN_URL
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

        generation = h2.find_next("div", class_="infocard-list infocard-list-pkmn-lg")
        for div in generation.find_all("div", class_="infocard"):
            pokemon = div.find("span", class_="infocard-lg-img").find("a").get("href").split("/")[-1]
            links.append(f"{PKMN_URL}{pokemon}")
        i += 1

    return links


if __name__ == "__main__":
    html = get_html(PKDX_URL)
    links = get_pkmn_links(html)
    print(links)
