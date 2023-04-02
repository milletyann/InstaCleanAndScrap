import pandas as pd

""" enlever les lignes vraiment inutiles
df = pd.read_stata("dataset.dta")

df.drop(
    [
        "commentscreated_at",
        "commentscontent_type",
        "commentsstatus",
        "commentsbit_flags",
        "commentsshare_enabled",
        "commentsuserpk",
        "commentsuserprofile_pic_url",
        "commentsuserprofile_pic_id",
        "commentsuserfollow_friction_type",
        "commentsuseris_mentionable",
        "commentsuserlatest_reel_media",
        "commentsuserlatest_besties_reel_",
        "commentsuserfacescount",
        "commentsuserfacesconfidence",
        "commentsis_covered",
        "commentshas_liked_comment",
        "commentspreview_child_comments",
        "commentsother_preview_users",
        "commentsinline_composer_display_",
        "commentsprivate_reply_status",
        "commentsis_liked_by_media_owner",
        "commentsother_preview_usersid",
        "commentsother_preview_usersprofi",
        "commentsnum_tail_child_comments",
        "commentshas_more_tail_child_comm",
        "commentshas_more_head_child_comm",
        "commentsusergrowth_friction_info",
        "commentsother_preview_users0id",
        "commentsother_preview_users0prof",
        "commentsother_preview_users1id",
        "commentsother_preview_users1prof",
        "commentsuseraccount_badges",
        "commentspreview_child_commentsco",
        "commentspreview_child_commentsus",
        "commentspreview_child_commentspk",
        "commentspreview_child_commentste",
        "commentspreview_child_commentsty",
        "commentspreview_child_commentscr",
        "commentspreview_child_commentsme",
        "commentspreview_child_commentsst",
        "commentspreview_child_commentspa",
        "commentspreview_child_commentssh",
        "commentspreview_child_commentspr",
        "commentspreview_child_commentsha",
        "commentsnext_min_child_cursor",
        "commentsnum_head_child_comments",
        "commentspreview_child_comments0c",
        "commentspreview_child_comments0u",
        "commentspreview_child_comments0p",
        "commentspreview_child_comments0t",
        "commentspreview_child_comments0m",
        "commentspreview_child_comments0s",
        "commentspreview_child_comments0h",
        "commentsnext_max_child_cursor",
        "commentshas_translation",
        "commentsuserpk_id",
        "commentsother_preview_users2id",
        "commentsother_preview_users2prof",
        "commentsother_preview_users3id",
        "commentsother_preview_users3prof",
        "commentscomment_social_context_l",
        "commentspreview_child_commentsch",
        "commentspreview_child_comments0i",
        "commentsuserfbid_v2",
        "commentspreview_child_commentsis",
        "diff_post_comment_second",
        "_merge",
    ],
    axis=1,
    inplace=True,
)
df.to_csv("db_posts_elague.csv", index=False)
"""

### ne garder que les légendes et les commentaires
df_elague = pd.read_csv("db_posts_elague.csv")

print(df_elague.columns)
print(df_elague.head())


def is_convertible_to_number(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
            float(s)
            return True
        except ValueError:
            return False


def isalphanum(string):
    dic = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "-",
        "_",
    ]
    l = []
    for char in string:
        if not (char in dic):
            return False
    return True


def clean(dataframe):
    to_del = []

    for index, line in dataframe.iterrows():
        if not (isalphanum(line["link"])):
            # test de type colonne "link"
            print("[ERROR] Line {}. Not alphanum {}".format(str(index), line["link"]))
            r = input("Delete the entry? [Y/n] ")
            if r == "Y":
                to_del.append(index)
        elif not (is_convertible_to_number(line["nb_likes"])):
            # test de type colonne "nb_likes"
            print(
                "[ERROR] Line {}. Can't convert {} to type int or float".format(
                    str(index), line["nb_likes"]
                )
            )
            r = input("Delete the entry? [Y/n] ")
            if r == "Y":
                to_del.append(index)
        else:
            print("[SUCCESS] Number of likes is Integer: {}".format(line["nb_likes"]))

    for i in to_del:
        print("Deleting row ".format(i))
    dataframe.drop(to_del, inplace=True)
    print("[SUCCESS] Cleaning column LINK")

    # test colonnes numériques
    to_del = []


# clean(df_elague)
"""
caption_et_comment = df_elague.drop(
    [
        "link",
        "nb_likes",
        "nb_views",
        "posted_at",
        "scraped_at",
        "nb_comments",
        "commentspk",
        "insta_id",
        "commentstype",
        "commentscreated_at_utc",
        "commentsdid_report_as_spam",
        "username",
        "full_name",
        "private_acc",
        "verified_acc",
        "comment_like_count",
        "comment_child_count",
        "newspaper",
        "commentscomment_index",
        "commentsis_ranked_comment",
        "commentsuseraccount_type",
        "type",
        "post_hour",
        "post_day",
        "scrap_hour",
        "scrap_day",
        "comment_hour_utc",
        "comment_hour",
        "comment_day",
    ],
    axis=1,
)
caption_et_comment.to_csv("db_captions_and_comments.csv", index=False)
"""

""" sortir un sample de légendes et de commentaires pour Sakaya
df_samples = pd.read_csv("db_captions_and_comments.csv")
print(df.head())


sample_df = df_samples.sample(n=1000)
sample_df.to_csv("sample4sak.csv")
"""
