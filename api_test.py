"""This scripts tests the Wikipedia API and tries to determine if it's a good idea to
use it whithin this project"""

import pandas as pd
import wikipediaapi

#Getting a page from Wikipedia in a certain language
language = 'fr'
wiki_obj = wikipediaapi.Wikipedia(language)
page_py = wiki_obj.page('Participation_au_capital')

def get_first_link(page, skip_parenthesis=False):
    # Getting the links labels
    # The links are not in the right order which is a problem
    links_labels_list = list(page.links.keys())
    # putting it in a DF
    links_df = pd.DataFrame()
    links_df['links_labels'] = links_labels_list

    # Getting the text
    text_low = page.text.lower()

    # Getting position of the links in the text
    links_df['position'] = links_df.links_labels.apply(lambda link_label: text_low.find(link_label.lower()))

    # Filtering out links that were not found and sorting to get the first
    links_df_core = links_df[links_df.position >= 0]
    links_df_core = links_df_core.sort_values(by='position', ascending=True)

    # This arg is not yet developped because i'm not sure whether I'll use this library
    if not skip_parenthesis:
        return links_df_core.links_labels.values[0]
    else:
        print("skip_parenthesis arg is not developped yet, returning whithout skipping")
        return links_df_core.links_labels.values[0]

print(get_first_link(page_py))
# The problem here is that the name of the Wiki page (ie the /wiki/Name_page(_precision))
# is different of the text containing the link. This lead me to use a another method to avoid further problems. For now