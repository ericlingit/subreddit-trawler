from dataclasses import dataclass
from typing import List, Optional
from urllib import parse

from bs4 import BeautifulSoup
from bs4.element import Tag

from subreddit_trawler.walker import PostMetadata, PostType


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

    Only comments on the first page are scraped. Deep threads aren't followed.
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
