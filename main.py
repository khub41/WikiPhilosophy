import time
import requests
from bs4 import BeautifulSoup


def get_first_link(url, language):
    # Getting response
    try:
        response = requests.get(
            url=url,
        )
    except:
        print("Sleeping to avoid overload...")
        time.sleep(10)

    # Converting into Soup obj
    soup = BeautifulSoup(response.content, 'html.parser')

    # I want to ignore the bandeau containers
    for div in soup.find_all('div', class_="bandeau-container"):
        div.decompose()
    # IDEM for infoboxes
    for div in soup.find_all('div', class_="infobox"):
        div.decompose()
    # IDEM for tables
    for table in soup.find_all("table"):
        table.decompose()
    # IDEM for prononciation
    for sup in soup.find_all("sup", class_="prononciation"):
        sup.decompose()
    # IDEM for phonetics blocks
    alphabet_acronym = {'fr': 'API', 'en': 'IPA', 'es': 'IPA'}
    for span in soup.find_all("span", class_=alphabet_acronym[language]):
        span.decompose()
    # IDEM for some bad links not leading to a proper wiki page
    for a in soup.find_all("a", class_="extiw"):
        a.decompose()

    # Selecting links that are in a paragraph whithin the main info container mw-context-text
    allLinks = soup.find(id="mw-content-text").select("p a[href]")

    latin_dict = {'fr': 'Latin', 'en': 'Latin', 'es': 'Lat%C3%ADn'}
    greek_dict = {'fr': 'Grec', 'en': 'Greek_language', 'es': 'Idioma_griego'}
    for link in allLinks:
        # We are only interested in other wiki articles
        if link['href'].find("/wiki/") != -1:
            if link['href'].split('/wiki/')[1] != latin_dict[language] and \
                    link['href'].split('/wiki/')[1] != greek_dict[language]:
                first_link = link
                return first_link

def main():

    language = 'fr'
    philo_dict = {'fr': 'Philosophie', 'en': 'Philosophy', 'es': 'Filosofía'}
    starting_article = "Systeme"
    print(f"Starting from {starting_article}")
    url = f"https://{language}.wikipedia.org/wiki/{starting_article}"
    distance = 0

    while True:
        new_article = get_first_link(url, language)
        new_article_wiki_adress = new_article['href'].split('/wiki/')[1]
        print(f"Going through {new_article.text}")
        distance += 1
        if new_article_wiki_adress == philo_dict[language]:
            print(f"Success, we reached {philo_dict[language]} in {distance} round(s) from the Article {starting_article}")
            break
        else:
            url = f"https://{language}.wikipedia.org/wiki/{new_article_wiki_adress}"


if __name__ == "__main__":
    main()