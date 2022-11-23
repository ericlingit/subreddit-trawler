from dataclasses import dataclass
from typing import List, Optional
from urllib import parse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from subreddit import PostLink, PostType, headers


@dataclass
class Video:
    # Video and audio track are stored separately.
    video: str
    audio: str


@dataclass
class Content:
    comment: List[str]
    image: List[str]  # List of image URLs.
    video: Optional[Video]


def parse_post_content(soup: BeautifulSoup, metadata: PostLink) -> None:
    # Title.
    maybe_title: List[Tag] = soup.select("p.title a.title")
    assert len(maybe_title) == 1
    title = maybe_title.pop()
    print(title.text.strip())  # Title text could be blank.

    # Flare, if any.
    maybe_flare: List[Tag] = soup.select("p.title span.linkflairlabel")
    flare = maybe_flare[0].text.strip() if len(maybe_flare) > 0 else "(no flare)"
    print(flare)

    # # Comments, including opening poster's comment (reply structure not preserved).
    # comments = soup.select("div.entry div.usertext-body div.md p")
    # print(len(comments))
    # for p in comments:
    #     print(p.text)

    # OP image (get link from PostLink object)
    if metadata.type is PostType.Image:
        print(f"found image: {metadata.url}")

    # OP video (get link from PostLink object)
    if metadata.type is PostType.Video:
        metadata.url
        # Transform from "https://v.redd.it/abc123xyz"
        # to "https://v.redd.it/4huchegx4x0a1/DASH_720.mp4"
        # and "https://v.redd.it/4huchegx4x0a1/DASH_audio.mp4"
        print("found video")
        print(f"{metadata.url}/DASH_720.mp4")
        print(f"{metadata.url}/DASH_audio.mp4")

    # Gallery.
    if metadata.type is PostType.Gallery:
        gallery_img = soup.select(
            "div.media-gallery div.gallery-tiles div div.gallery-tile-content img.preview"
        )
        print(f"found gallery with {len(gallery_img)} pics")
        for img in gallery_img:
            src = img.get("src", "")
            # Transform src URL
            # from "https://preview.redd.it/abcxyz123.jpg?width=108&crop=smart&auto=webp&s=xxxxxxxxxxxxxxxxxxxxxxxxxx"
            # to   "https://i.redd.it/abcxyz123.jpg"
            d = parse.urlparse(src)

            print(
                parse.urlunparse(
                    (
                        d[0],  # scheme="https"
                        "i.redd.it",  # netloc="i.redd.it"
                        d[2],  # path="abcxyz123.jpg"
                        "",  # params=""
                        "",  # query=""
                        "",  # fragment=""
                    )
                )
            )


if __name__ == "__main__":
    import pickle

    sample_text = PostLink(
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
    sample_link = PostLink(
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
    sample_img = PostLink(
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
    sample_gallery = PostLink(
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
    sample_vid = PostLink(
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

    # # Visit post
    # resp = requests.get(sample_gallery.permalink, headers=headers)
    # with open("post_gallery.pickle", "wb") as fh:
    #     pickle.dump(resp, fh)

    # Load Page snapshot.
    with open("post_gallery.pickle", "rb") as fh:
        resp: Response = pickle.load(fh)

    soup = BeautifulSoup(resp.content, "lxml")
    parse_post_content(soup, sample_img)
