from bs4 import BeautifulSoup
from core import *
from constants import PKMN_URL
import argparse
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

    # Get generation 5/8 sprite
    sprite_table = soup.find("table", class_="sprites-table")
    if sprite_table:
        normal_sprites = sprite_table.find("tbody").find("tr")
        sprite_priority = [
            "black-white",
            "diamond-pearl",
            "ruby-sapphire",
            "sun-moon",
            "sword-shield",
            "scarlet-violet",
            "x-y",
            "silver",
            "red-blue",
        ]

        for gen in sprite_priority:
            src = f"https://img.pokemondb.net/sprites/{gen}/normal/{name.lower()}.png"
            cell = normal_sprites.find("img", src=f"https://img.pokemondb.net/sprites/{gen}/normal/{name.lower()}.png")
            if cell:
                sprite = src
                break

    # Get base stats
    stats_table = soup.find("h2", text="Base stats").find_next("table")
    for row in stats_table.find_all("tr")[1:]:
        stat_name = row.find("th").text.strip()
        stat_value = int(row.find_all("td")[0].text.strip())
        stats[stat_name] = stat_value

    # Get all moves
    moves = []
    moves_table = soup.find("h3", text="Moves learnt by level up").find_next("table")
    for row in moves_table.find_all("tr")[1:]:
        move_cell = row.find("td", class_="cell-name")
        if move_cell:
            move_name = move_cell.text.strip()
            moves.append(move_name)
    tm_table = soup.find("h3", text="Moves learnt by TM").find_next("table")
    for row in tm_table.find_all("tr")[1:]:
        move_cell = row.find("td", class_="cell-name")
        if move_cell:
            move_name = move_cell.text.strip()
            moves.append(move_name)
    egg_table = soup.find("h3", text="Egg moves").find_next("table")
    for row in egg_table.find_all("tr")[1:]:
        move_cell = row.find("td", class_="cell-name")
        if move_cell:
            move_name = move_cell.text.strip()
            moves.append(move_name)

    return {
        "sprite": sprite,
        "category": category,
        "number": number,
        "stats": stats,
        "abilities": abilities,
        "types": types,
        "moves": moves,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pokemon Scraper")
    parser.add_argument("--start", type=int, default=1, help="Generation to start parsing from (default: 1)")
    parser.add_argument("--end", type=int, default=99, help="Generation to end parsing at (default: 99)")
    args = parser.parse_args()
    start = args.start
    end = args.end

    html = get_html(PKMN_URL + "national/")
    links = get_pkmn_links(html)

    for i, generation in enumerate(links[start - 1 : end]):
        data = {}
        print(f"Getting generation {i + start}...")

        for link in generation:
            pokemon = link.split("/")[-1]
            print(f"Getting stats for {pokemon}...")

            html = get_html(link)
            stats = get_pkmn_data(html)
            data[pokemon] = stats
            time.sleep(0.5)

        save_json(data, f"pkmn_gen{i + start}.json")
