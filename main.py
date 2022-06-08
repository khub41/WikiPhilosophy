import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def get_first_link(url, language):
    # Getting response
    try:
        response = requests.get(
            url=url,
        )
    except:
        try:
            logging.info(f"Sleeping 10s to avoid overload when reaching {url.split('/wiki/')[1]}...")
            time.sleep(10)
        except Exception as e:
            logging.WARNING(f"Failed to reach wiki page {url.split('/wiki/')[1]}")
            return None

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
    # Sometimes, in some very basic pages, links are inside a list
    if len(allLinks) == 0:
        allLinks = soup.find(id="mw-content-text").select("ul a[href]")

    latin_dict = {'fr': 'Latin', 'en': 'Latin', 'es': 'Lat%C3%ADn'}
    greek_dict = {'fr': 'Grec', 'en': 'Greek_language', 'es': 'Idioma_griego'}
    for link in allLinks:
        # We are only interested in other wiki articles and I prefer to skip greek and latin pages
        # that often present in the parenthesis at the beginning of the article
        if link['href'].find("/wiki/") != -1:
            if link['href'].split('/wiki/')[1] != latin_dict[language] and \
                    link['href'].split('/wiki/')[1] != greek_dict[language]:
                first_link = link
                return first_link


def get_path(starting_article, language, pandas_apply_mode=False):
    # When used with pandas apply, starting article is a row of a df and we need to get the name of the attribute
    if pandas_apply_mode:
        # here the attribute is called 'clean'
        starting_article = starting_article.clean

    # To get the algorythm to stop we need to detect if we arrived to the Philosophy page in the right language
    philo_dict = {'fr': 'Philosophie', 'en': 'Philosophy', 'es': 'Filosofía'}

    # Making the wiki url
    logging.info(f"Starting from {starting_article}")
    url = f"https://{language}.wikipedia.org/wiki/{starting_article}"

    # Init variables to track progress
    distance = 0
    path_to_philo = [starting_article]

    while True:
        # Getting the first link of the wiki page
        new_article = get_first_link(url, language)

        # When None, something bad happened, generally a bad link to a poorly made page
        if new_article is None:
            return path_to_philo, 'error_page', len(path_to_philo)
        logging.info(f"Going through {new_article.text}")
        # Getting the adress name from the link and the associated text in the current page
        new_article_wiki_adress = new_article['href'].split('/wiki/')[1]
        # Tracking progress
        distance += 1
        # Stopping if Philosophy has been reached
        if new_article_wiki_adress == philo_dict[language]:
            logging.info(f"Success, we reached {philo_dict[language]} in {distance} round(s) from the Article {starting_article}")
            return path_to_philo, 'success', len(path_to_philo)

        else:
            # Stopping if page has already been visited
            if new_article_wiki_adress in path_to_philo:
                logging.info(f"Failed, we reached a loop at {new_article_wiki_adress}")
                path_to_philo.append(new_article_wiki_adress)
                return path_to_philo, 'other_loop', len(path_to_philo)
            # Carry on, almost there Chidi!
            else:
                url = f"https://{language}.wikipedia.org/wiki/{new_article_wiki_adress}"
                path_to_philo.append(new_article_wiki_adress)


def process_pages():
    titles = pd.read_csv("data/all_titles_fr.csv",
                         usecols=['clean'],
                         nrows=1000000).sample(20, random_state=2019)
    print(titles.clean)
    titles[['path_to_philo', 'status', 'distance']] = titles.apply(get_path,
                                                       axis=1,
                                                       result_type='expand',
                                                       language='fr',
                                                       pandas_apply_mode=True)

    return titles


if __name__ == "__main__":
    paths = process_pages()
    paths['distance'] = paths.apply(lambda x: len(x.path_to_philo), axis=1)

    # res = get_path("Concept", 'fr')
