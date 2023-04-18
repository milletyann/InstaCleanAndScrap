import pandas as pd
import csv

import random as rd
import time

################################################
##################### DOC ######################
################################################
##
## retrieve all comments one single time
##

comments = pd.read_csv("db_posts_elague.csv")
captions = comments["content"]

print(captions.head())

i = 0
single_captions = []
for cap in captions:
    single_captions.append(cap)

single_captions = list(set(single_captions))

captions_unique = pd.DataFrame(single_captions)
print(captions_unique)
captions_unique.to_csv("captions_unique.csv", index=False)
