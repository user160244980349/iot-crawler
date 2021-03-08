import re
from difflib import SequenceMatcher

from tools.exceptions import UrlNotFound

reg1 = re.compile("^(.*):(.*)$")
reg2 = re.compile(r"^https?://(.*[^/])(/|$)")
reg3 = re.compile(r"[&/?=+\\]")


def similarity(content, url):
    return SequenceMatcher(None, content, url).ratio()


def parse_proxy(proxy: str):
    p = reg1.match(proxy)
    return p.group(1), int(p.group(2))


def url_to_name(url: str):
    name = reg2.match(url)
    if not name:
        raise UrlNotFound(url)
    name = reg3.sub("-", name.group(1))
    return f"{name}.html"
