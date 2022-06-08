"""
From the file found at this adress: https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-all-titles.gz on 7th june 2022
This short script converts it into a df containing the URLs and saves it in csv
"""

import pandas as pd

all_titles_file = open("data/frwiki-latest-all-titles", 'r')
df = pd.DataFrame(all_titles_file.readlines(), columns=['raw'])
df['clean'] = df.raw.apply(lambda x : x.split("\t")[1].strip("\n"))
df.to_csv('data/all_titles_fr.csv')
