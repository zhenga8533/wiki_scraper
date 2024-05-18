from bs4 import BeautifulSoup
from core import *
from constants import *


def get_titles(html: str) -> list:
    titles = []

    soup = BeautifulSoup(html, 'html.parser')
    blockquotes = soup.find_all('blockquote')
    for blockquote in blockquotes:
        links = blockquote.find_all('a')
        for link in links:
            titles.append(link.get_text(strip=True))
    return titles

def get_locations(titles: list):
    locations = {}

    for title in titles:
        # Get the HTML and create a BeautifulSoup object from it
        location = {}
        location_url = f'{BASE_URL}/{title}'
        html = get_html(location_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the span tag with id="Zones"
        span_zones = soup.find('span', id='Zones')
        if span_zones is None:
            continue

        # Find the zones table
        table = span_zones.parent.find_next_sibling('table', {'class': 'wikitable'})
        if table is None:
            continue

        # Find the coordinates column
        header_row = table.find_all('tr')[0]
        headers = [th.get_text(strip=True).lower() for th in header_row.find_all('th')]
        coord_index = headers.index('coordinates') if 'coordinates' in headers else None
        if coord_index is None:
            continue

        # Find the zones and their coordinates
        rows = table.find_all('tr')[2:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < coord_index + 3:
                continue

            zone_name = cols[0].get_text(strip=True)
            x = cols[coord_index + 0].get_text(strip=True)
            y = cols[coord_index + 1].get_text(strip=True)
            z = cols[coord_index + 2].get_text(strip=True)
            location[zone_name] = [x, y, z]
        
        # Add the location to the locations dictionary
        locations[title] = location

    return locations

if __name__ == '__main__':
    html = get_html(LOCATION_URL)
    titles = get_titles(html)
    locations = get_locations(titles)
    save_json(locations, 'locations.json')
