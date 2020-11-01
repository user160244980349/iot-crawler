import re

from crawler.downloader.exceptions import UrlNotFound


def url_to_name(url):

    name = re.match(r"^https?://(.*[^/])(/|$)", url)

    if not name:
        raise UrlNotFound(url)

    name = name.group(1)

    name = re.sub(r"[/\\]", "-", name)

    return f"{name}.html"
