from bs4 import BeautifulSoup
from core import get_html, save_html


NPC_URL = 'https://wiki.hypixel.net/NPCs'

def get_npcs(html: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all(['blockquote', 'h4'])

    last_area = 'Unknown'
    for block in blocks:
        if block.name == 'blockquote':
            area_tag = block.find('a', title=True)
            last_area = area_tag['title'] if area_tag else 'Unknown'
        
        if block.name == 'h4' or block.find_next_sibling('table', class_='wikitable mw-collapsible'):
            table = block.find_next_sibling('table', class_='wikitable mw-collapsible')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    title_tag = row.find('a', title=True)
                    if title_tag:
                        print(f"NPC: {title_tag['title']}, Area: {last_area}")

if __name__ == '__main__':
    html = get_html(NPC_URL)
    save_html(html, 'html/npcs.html')
    get_npcs(html)
