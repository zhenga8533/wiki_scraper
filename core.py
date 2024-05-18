import bs4
import requests


def get_html(url):
    """
    Get the HTML from a URL.
    
    :param url: The URL to get the HTML from.
    :return: The HTML from the URL.
    """

    response = requests.get(url)
    return response.text

def save_html(html: str, file_path: str):
    """
    Save HTML to a file.

    :param html: The HTML to save.
    :param file_path: The path to save the HTML to.
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')
    pretty_html = soup.prettify()

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_html)
