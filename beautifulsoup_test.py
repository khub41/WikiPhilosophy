"""Testing BeautifulSoup to get the first link of a Wiki Article"""

import requests
from bs4 import BeautifulSoup


def get_first_link(url):
    # Getting response
    response = requests.get(
        url=url,
    )
    # Converting into Soup obj
    soup = BeautifulSoup(response.content, 'html.parser')

    # I want to ignore the bandeau containers
    for div in soup.find_all('div', class_="bandeau-container"):
        div.decompose()

    # Selecting links that are in a paragraph whithin the main info container mw-context-text
    allLinks = soup.find(id="mw-content-text").select("p a[href]")


    for link in allLinks:
        # We are only interested in other wiki articles
        if link['href'].find("/wiki/") != -1:
            return link.attrs['href'].split("/wiki/")[1]

print(get_first_link("https://fr.wikipedia.org/wiki/Participation_au_capital"))