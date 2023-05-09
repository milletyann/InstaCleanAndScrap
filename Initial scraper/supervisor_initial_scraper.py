# Selenium imports
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver as wd

# Common imports
from datetime import datetime, timedelta
from random import randint
from time import sleep
import urllib.parse
import requests
import base64
import json
import os

# Personal imports
from utils.faceDetection import loadImage, detectAndDisplay
from utils.error_gestion import manage_error
from utils.request import makeRequest
from supervisor_initial_config import *


def shortcode_to_id(shortcode):
    code = ("A" * (12 - len(shortcode))) + shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b"-_"), "big")


class igScraper:
    def __init__(self):
        self._base_url = "https://www.instagram.com/"
        self._graphql_url = self._base_url + "graphql/query/"
        self._wait_delay = 30
        self._like_wait_delay = 5
        self._store_folder = "test_data"
        # Create chromedriver with required options (speed purpose)
        # Disabling image loading is the best way to speed up the process
        options = wd.ChromeOptions()
        # options.add_experimental_option('prefs', {
        #     'profile.managed_default_content_settings.images': 2
        # })
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        self._driver = wd.Chrome(service=Service(WEBDRIVER), options=options)
        self._driver.set_window_position(400, 0)
        self._driver.set_window_size(1100, 750)

    def _signIn(self, username, password, retry=1, max_retries=10):
        try:
            self._driver.delete_all_cookies()
            self._driver.get(self._base_url)
            # Allow cookies
            WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
                    )
                )
            ).click()
            # Fill username input
            WebDriverWait(self._driver, 2).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input",
                    )
                )
            ).send_keys(username)
            # Fill password input
            WebDriverWait(self._driver, 2).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input",
                    )
                )
            ).send_keys(password)
            # Click submit button
            WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button",
                    )
                )
            ).click()
            try:
                # Allow 2nd cookies
                WebDriverWait(self._driver, 2).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[4]/div/div/button[2]")
                    )
                ).click()
            except Exception:
                pass
            try:
                # Remember me
                WebDriverWait(self._driver, 2).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/section/main/div/div/div/div/button",
                        )
                    )
                ).click()
            except Exception:
                pass
            try:
                # Disable notifications
                WebDriverWait(self._driver, 2).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]",
                        )
                    )
                ).click()
            except Exception:
                pass
        except Exception as e:
            manage_error(e)
            if retry < max_retries:
                self._signIn(username, password, retry=retry + 1)
            else:
                exit()

    def _signOut(self):
        WebDriverWait(self._driver, self._wait_delay).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span",
                )
            )
        ).click()
        WebDriverWait(self._driver, self._wait_delay).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div",
                )
            )
        ).click()

    def _checkProfile(self, name):
        articles = []
        self._driver.get(self._base_url + name)
        for i in range(0, NB_SCROLLS):
            print(f"SCROLL n°{i}")
            # Scroll to the bottom of the page to load new articles
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # Wait for articles to load
            sleep(3)
            try:
                articles.extend(
                    [
                        div.find_element(By.TAG_NAME, "a").get_attribute("href")
                        for div in self._driver.find_elements(
                            By.CLASS_NAME, "_aabd._aa8k._al3l"
                        )
                    ]
                )
            except Exception as e:
                manage_error(e)
        # print('LIST OF ARTICLES:', articles)
        return list(dict.fromkeys(articles))

    def _getNbLikes(self):
        views = 0
        # instagram html is slightly different wether it's a video or a picture
        try:  # picture
            nb_likes = int(
                WebDriverWait(self._driver, self._like_wait_delay)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div[3]/section/div/div/div/a/div/span",
                        )
                    )
                )
                .text.encode("ascii", "ignore")
            )
            media_type = "picture #1"
            print("Number of like #1")
        except Exception:  # video
            try:
                #                WebDriverWait(self._driver, self._like_wait_delay).until(
                #                    EC.element_to_be_clickable(
                #                        (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span')
                #                    )
                #                ).click()
                nb_likes = int(
                    WebDriverWait(self._driver, self._like_wait_delay)
                    .until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span",
                            )
                        )
                    )
                    .text.encode("ascii", "ignore")
                )
                media_type = "video"
                print("Number of like #2")
            except Exception:
                try:
                    nb_likes = int(
                        WebDriverWait(self._driver, self._like_wait_delay)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span",
                                )
                            )
                        )
                        .text.replace(",", "")
                        .replace(" ", "")
                    )
                    media_type = "video"
                except Exception:
                    try:
                        nb_likes = int(
                            WebDriverWait(self._driver, self._like_wait_delay)
                            .until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span",
                                    )
                                )
                            )
                            .text.encode("ascii", "ignore")
                        )
                        media_type = "Picture + left side toolbar#1"
                    except Exception:
                        try:
                            nb_likes = int(
                                WebDriverWait(self._driver, self._like_wait_delay)
                                .until(
                                    EC.presence_of_element_located(
                                        (
                                            By.XPATH,
                                            "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span",
                                        )
                                    )
                                )
                                .text.encode("ascii", "ignore")
                            )
                            media_type = "Picture + left side toolbar#2"
                        except Exception:
                            try:
                                nb_likes = 0
                                views = int(
                                    WebDriverWait(self._driver, self._like_wait_delay)
                                    .until(
                                        EC.presence_of_element_located(
                                            (
                                                By.XPATH,
                                                "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span/div/span",
                                            )
                                        )
                                    )
                                    .text.encode("ascii", "ignore")
                                )
                                media_type = "video + left side toolbar #1"
                            except Exception:
                                try:
                                    nb_likes = 0
                                    views = int(
                                        WebDriverWait(
                                            self._driver, self._like_wait_delay
                                        )
                                        .until(
                                            EC.presence_of_element_located(
                                                (
                                                    By.XPATH,
                                                    "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span",
                                                )
                                            )
                                        )
                                        .text.encode("ascii", "ignore")
                                    )
                                    media_type = "video + left side toolbar #2"
                                except Exception:
                                    try:
                                        nb_likes = 0
                                        views = int(
                                            WebDriverWait(
                                                self._driver, self._like_wait_delay
                                            )
                                            .until(
                                                EC.presence_of_element_located(
                                                    (
                                                        By.XPATH,
                                                        "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span/div/span",
                                                    )
                                                )
                                            )
                                            .text.encode("ascii", "ignore")
                                        )
                                        media_type = "video + left side toolbar #3"
                                    except Exception:
                                        print("!!!!!!! No likes !!!!!!!!!!")
                                        nb_likes = 0
                                        media_type = "!!!!!!!!!! unknown !!!!!!!!!!"
        except Exception as e:
            manage_error(e)
            return 0
        print(f"{nb_likes} likes ({media_type})")
        print(f"{views} views")
        return nb_likes, views

    def _scrapeLikes(self, shortcode, newspaper, download_images=False):
        retry, max_retries = 1, 5
        likes = []
        nb_likes, views = self._getNbLikes()
        if not nb_likes:
            return likes, nb_likes, views
        # Cookies are mandatory in order to get a 200 response
        gc = self._driver.get_cookie
        cookie = f"mid={gc('mid')['value']}; ig_did={gc('ig_did')['value']}; csrftoken={gc('csrftoken')['value']}; ds_user_id={gc('ds_user_id')['value']}; sessionid={gc('sessionid')['value']}; rur={gc('rur')['value']}"
        processed_likes = 0
        after_cursor = ""
        while processed_likes < nb_likes:
            while True:
                try:
                    # You can request 50 first likes after a cursor (optional)
                    nb = (
                        50
                        if processed_likes + 50 <= nb_likes
                        else nb_likes - processed_likes
                    )
                    print(f"{processed_likes + nb}/{nb_likes}")
                    likes_url = self._graphql_url + urllib.parse.quote(
                        f'?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={{"shortcode":"{shortcode}","include_reel":false,"first":{nb},"after":"{after_cursor}"}}',
                        safe="?/=&",
                    )
                    # Retrieve data
                    data = makeRequest(likes_url, cookies=cookie)
                    for node in data["data"]["shortcode_media"]["edge_liked_by"][
                        "edges"
                    ]:
                        faces = {"front": 0, "profile": 0, "eyes": 0, "path": None}
                        try:
                            filepath = f"{PIC_DIRECTORY}/{newspaper}~{node['node']['id']}~{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.jpg"
                            with open(filepath, "wb") as file:
                                file.write(
                                    requests.get(
                                        node["node"]["profile_pic_url"],
                                        stream=True,
                                        timeout=15,
                                    ).content
                                )
                            img = loadImage(filepath)
                            if img is not None:
                                faces = detectAndDisplay(img, display=False)
                                faces["path"] = filepath
                            if not download_images:
                                os.remove(filepath)
                        except Exception as e:
                            manage_error(e)
                        node["faces"] = faces
                        likes.append(node)
                    # Get the cursor of the last like of the request
                    after_cursor = data["data"]["shortcode_media"]["edge_liked_by"][
                        "page_info"
                    ]["end_cursor"]
                    print(f"{processed_likes + nb}/{nb_likes}")
                    processed_likes += nb
                    if processed_likes >= MAX_LIKES:
                        print(f"{MAX_LIKES} likes limit reached !")
                        return likes, nb_likes, views
                    # Don't spam the endpoint -> wait {delay} second(s) before making a new call
                    delay = randint(2, 4)
                    print(f"Waiting for {delay} second(s)...")
                    sleep(delay)
                    # Exit the inner loop if everything went well
                    break
                # If an error occurs, retry the loop iteration after refreshing cookies
                except Exception as e:
                    manage_error(e)
                    if retry < max_retries:
                        # Wait for {delay} sec before sending other requests, we might be getting 429 errors (too many requests)
                        delay = 180
                        print(f"Waiting for {delay} seconds...")
                        sleep(delay)
                        # Refreshing cookies
                        cookie = f"mid={gc('mid')['value']}; ig_did={gc('ig_did')['value']}; csrftoken={gc('csrftoken')['value']}; ds_user_id={gc('ds_user_id')['value']}; sessionid={gc('sessionid')['value']}; rur={gc('rur')['value']}"
                        retry += 1
                        continue
                    else:
                        retry = 1
                        break
        return likes, nb_likes, views

    def _getFirstComments(self, shortcode, post_id, headers, delay):
        first_call_url = f"https://i.instagram.com/api/v1/media/{post_id}/comments/?can_support_threading=true&permalink_enabled=false"
        try:
            r = makeRequest(first_call_url, headers=headers)
        except Exception as e:
            manage_error(e)
            print(f"Waiting for {delay} seconds...")
            sleep(delay)
            self._getFirstComments(shortcode, post_id, headers, delay)
        return r

    def _scrapeComments(self, shortcode):
        # This function uses the same process as _scrapeLikes
        delay = 180
        retry, max_retries = 1, 5
        gc = self._driver.get_cookie
        post_id = shortcode_to_id(shortcode)
        cookie = f"mid={gc('mid')['value']}; ig_did={gc('ig_did')['value']}; csrftoken={gc('csrftoken')['value']}; ds_user_id={gc('ds_user_id')['value']}; sessionid={gc('sessionid')['value']}; rur={gc('rur')['value']}"
        headers = [
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
                "cookie": cookie,
                "x-ig-app-id": "936619743392459",
                "x-ig-www-claim": "hmac.AR3hRu0gALaEykywFwKw7__BS7gkup4_U0HrFnabNKEYsrNO",
            }
        ]
        r = self._getFirstComments(shortcode, post_id, headers, delay)
        comment_count, nb_comments, comments = (
            r["comment_count"],
            len(r["comments"]),
            r["comments"],
        )
        while nb_comments < comment_count and "next_min_id" in r:
            while True:
                try:
                    bifilter_token = r["next_min_id"]
                    comments_url = (
                        f"https://i.instagram.com/api/v1/media/{post_id}/comments/"
                        + urllib.parse.quote(
                            f"?can_support_threading={True}&min_id={bifilter_token}",
                            safe="?/=&",
                        )
                    )
                    r = makeRequest(comments_url, headers=headers)
                    comments += r["comments"]
                    nb_comments += len(r["comments"])
                    # Don't spam the endpoint -> wait {delay} second(s) before making a new call
                    delay = randint(2, 6)
                    print(f"Waiting for {delay} second(s)...")
                    sleep(delay)
                    break
                except Exception as e:
                    manage_error(e)
                    if retry < max_retries:
                        # Wait for {delay} sec before sending other requests, we might be getting 429 errors (too many requests)
                        print(f"Waiting for {delay} seconds...")
                        sleep(delay)
                        # Refreshing cookies
                        cookie = f"mid={gc('mid')['value']}; ig_did={gc('ig_did')['value']}; csrftoken={gc('csrftoken')['value']}; ds_user_id={gc('ds_user_id')['value']}; sessionid={gc('sessionid')['value']}; rur={gc('rur')['value']}"
                        retry += 1
                        continue
                    else:
                        retry = 1
                        break
        print(f"Number of comments: {nb_comments}")
        return comments, nb_comments

    def _getDate(self):
        xpaths = [
            "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div[3]/div[2]/div/a/div/time",
            "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div/a/div/time",
        ]
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        for xpath in xpaths:
            try:
                date = (
                    WebDriverWait(self._driver, 2)
                    .until(EC.presence_of_element_located((By.XPATH, xpath)))
                    .get_attribute("datetime")
                    .replace(".000", "")
                )
                break
            except Exception:
                pass
        if not date:
            print("Unable to retrieve date")
        print(date)
        return date

    def _getName(self, newspaper):
        path = f"{self._store_folder}/{newspaper}"
        i = 0
        while True:
            filename = f"{path}/{newspaper}_{i}.json"
            if not os.path.exists(filename):
                return filename
            i += 1

    def _scrapeArticles(self, newspaper, articles):
        print(newspaper.upper(), f"({len(articles)} articles)")
        for link, i in zip(articles, range(1, len(articles) + 1)):
            try:
                if os.path.exists("blacklist"):
                    with open("blacklist", "r") as file:
                        blacklist = [
                            line.replace("\n", "") for line in file.readlines()
                        ]
                print(i, link)
                shortcode = list(filter(len, link.split("/")))[-1]
                # Don't scrape the same article several times
                if shortcode in blacklist:
                    print("-> ALREADY SCRAPED\n")
                    delay = randint(2, 4)
                    print(f"Waiting for {delay} second(s)...")
                    sleep(delay)
                    continue
                self._driver.get(link)
                date = self._getDate()
                article_timestamp = datetime.timestamp(
                    datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                )
                nb_days = timedelta(days=NB_DAYS)
                # If the article was posted less than one week ago, don't scrape it
                if datetime.timestamp(datetime.now() - nb_days) < article_timestamp:
                    print("-> POST IS TOO RECENT\n")
                    delay = randint(2, 4)
                    print(f"Waiting for {delay} second(s)...")
                    sleep(delay)
                    continue
                # If the article was posted before the {START_DATE}, don't scrape it
                if datetime.timestamp(START_DATE) > article_timestamp:
                    print("-> POST IS TOO OLD\n")
                    delay = randint(2, 4)
                    print(f"Waiting for {delay} second(s)...")
                    sleep(delay)
                    continue
                try:
                    post_content = (
                        WebDriverWait(self._driver, self._wait_delay)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div[2]/div/div/ul/div/li/div/div/div[2]/div[1]/h1",
                                )
                            )
                        )
                        .text
                    )
                    print("Content #1")
                except Exception:
                    try:
                        post_content = (
                            WebDriverWait(self._driver, self._wait_delay)
                            .until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1",
                                    )
                                )
                            )
                            .text
                        )
                        print("Content #2")
                    except Exception:
                        try:
                            post_content = (
                                WebDriverWait(self._driver, self._wait_delay)
                                .until(
                                    EC.presence_of_element_located(
                                        (
                                            By.XPATH,
                                            "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span",
                                        )
                                    )
                                )
                                .text
                            )
                            print("Content #3")
                        except Exception:
                            print("UNABLE TO RETRIEVE POST CONTENT, SKIPPING...")

                print(f"\n\nSCRAPING COMMENTS [{link}]\n")
                comments, nb_comments = self._scrapeComments(shortcode)
                print(f"\n\nSCRAPING LIKES [{link}]\n")
                likes, nb_likes, views = self._scrapeLikes(shortcode, newspaper)
                if nb_likes <= 0 and views <= 0:
                    continue
                filename = self._getName(newspaper)
                with open(filename, "w") as file:
                    json.dump(
                        {
                            "link": f"https://www.instagram.com/p/{shortcode}/",
                            "shortcode": shortcode,
                            "posted_at": date,
                            "scraped_at": datetime.now().isoformat(),
                            "content": post_content,
                            "nb_views": views,
                            "nb_likes": nb_likes,
                            "nb_comments": nb_comments,
                            "comments": comments,
                            "likes": likes,
                        },
                        file,
                        indent=1,
                    )
                with open("blacklist", "a") as file:
                    file.write(f"{shortcode}\n")
            except Exception as e:
                manage_error(e)

    def run(self):
        minutes = 0.1
        if not os.path.exists(f"{self._store_folder}"):
            os.mkdir(f"{self._store_folder}")
        if not os.path.exists(PIC_DIRECTORY):
            os.mkdir(PIC_DIRECTORY)
        self._signIn(USERNAME, PASSWORD)
        for newspaper in NEWSPAPERS[MODE]:
            try:
                if not os.path.exists(f"{self._store_folder}/{newspaper}"):
                    os.mkdir(f"{self._store_folder}/{newspaper}")
                articles = self._checkProfile(newspaper)
                self._scrapeArticles(newspaper, articles)
                # Disconnect before waiting {minutes} minutes
                print("sign out")
                self._signOut()
                # Sleeping to mimic a human behavior
                print(f"Waiting for {minutes} minutes...")
                sleep(60 * minutes)
                # Sign in again after the sleep
                self._signIn(USERNAME, PASSWORD)
            except Exception as e:
                manage_error(e)


if __name__ == "__main__":
    s = igScraper()
    s.run()
