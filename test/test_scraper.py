import pickle

from requests import Response

from subreddit_trawler.scraper import parse_post_content, PostMetadata, PostType


def test_parse_post_content():
    sample_text = PostMetadata(
        id="z0oio5",
        author="Proper_Bodybuilder_2",
        timestamp=1669002333000,
        url="/r/China_irl/comments/z0oio5/越南数字威权主义的悄然演变/",
        permalink="https://old.reddit.com/r/China_irl/comments/z0oio5/越南数字威权主义的悄然演变/",
        domain="self.China_irl",
        comments_count=40,
        score=35,
        nsfw=False,
        spoiler=False,
        type=PostType.Text,
    )
    sample_link = PostMetadata(
        id="z2bhbm",
        author="Counterhaters",
        timestamp=1669166866000,
        url="https://www.zaobao.com.sg/realtime/china/story20221122-1335992",
        permalink="https://old.reddit.com/r/China_irl/comments/z2bhbm/消息中国拟对蚂蚁处以逾10亿美元罚款/",
        domain="zaobao.com.sg",
        comments_count=1,
        score=4,
        nsfw=False,
        spoiler=False,
        type=PostType.Link,
    )
    sample_image = PostMetadata(
        id="z0ojwn",
        author="Different_Ad6979",
        timestamp=1669002431000,
        url="https://i.redd.it/yipqe5ix581a1.jpg",
        permalink="https://old.reddit.com/r/China_irl/comments/z0ojwn/天朝笑话48辱华罪名失败看了以后哭笑不得男默女泪/",
        domain="i.redd.it",
        comments_count=87,
        score=455,
        nsfw=False,
        spoiler=False,
        type=PostType.Image,
    )
    sample_gallery = PostMetadata(
        id="z0728o",
        author="Different_Ad6979",
        timestamp=1668958500000,
        url="https://www.reddit.com/gallery/z0728o",
        permalink="https://old.reddit.com/r/China_irl/comments/z0728o/苏联德国二战前海报对比/",
        domain="old.reddit.com",
        comments_count=17,
        score=27,
        nsfw=False,
        spoiler=False,
        type=PostType.Gallery,
    )
    sample_video = PostMetadata(
        id="z09a7r",
        author="Dry_Illustrator5642",
        timestamp=1668963979000,
        url="https://v.redd.it/4huchegx4x0a1",
        permalink="https://old.reddit.com/r/China_irl/comments/z09a7r/翼刀性感电臀舞/",
        domain="v.redd.it",
        comments_count=1,
        score=0,
        nsfw=False,
        spoiler=False,
        type=PostType.Video,
    )

    # Visit post
    # import requests
    # from subreddit import headers
    # resp = requests.get(sample_text.permalink, headers=headers)
    # with open("post_text.pickle", "wb") as fh:
    #     pickle.dump(resp, fh)

    # Load page snapshot.
    with open("test/post_text.pickle", "rb") as fh:
        resp: Response = pickle.load(fh)

    c = parse_post_content(resp.content, sample_text)
    assert c.title == "越南数字威权主义的悄然演变"
    assert len(c.comments) == 71
    assert c.flare == "政治经济"
    assert c.images == []
    assert c.video is None
