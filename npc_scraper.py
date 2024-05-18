from bs4 import BeautifulSoup
from core import get_html, save_html


NPC_URL = 'https://wiki.hypixel.net/NPCs'

def get_npcs(html: str) -> dict:
    """
    Get the NPCs from the HTML.

    :param html: The HTML to get the NPCs from.
    :return: The NPCs from the HTML.
    """

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all(['blockquote', 'h4'])
    npcs = {}

    last_area = 'Unknown'
    for block in blocks:
        # Find the area name
        if block.name == 'blockquote':
            area_tag = block.find('a', title=True)
            last_area = area_tag['title'] if area_tag else 'Unknown'

        # Create the area if it doesn't exist
        if last_area not in npcs:
            npcs[last_area] = []
        
        # Find the NPCs
        table = block.find_next_sibling('table', class_='wikitable mw-collapsible')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                title_tag = row.find('a', title=True)
                if title_tag:
                    npcs[last_area].append(title_tag['title'])
    
    return npcs

if __name__ == '__main__':
    html = get_html(NPC_URL)
    print(get_npcs(html))
