# Subreddit trawler

Scrape sub reddit posts using the old url `https://old.reddit.com`.

https://old.reddit.com/r/Chinatown_irl/

https://old.reddit.com/r/China_irl/



- scrape sub reddit
    - visit each post link
        - skip announcement
            - if the url contains `predictions?tournament`, always skip this link. no old version is available.
                - eg: `https://www.reddit.com/r/wallstreetbets/predictions?tournament=tnmt-0b14066a-ad68-4351-8261-d1c0740c44d2`
        - scrape comments
            - submit text
            - submit image
            - submit video
            - nsfw/spoiler

- find next button
    - extract link
    - go to link
    - repeat above

Examples for various post types:
- [Text post](https://old.reddit.com/r/China_irl/comments/z0oio5)
- [Image post](https://old.reddit.com/r/China_irl/comments/z0ojwn)
- [Video post](https://old.reddit.com/r/China_irl/comments/yzv625)
- [Gallery](https://old.reddit.com/r/China_irl/comments/z0728o)
- [NSFW text (Whats the most NSFW experience you witnessed right in front of your eyes?)](https://old.reddit.com/r/AskReddit/comments/z0uq39)
- [NSFW image (Grown man ass-kissing)](https://www.reddit.com/r/cringepics/comments/z0xhwy)
- [NSFW video (Ukrainian drone flies right into the Russian trench)](https://old.reddit.com/r/CombatFootage/comments/z1391l)

## Notes

Sample video PostLink:

```json
{
    "id": "z09a7r",
    "author": "Dry_Illustrator5642",
    "timestamp": 1668963979000,
    "url": "https://v.redd.it/4huchegx4x0a1",
    "permalink": "https://old.reddit.com/r/China_irl/comments/z09a7r/翼刀性感电臀舞/",
    "domain": "v.redd.it",
    "comments_count": 1,
    "score": 0,
    "nsfw": false,
    "spoiler": false,
    "type": "video"
}
```

Actual downloadable video addr: `https://v.redd.it/4huchegx4x0a1/DASH_720.mp4`
Audio addr: `https://v.redd.it/4huchegx4x0a1/DASH_audio.mp4`


Sample image PostLink:

```json
{
    "id": "wv4ydl",
    "author": "darkyknight01",
    "timestamp": 1661201834000,
    "url": "https://i.redd.it/6b66lj3fwbj91.jpg",
    "permalink": "https://old.reddit.com/r/zenfone6/comments/wv4ydl/in_delhi_i_need_info_for_that_how_should_i/",
    "domain": "i.redd.it",
    "comments_count": 1,
    "score": 1,
    "nsfw": false,
    "spoiler": false,
    "type": "image"
}
```

Sample text PostLink:

```json
{
    "id": "xg61f6",
    "author": "silver2006",
    "timestamp": 1663370013000,
    "url": "/r/zenfone6/comments/xg61f6/need_help_unlocking_the_bootloader/",
    "permalink": "https://old.reddit.com/r/zenfone6/comments/xg61f6/need_help_unlocking_the_bootloader/",
    "domain": "self.zenfone6",
    "comments_count": 4,
    "score": 1,
    "nsfw": false,
    "spoiler": false,
    "type": "text"
}
```

Sample link PostLink:

```json
{
    "id": "z2bhbm",
    "author": "Counterhaters",
    "timestamp": 1669166866000,
    "url": "https://www.zaobao.com.sg/realtime/china/story20221122-1335992",
    "permalink": "https://old.reddit.com/r/China_irl/comments/z2bhbm/消息中国拟对蚂蚁处以逾10亿美元罚款/",
    "domain": "zaobao.com.sg",
    "comments_count": 1,
    "score": 4,
    "nsfw": false,
    "spoiler": false,
    "type": "link"
}
```

Gallery element:

```html
<div class="media-gallery">
    <div class="gallery-tiles">
        <div class="gallery-tile gallery-navigation">
            <div class="media-preview-content gallery-tile-content">
                <img class="preview", src="...", width=..., height=...>
            </div>
        </div>
    </div>
</div>
```

The "next" button element:

```html
<span class="next-button">
    <a href="https://old.reddit.com/r/Music/?count=25&after=t3_z1lqur" rel="nofollow next">next ›</a>
</span>
```

The element that lists all posts:

```html
<div id="siteTable" class="sitetable linklisting">
```

![screenshot of element that has all the links](Screenshot-link-list.png)

When you forget to change user-agent:

```html
<!doctype html>
<html>

<head>
    <title>Too Many Requests</title>
</head>

<body>
    <h1>whoa there, pardner!</h1>
    <p>we're sorry, but you appear to be a bot and we've seen too many requests from you lately. we enforce a hard
        speed limit on requests that appear to comefrom bots to prevent abuse.</p>
    <p>if you are not a bot but are spoofing one via your browser's user agentstring: please change your user agent
        string to avoid seeing this messageagain.</p>
    <p>please wait 1 second(s) and try again.</p>
    <p>as a reminder to developers, we recommend that clients make no more than <a
            href="http://github.com/reddit/reddit/wiki/API">one request every two seconds</a> to avoid seeing this
        message.</p>
</body>

</html>
```