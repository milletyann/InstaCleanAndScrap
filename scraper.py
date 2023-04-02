import instaloader
import csv
import pandas as pd


def download_instagram_post(shortcode):
    L = instaloader.Instaloader()

    # .split récupère le shortcode du post et crée le post (récupéré grâce à son shortcode)
    SHORTCODE = shortcode
    post = instaloader.Post.from_shortcode(L.context, SHORTCODE)

    L.dirname_pattern = "media/{target}"

    target = str(SHORTCODE)
    L.download_post(post, target=target)


def scrap(start_index, batch_size=100):
    for sc in shortcodes[start_index : start_index + batch_size]:
        download_instagram_post(sc)


data = pd.read_csv("cleaned.csv")

shortcodes = list(set(data["link"].tolist()))
scrap(400)
