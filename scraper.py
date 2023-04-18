import instaloader
import csv
import pandas as pd
from os.path import exists
import random as rd
import time
from selenium import webdriver

SCRAP_FINISHED = False
BATCH_SIZE = 50


def download_instagram_post(shortcode):
    L = instaloader.Instaloader()

    SHORTCODE = shortcode
    post = instaloader.Post.from_shortcode(L.context, SHORTCODE)

    L.dirname_pattern = "media/{target}"

    target = str(SHORTCODE)
    L.download_post(post, target=target)


def sleep_time(x, a, b):
    # [a, b] is an interval of second for the
    return x * (b - 1) + a


""" pour fabriquer le csv des liens pas encore scrapés
# read the cleaned dataset
data = pd.read_csv("cleaned.csv")
# isolate link column
shortcodes = data["link"]
# convert it to list and remove doubles
shortcodes = list(set(shortcodes.tolist()))
# convert it back to dataframe
shortcodes = pd.DataFrame({"link": shortcodes})
# save it to csv
shortcodes.to_csv("still_to_scrap.csv", index=False)

shortcodes = pd.read_csv(("still_to_scrap.csv"))
shortcodes = shortcodes["link"].tolist()

i = 0
for link in shortcodes:
    path = "media/" + str(link)
    if exists(path):
        i += 1
        print("on l'a déjà scrap donc ça dégage, c'est le {}ème".format(i))
        shortcodes.remove(link)
    else:
        continue

# convert to dataframe
shortcodes = pd.DataFrame({"link": shortcodes})
# save it to csv
shortcodes.to_csv("still_to_scrap.csv", index=False)
# """

# read csv
shortcodes = pd.read_csv("still_to_scrap.csv")
# convert to list
shortcodes = shortcodes["link"].tolist()

# while not SCRAP_FINISHED:
#     try:
#         # scrap a batch of posts in shortcodes
#         for i in range(BATCH_SIZE):
#             time_to_wait = sleep_time(rd.random(), 1, 1)
#             download_instagram_post(shortcodes[0])
#             links.remove(shortcodes[0])
#             sleep(time_to_wait)
#         # convert to dataframe
#         shortcodes = pd.DataFrame(shortcodes, columns=["link"])
#         # save to csv
#         shortcodes.to_csv("still_to_scrap.csv")
#         SCRAP_FINISHED = True
#     except:
#         print("merde ça plante")
#         # update the csv not to scrap again the beginning of the batch again
#         shortcodes = pd.DataFrame(shortcodes, columns=["link"])
#         shortcodes.to_csv("still_to_scrap.csv")

#     if not SCRAP_FINISHED:
#         r = input("Scrap not finished, want to continue? [Y/n] ")
#     if r != "Y":
#         break


# setup the driver
driver = webdriver.Chrome()

# test shortcode
shortcode = "BvDpDh6lFjH"
