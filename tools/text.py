import re
from difflib import SequenceMatcher
from re import sub, match

from tools.exceptions import UrlNotFound


def similarity(content, url):
    return SequenceMatcher(None, content, url).ratio()


def parse_proxy(proxy: str):
    p = re.match("^(.*):(.*)$", proxy)
    return p.group(1), int(p.group(2))


def url_to_name(url: str):
    name = match(r"^https?://(.*[^/])(/|$)", url)
    if not name:
        raise UrlNotFound(url)
    name = sub(r"[&/?=+\\]", "-", name.group(1))
    return f"{name}.html"
