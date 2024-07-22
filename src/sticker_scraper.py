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
    stickers = {}

    tables = soup.select("table.article-table.mw-collapsible")
    for table in tables:
        rows = table.find_all("tr")  # Skip the header row

        # Parse out the category
        category_img = rows[0].find("th").find("a").find("img")
        if category_img is None:
            continue
        category = category_img["alt"].split(" ")[-1].lower()
        if category not in stickers:
            stickers[category] = []

        for row in rows[1:]:
            cells = row.find_all(["th", "td"])
            sticker_data = {
                "image_url": cells[0].find("a")["href"].split("/revision")[0],
                "name": cells[1].text.strip(),
                "description": cells[2].text.strip(),
                "stack_boost": cells[3].text.strip(),
                "stack_reward": cells[4].text.strip(),
                "where_from": cells[5].text.strip(),
            }
            stickers[category].append(sticker_data)

    return stickers


if __name__ == "__main__":
    html = get_html(STICKER_URL)
    # save_html(html, "sticker.html")
    stickers = get_stickers(html)
    for category, sticker_list in stickers.items():
        save_json(sticker_list, f"{category}s.json")
