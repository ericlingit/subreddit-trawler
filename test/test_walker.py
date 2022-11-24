import pickle
from typing import List

from bs4 import BeautifulSoup
from requests import Response

from subreddit_trawler.walker import collect_links, PostMetadata


def test_collect_links():
    with open("test/subreddit_China_irl.pickle", "rb") as fh:
        china_irl: Response = pickle.load(fh)
    soup = BeautifulSoup(china_irl.content, "lxml")

    pm: List[PostMetadata] = collect_links(soup)
    assert len(pm) == 25
    for p in pm:
        assert p.author != ""
        assert p.comments_count >= 0
        assert p.domain != ""
        assert p.id != ""
        assert p.permalink.startswith("https://old.reddit.com/r/China_irl")
        assert p.timestamp > 1660000000000
        assert p.url != ""


# def test_walk_subreddit():
#     # url = "https://old.reddit.com/r/China_irl/"
#     # url = "https://old.reddit.com/r/CombatFootage/"
#     url = "https://old.reddit.com/r/zenfone6/"
#     walk_subreddit(url, print)
