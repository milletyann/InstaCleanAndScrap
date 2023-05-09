from datetime import datetime

# Chrome webdriver
WEBDRIVER = "chromedriver.exe"

# instagram credentials

# 429: 29/10  10:00
# Phone number: perso
USERNAME = SET_YOUR_OWN
PASSWORD = SET_YOUR_OWN


# Number of scrolls the scraper will perform before retrieving the posts
NB_SCROLLS = 8
# Number days for a post to be scraped after its publication date
NB_DAYS = 7
# Maximum likes we can scrape
MAX_LIKES = 20_000
# Posts older than this date won't be scraped
# datetime(year, month, day, hour, minute, second)
START_DATE = datetime(2022, 1, 23)

# Directory where profile pictures will be downloaded
PIC_DIRECTORY = "profile_pictures"

# MODE = 'DEV'
MODE = "PROD"

NEWSPAPERS = {
    "DEV": [
        "buzzfeed",
        "brutofficiel",
        "vice_france",
        "ajplusfrancais",
        "slatefrance",
        "mediapart",
        "mariannelemag",
        "valeurs_actuelles",
        "charlie_hebdo_officiel",
        "scienceetvie",
        "latribune_news",
        "letudiant_",
        "francesoirfr",
        "lepointfr",
        "courrierinter" "lemondefr",
        "lesechos",
        "liberationfr",
        "LeParisien",
        "lefigarofr",
        "parismatch_magazine",
        "closeronline",
        "publicfr",
        "galafr",
        "pointdevue",
        "lequipe",
        "autoplusmag",
        "francefootball",
        "midi.olympique",
        "velo.magazine",
        "moto_magazine_france",
        "madamefigarofr",
        "marieclairefr",
        "ellefr",
        "cosmopolitan_fr",
        "femme_actuelle",
        "santemagazine",
        "tf1",
        "europe1",
        "m6officiel",
        "rtl_france",
        "20minutesfrance",
        "bfmtv",
        "lobs",
        "cnewsofficiel",
        "lhumanitefr",
        "lexpressfr",
        "closer_france",
        "voici",
    ],
    "PROD": ["lequipe"],
}


# Newspapers list:

# autoplusmag
# ellefr
# enduromag_officiel
# femme_actuelle
# galafr
# lefigarofr
# lemondefr
# lequipe
# lesechos
# lhumanitefr
# liberationfr
# madamefigarofr
# marieclairefr
# midi.olympique
# onzemondial
# parismatch
# pointdevue
# Psychologies_
# publicfr
# purepeople
# santeplusmag
# sofoot
# valeurs_actuelles
# voici


ERROR_FILE = f"errors/{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.log"
