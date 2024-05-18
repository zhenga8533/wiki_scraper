from bs4 import BeautifulSoup
from core import *


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

def find_locations(soup: BeautifulSoup) -> list:
    locations = []
    location_tags = soup.find_all('td', style="display: flex;justify-content: space-around;padding: 5px 0px;")
    for location_tag in location_tags:
        # Find the title of the location
        title_tag = location_tag.find_previous_sibling('td')
        title = title_tag.get_text(strip=True) if title_tag else 'Unknown'
        div_tags = location_tag.find_all('div', style="display: inline-block;")

        # If there are 3 div tags, then the location is valid
        if len(div_tags) == 3:
            x = div_tags[0].get_text(strip=True)
            y = div_tags[1].get_text(strip=True)
            z = div_tags[2].get_text(strip=True)
            locations.append([title, x, y, z])
    
    return locations

def get_locations(npcs) -> dict:
    locations = {}

    for area in npcs:
        world = {}

        for npc in npcs[area]:
            # Get the HTML of the NPC wiki page
            npc_url = f'https://wiki.hypixel.net/{npc.replace(" ", "_")}'
            npc_html = get_html(npc_url)
            soup = BeautifulSoup(npc_html, 'html.parser')

            # Find and store the locations of the NPC
            locs = find_locations(soup)
            if locs:
                world[npc] = locs

        locations[area] = world
    
    return locations

if __name__ == '__main__':
    html = get_html(NPC_URL)
    npcs = get_npcs(html)
    save_json(get_locations(npcs), 'locations.json')
