from bs4 import BeautifulSoup
from core import get_html, save_html


NPC_URL = 'https://wiki.hypixel.net/NPCs'

def get_npcs(html: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='wikitable mw-collapsible')
    
    for table in tables:
        print(table)

if __name__ == '__main__':
    html = get_html(NPC_URL)
    save_html(html, 'html/npcs.html')
    get_npcs(html)
