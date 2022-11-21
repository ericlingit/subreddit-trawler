import pickle
from typing import List

import requests
from requests import Response
from bs4 import BeautifulSoup
from bs4.element import Tag


# Video post
# https://old.reddit.com/r/China_irl/comments/yzv625/%E5%B0%8F%E7%86%8A%E7%8C%AB%E5%90%83%E8%91%A1%E8%90%84%E4%B8%8D%E5%90%90%E8%91%A1%E8%90%84%E7%9A%AE/

# Image post
# https://old.reddit.com/r/China_irl/comments/z0ojwn/%E5%A4%A9%E6%9C%9D%E7%AC%91%E8%AF%9D48%E8%BE%B1%E5%8D%8E%E7%BD%AA%E5%90%8D%E5%A4%B1%E8%B4%A5%E7%9C%8B%E4%BA%86%E4%BB%A5%E5%90%8E%E5%93%AD%E7%AC%91%E4%B8%8D%E5%BE%97%E7%94%B7%E9%BB%98%E5%A5%B3%E6%B3%AA/

# Text post
# https://old.reddit.com/r/China_irl/comments/z0oio5/%E8%B6%8A%E5%8D%97%E6%95%B0%E5%AD%97%E5%A8%81%E6%9D%83%E4%B8%BB%E4%B9%89%E7%9A%84%E6%82%84%E7%84%B6%E6%BC%94%E5%8F%98/


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
url = "https://old.reddit.com/r/China_irl/"

# Rate-limit: no more than 3 requests per second.

# # Capture subreddit snapshot.
# resp = requests.get(url, headers=headers)
# with open("subreddit_china_irl.pickle", "wb") as fh:
#     pickle.dump(resp, fh)

# Load subreddit snapshot.
with open("subreddit_china_irl.pickle", "rb") as fh:
    resp: Response = pickle.load(fh)

soup = BeautifulSoup(resp.content, "lxml")
# print(soup.text)
listing: List[Tag] = soup.find_all(class_="linklisting")
assert (
    len(listing) == 1
), "not found: <div id='siteTable' class='sitetable linklisting'>"
