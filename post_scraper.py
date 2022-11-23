from dataclasses import dataclass
from typing import List, Optional
from urllib import parse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from subreddit import PostMetadata, PostType, headers


@dataclass
class Video:
    # Video and audio track are stored separately.
    video_track: str
    audio_track: str


@dataclass
class Content:
    title: str
    flare: str
    # `comment` has OP's comment and all replies. Reply structure and commentor
    # metadata are not preserved. Each <p> tag text is a str item in this list.
    comments: List[str]
    images: List[str]  # List of image URLs.
    video: Optional[Video]


def parse_post_content(raw_response: bytes, metadata: PostMetadata) -> Content:
    """Parse the raw response of a subreddit post. `raw_response` should be the
    response data (e.g., the `request.Response.content` attribute) of a GET
    request to a URL like this:

    https://old.reddit.com/r/Subreddit_name/comments/abcxyz/op_title/
    """
    soup = BeautifulSoup(raw_response, "lxml")

    # Title.
    title: str = ""
    maybe_title: List[Tag] = soup.select("p.title a.title")
    if len(maybe_title) == 1:
        title_tag = maybe_title.pop()
        title = title_tag.text.strip()  # Title text could be blank.

    # Flare, if any.
    flare: str = ""
    maybe_flare: List[Tag] = soup.select("p.title span.linkflairlabel")
    if len(maybe_flare) == 1:
        flare_tag = maybe_flare.pop()
        flare = flare_tag.text.strip()

    # Comments, including OP's comment (reply structure not preserved).
    maybe_comments = soup.select("div.entry div.usertext-body div.md p")
    comments: List[str] = [
        p_tag.text.strip()
        for p_tag in maybe_comments
        if p_tag.text.strip() != "[removed]"
    ]

    # OP video.
    video: Optional[Video] = None
    if metadata.type is PostType.Video:
        # Transform from "https://v.redd.it/abc123xyz"
        # to  "https://v.redd.it/4huchegx4x0a1/DASH_720.mp4"
        # and "https://v.redd.it/4huchegx4x0a1/DASH_audio.mp4"
        video = Video(
            video_track=f"{metadata.url}/DASH_720.mp4",
            audio_track=f"{metadata.url}/DASH_audio.mp4",
        )

    # OP image.
    images: List[str] = []
    if metadata.type is PostType.Image:
        images.append(metadata.url)
    # Gallery.
    if metadata.type is PostType.Gallery:
        gallery_img = soup.select(
            "div.media-gallery div.gallery-tiles div div.gallery-tile-content img.preview"
        )
        for img in gallery_img:
            src: str = img.get("src", "")
            # Transform src URL
            # from "https://preview.redd.it/abcxyz123.jpg?width=108&crop=smart&auto=webp&s=xxxxxxxxxxxxxxxxxxxxxxxxxx"
            # to   "https://i.redd.it/abcxyz123.jpg"
            scheme, _, path, _, _, _ = parse.urlparse(src)
            img_url: str = parse.urlunparse(
                (
                    scheme,
                    "i.redd.it",  # netloc
                    path,
                    "",  # params
                    "",  # query
                    "",  # fragment
                )
            )
            images.append(img_url)

    return Content(
        title=title,
        flare=flare,
        comments=comments,
        images=images,
        video=video,
    )


if __name__ == "__main__":
    import pickle

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

    # # Visit post
    # resp = requests.get(sample_video.permalink, headers=headers)
    # with open("post_video.pickle", "wb") as fh:
    #     pickle.dump(resp, fh)

    # Load page snapshot.
    with open("post_video.pickle", "rb") as fh:
        resp: Response = pickle.load(fh)

    c = parse_post_content(resp.content, sample_video)
    print(c)
