import json
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Callable, List

import requests
from requests import Response
from bs4 import BeautifulSoup
from bs4.element import Tag


headers = {
    "Host": "old.reddit.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "loid=0000000000ug9l2gua.2.1669015062000.Z0FBQUFBQmpleVlXYWZnZWV0dG43WFNWcmlTajZmSW1rejBzYjRfdWxKYW9LanR4VjhsN0FCT01Va0hjUlREaHNFdks0U3lmeWVCUVZxTFhaeDA5TS1aeVFwQVdtYjNIY0dsTDBCNnBrYWlINk9rWngwNkRVN0QzS3ZxY1JhWnRJalNJb1NSWXNfbzU; session_tracker=eraklefoladlmqleea.0.1669016031895.Z0FBQUFBQmpleW5ncmtHdnFfcS1DNTAxZWtzNjVVS0FmUjRuVm5XWEZvejkzOWQtR0NmRzZuQTNLVUZraFROMkJGZHVrTEVuSmw5VG1VYWdpTGNZMFZWYTRBajFPMXg0c05NWEd4R1owWUtYcUtlUndYb0s4YzBxZUpMOTRMNFpYTVdaNmo4V0VLc0Q; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjkxMDEzNDgsInN1YiI6Ii03eXl2WkhsemZnVEpVSEpxa25QcjZqU0pudVhnTGciLCJsb2dnZWRJbiI6ZmFsc2UsInNjb3BlcyI6WyIqIiwiZW1haWwiLCJwaWkiXX0.YsQtRvAAO4AJQ_Um3uLVoaWIYRWXWrwdhWnALvg6ORY; csv=2; edgebucket=GLgilbFKOiJTed5tob; USER=eyJwcmVmcyI6eyJnbG9iYWxUaGVtZSI6IlJFRERJVCIsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sIm5pZ2h0bW9kZSI6ZmFsc2UsInN1YnNjcmlwdGlvbnNQaW5uZWQiOmZhbHNlLCJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6MCwidG9wQ29udGVudFRpbWVzRGlzbWlzc2VkIjowfX0=; recent_srs=t5_x72uq%2Ct5_2qh2v%2C; pc=1w",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
}


class PostType(Enum):
    Text = "text"
    Link = "link"
    Video = "video"
    Image = "image"
    Gallery = "gallery"


@dataclass
class PostMetadata:
    id: str
    author: str
    timestamp: int
    url: str
    permalink: str
    domain: str
    comments_count: int
    score: int
    nsfw: bool
    spoiler: bool
    type: PostType

    def to_json_str(self) -> str:
        return json.dumps(
            asdict(self), ensure_ascii=False, indent=4, default=lambda x: x.value
        )

    def __str__(self) -> str:
        return self.to_json_str()


def collect_links(soup: BeautifulSoup) -> List[PostMetadata]:
    """Find and parse the BeautifulSoup object and return a list of PostLink objects."""
    listing: List[Tag] = soup.find_all(class_="linklisting")
    if len(listing) != 1:
        raise Exception("could not locate the div tag with linklisting class attribute")
    listing_div: Tag = listing.pop()
    all_posts: List[Tag] = listing_div.find_all(class_="link")
    if len(all_posts) < 1:
        raise Exception("found no posts")

    # Collect links to posts.
    posts: List[PostMetadata] = []
    for post in all_posts:
        # Skip ads or announcements.
        class_attr: List[str] = post.get_attribute_list("class")
        if "promoted" in class_attr or "stickied" in class_attr:
            continue

        post_id = post.get("id", "").replace("thing_t3_", "")

        # Identify post type by the data-domain attribute.
        # eg: "i.redd.it", "v.redd.it", "self.Music", "bloomberg.com", "youtube.com"
        data_domain = post.get("data-domain", "")
        if post.get("data-is-gallery", "false") == "true":
            post_type = PostType.Gallery
        elif data_domain.startswith("i.redd"):
            post_type = PostType.Image
        elif data_domain.startswith("v.redd"):
            post_type = PostType.Video
        elif data_domain.startswith("self."):
            post_type = PostType.Text
        else:
            post_type = PostType.Link

        p = PostMetadata(
            id=post_id,
            author=post.get("data-author", ""),
            timestamp=int(post.get("data-timestamp", -1)),  # eg: "1669002431000"
            url=post.get("data-url", ""),  # eg: "https://i.redd.it/gs54gv7cpf1a1.jpg"
            permalink=f"https://old.reddit.com{post.get('data-permalink', '')}",
            domain=data_domain,
            comments_count=int(post.get("data-comments-count", 0)),  # eg: "57"
            score=int(post.get("data-score", 0)),  # eg: "131"
            nsfw=True if post.get("data-nsfw", "") == "true" else False,  # eg: "false"
            spoiler=True if post.get("data-spoiler", "") == "true" else False,
            type=post_type,
        )
        posts.append(p)
    return posts


def walk_subreddit(
    url: str, processor: Callable[[PostMetadata], None], rate_limit: float = 3.0
) -> None:
    """Walk the subreddit at `url` until there are no more posts. Each post is
    passed to `processor` for processing. Advertisement and announcement posts
    are skipped.

    `rate_limit` specifies how long to sleep for after each request to Reddit.
    To be respectful, a default 3-second sleep time is applied before making the
    next request.
    """
    # Go to url.
    resp: Response = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    # Extract all links.
    posts = collect_links(soup)

    # Process each post with processor function.
    for post in posts:
        processor(post)
        time.sleep(rate_limit)

    # Find the "next" button and its URL.
    next = soup.select("span.next-button a")
    if len(next) != 1:
        print(f"reached end of subreddit: {url}")
        return
    next_url = next.pop().get("href", "")

    # Go to next page.
    time.sleep(rate_limit)
    walk_subreddit(next_url, processor)
