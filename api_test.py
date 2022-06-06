import pandas as pd
import wikipediaapi
"""This scripts tests the Wikipedia API and tries to determine if it's a good idea to use it whithin this project"""

language = 'fr'

wiki_obj = wikipediaapi.Wikipedia(language)

page_py = wiki_obj.page('Participation_au_capital')

def get_first_link(page, skip_parenthesis=False):
    links_labels_list = list(page.links.keys())
    text_low = page.text.lower()

    links_df = pd.DataFrame()
    links_df['links_labels'] = links_labels_list

    links_df['position'] = links_df.links_labels.apply(lambda link_label: text_low.find(link_label.lower()))

    links_df_core = links_df[links_df.position >= 0]
    links_df_core = links_df_core.sort_values(by='position', ascending=True)

    if not skip_parenthesis:
        return links_df_core.links_labels.values[0]

    else:
        pass


print(get_first_link(page_py))
# The problem here is that the name of the Wiki page (ie the /wiki/Name_page(_precision))
# is different of the text containing the link. This lead me to use a another method to avoid further problems. For now