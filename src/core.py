import bs4
import json
import requests


def get_html(url):
    """
    Get the HTML from a URL.
    
    :param url: The URL to get the HTML from.
    :return: The HTML from the URL.
    """

    response = requests.get(url)
    return response.text

def save_html(html: str, file_name: str):
    """
    Save HTML to a file.

    :param html: The HTML to save.
    :param file_name: The path to save the HTML to.
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')
    pretty_html = soup.prettify()

    with open(f'html/{file_name}', 'w', encoding='utf-8') as file:
        file.write(pretty_html)
    
def save_json(data: dict, file_name: str):
    """
    Save JSON to a file.

    :param data: The JSON to save.
    :param file_name: The path to save the JSON to.
    """

    with open(f'json/{file_name}', 'w') as file:
        json.dump(data, file, indent=4)
