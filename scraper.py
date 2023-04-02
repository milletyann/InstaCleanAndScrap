import instaloader
import csv

FEATURE_DIC = {
    "link": 0,
    "nb_likes": 1,
    "nb_views": 2,
    "posted_at": 3,
    "content": 5,
    "nb_comments": 6,
    "comment_text": 9,
    "username": 19,  # de la personne qui commente
}


def download_instagram_post(shortcode):
    L = instaloader.Instaloader()

    # .split récupère le shortcode du post et crée le post (récupéré grâce à son shortcode)
    SHORTCODE = shortcode
    post = instaloader.Post.from_shortcode(L.context, SHORTCODE)

    OWNER_USERNAME = post.owner_username
    # get_sidecar_nodes
    print(post.get_sidecar_nodes())

    target = str(OWNER_USERNAME) + "_" + str(SHORTCODE)
    L.download_post(post, target=target)


def retrieve_data(file_link, newline="", feature_dict=False):
    # feature_dict is a boolean that takes into account the feature dictionnary or not, for simplifying purposes
    with open("db_posts.csv", newline="") as data:
        reader = csv.reader(data, delimiter=",")

        data = []
        line = []
        few_features = list(FEATURE_DIC.values())
        print(few_features)
        max = 20
        for row in reader:
            if max > 0:
                print("--------------")
                print("Nouvelle ligne")
                print("Elle fait " + str(len(row)) + " feature")
                if len(row) != 98:
                    print("La ligne ne fait pas 98 feature, on la skip")
                    # data incomplete, skip this line
                    continue
                if feature_dict:
                    print("")
                    for i in few_features:
                        print("")
                        print("On ajoute la feature n°" + str(i))
                        print("La ligne possède " + str(len(row)) + "features")
                        print("On prend donc celle-ci: " + str(row[i]))
                        line.append(row[i])
                    data.append(line)
                else:
                    data.append(row)

                #                print("")
                #               input("On continue sur une nouvelle ligne? ")
                #              print("")
                max -= 1
            else:
                return data
        # return data


def find_index(feature):
    ### pour faciliter la récupération de l'index d'une feature
    index = 0
    l = len(data[0])
    for i in range(l):
        if data[0][i] != feature:
            index += 1
        else:
            return index
    return "pas trouvé dsl"


def save(data):
    with open("clean.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for row in data:
            writer.writerow(row)


data = retrieve_data("db_posts.csv", feature_dict=True)
save(data)

# links = []

# l = len(links)
# for i in range(l):
#    download_instagram_post(links[i])
