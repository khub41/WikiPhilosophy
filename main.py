import time
import requests
from bs4 import BeautifulSoup


def get_first_link(url):
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
    for div in soup.find_all('div', class_="infobox"):
        div.decompose()
    for table in soup.find_all("table"):
        table.decompose()
    for sup in soup.find_all("sup", class_="prononciation"):
        sup.decompose()
    for span in soup.find_all("span", class_="API"):
        span.decompose()
    for a in soup.find_all("a", class_="extiw"):
        a.decompose()

    # Selecting links that are in a paragraph whithin the main info container mw-context-text
    allLinks = soup.find(id="mw-content-text").select("p a[href]")


    for link in allLinks:
        # We are only interested in other wiki articles
        if link['href'].find("/wiki/") != -1:
            first_link = link
            return first_link

def main():

    language = 'fr'
    philo_dict = {'fr': 'Philosophie', 'en': 'Philosophy', 'es': 'Filosofía'}
    starting_article = "Aérodrome_de_Fayence_-_Tourrettes"
    print(f"Starting from {starting_article}")
    url = f"https://{language}.wikipedia.org/wiki/{starting_article}"
    distance = 0

    while True:
        new_article = get_first_link(url)
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