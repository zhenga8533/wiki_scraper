from bs4 import BeautifulSoup
from core import *
from constants import STICKER_URL


def get_stickers(html: str) -> list:
    """
    Get the stickers from the HTML.

    :param html: The HTML to get the stickers from.
    :return: The stickers from the HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    stickers = []

    tables = soup.find_all("table", class_="article-table mw-collapsible mw-collapsed article-table striped sortable")
    for table in tables:
        headers = ["Image URL", "Name", "Description", "Stack Boost", "Stack Reward", "Where it's from"]
        rows = table.find_all("tr")[1:]  # Skip the header row

        for row in rows:
            cells = row.find_all(["th", "td"])
            sticker_data = {
                "image_url": cells[0].find("a")["href"],
                "name": cells[1].text.strip(),
                "description": cells[2].text.strip(),
                "stack_boost": cells[3].text.strip(),
                "stack_reward": cells[4].text.strip(),
                "where_from": cells[5].text.strip(),
            }
            stickers.append(sticker_data)

    return stickers


if __name__ == "__main__":
    html = get_html(STICKER_URL)
    # save_html(html, "sticker.html")
    stickers = get_stickers(html)
    save_json(stickers, "stickers.json")
