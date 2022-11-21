# Subreddit scraper

Scrape sub reddit posts using the old url `https://old.reddit.com`.

https://old.reddit.com/r/Chinatown_irl/

https://old.reddit.com/r/China_irl/



- scrape sub reddit
    - visit each post link
        - skip announcement
            - if the url contains `predictions?tournament`, always skip this link. no old version is available.
                - eg: `https://www.reddit.com/r/China_irl/predictions/?tournament=tnmt-9458496b-ea9f-49d8-90f4-ddbad8772459`
        - scrape comments
            - submit text
            - submit image
            - submit video
            - nsfw

- find next button
    - extract link
    - go to link
    - repeat above


## notes

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
    <p>we\'re sorry, but you appear to be a bot and we\'ve seen too many requestsfrom you lately. we enforce a hard
        speed limit on requests that appear to comefrom bots to prevent abuse.</p>
    <p>if you are not a bot but are spoofing one via your browser\'s user agentstring: please change your user agent
        string to avoid seeing this messageagain.</p>
    <p>please wait 1 second(s) and try again.</p>
    <p>as a reminder to developers, we recommend that clients make no more than <a
            href="http://github.com/reddit/reddit/wiki/API">one request every two seconds</a> to avoid seeing this
        message.</p>
</body>

</html>
```