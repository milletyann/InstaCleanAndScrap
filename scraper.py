import instaloader
import csv
import pandas as pd
from os.path import exists


def download_instagram_post(shortcode):
    L = instaloader.Instaloader()

    SHORTCODE = shortcode
    post = instaloader.Post.from_shortcode(L.context, SHORTCODE)

    L.dirname_pattern = "media/{target}"

    target = str(SHORTCODE)
    L.download_post(post, target=target)


def scrap(links, batch_size=100):
    for i in range(batch_size):
        download_instagram_post(links[0])
        links.remove(links[0])


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
print(shortcodes[:10])

i = 0
for link in shortcodes:
    path = "media/" + str(link)
    print(path)
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
"""

# read csv
shortcodes = pd.read_csv("still_to_scrap.csv")
# convert to list
shortcodes = shortcodes["link"].tolist()

try:
    # scrap a batch of posts in shortcodes
    scrap(shortcodes, batch_size=50)
except:
    # update the csv not to scrap again the beginning of the batch again
    shortcodes = pd.DataFrame({"link": shortcodes})
    shortcodes.to_csv("still_to_scrap.csv")

# convert to dataframe
shortcodes = pd.DataFrame({"link": shortcodes})
# save to csv
shortcodes.to_csv("still_to_scrap.csv")
