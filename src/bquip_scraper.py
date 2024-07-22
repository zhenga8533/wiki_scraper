from bs4 import BeautifulSoup
from core import *
from constants import BQUIP_URL


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


def get_beequips(links: list) -> dict:
    """
    Get the beequips from the links.

    :param links: The links to get the beequips from.
    :return: The beequips from the links.
    """

    beequips = {}
    for link in links:
        html = get_html(link)
        soup = BeautifulSoup(html, "html.parser")
        continue

    return beequips


if __name__ == "__main__":
    html = get_html(BQUIP_URL)
    save_html(html, "beequip.html")
    links = get_beequip_links(html)
    print(links)
