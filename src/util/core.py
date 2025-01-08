from logging import Logger
import bs4
import json
import logging
import os
import requests


def get_html(url: str, retries: int, logger: Logger) -> str:
    """
    Get the HTML from a URL.

    :param url: The URL to get the HTML from.
    :param retries: The number of retries to try getting the HTML.
    :param logger: The logger to log with.
    :return: The HTML from the URL.
    """

    for i in range(retries):
        try:
            logger.log(logging.INFO, f"Attempt {i + 1}: Getting HTML from {url}")
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.log(logging.ERROR, f"Attempt {i + 1}: Failed to get HTML from {url}")
            logger.log(logging.ERROR, e)

    logger.log(logging.ERROR, f"Failed to get HTML from {url} after {retries} attempts")
    exit(1)


def save_html(html: str, file_name: str, logger: Logger):
    """
    Save HTML to a file.

    :param html: The HTML to save.
    :param file_name: The path to save the HTML to.
    :param logger: The logger to log with.
    :return: None
    """

    logger.log(logging.INFO, f"Formatting HTML to save to {file_name}")
    soup = bs4.BeautifulSoup(html, "html.parser")
    pretty_html = soup.prettify()

    logger.log(logging.INFO, f"Saving HTML to {file_name}")
    try:
        os.makedirs("html", exist_ok=True)
        with open(f"html/{file_name}", "w", encoding="utf-8") as file:
            file.write(pretty_html)
            logger.log(logging.INFO, f"Saved HTML to {file_name}")
    except Exception as e:
        logger.log(logging.ERROR, f"Failed to save HTML to {file_name}")
        logger.log(logging.ERROR, e)


def save_json(data: dict, file_name: str, logger: Logger):
    """
    Save JSON to a file.

    :param data: The JSON to save.
    :param file_name: The path to save the JSON to.
    :param logger: The logger to log with.
    :return: None
    """

    logger.log(logging.INFO, f"Saving JSON to {file_name}")
    try:
        os.makedirs("json", exist_ok=True)
        with open(f"json/{file_name}", "w") as file:
            json.dump(data, file, indent=4)
            logger.log(logging.INFO, f"Saved JSON to {file_name}")
    except Exception as e:
        logger.log(logging.ERROR, f"Failed to save JSON to {file_name}")
        logger.log(logging.ERROR, e)
