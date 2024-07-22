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

        card = soup.find("div", class_="mw-parser-output")
        table = card.find("table", class_="infobox")
        name = table.select("tr td p")[0].text.strip()

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
            bees = [a["title"] for a in requirements.find_all("a", title=True)]
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

        beequips[name] = {
            "level": level,
            "color": color,
            "limit": limit,
            "description": description,
            "bees": bees,
            "requirement": requirement,
            "stats": stats,
        }

    return beequips


if __name__ == "__main__":
    html = get_html(BQUIP_URL)
    # save_html(html, "beequip.html")
    links = get_beequip_links(html)
    beequips = get_beequips(links)
    save_json(beequips, "beequips.json")
