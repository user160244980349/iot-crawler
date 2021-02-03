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

    name = name.group(1)

    name = sub(r"[&/?=+\\]", "-", name)

    return f"{name}.html"


def remove_quotes(text):
    return sub(r"[\'\"“]", " ", text)


def remove_br(text):
    return sub(r"<br>", "\n", text)


def remove_strong(text):
    return sub(r"<strong>", "", sub(r"</strong>", "\n", text))


def remove_ul(text):
    return sub(r"<ul>", "", sub(r"</ul>", "\n", text))


def remove_li(text):
    return sub(r"<li>", "", sub(r"</li>", "\n", text))


def remove_newlines(text):
    return sub(r"\n+\s*\n*", "\n", text)


def remove_spaces(text):
    return sub(r" {2,}", " ", text)


def remove_digits(text):
    return sub(r"\d+", "", text)


def remove_links(text):
    return sub(r" (.*/)+", "", text)


def remove_spec_chars(text):
    return sub(r"[_|@#$.,;:&`\"\'()]", " ", text)
