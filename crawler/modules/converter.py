import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup, Tag, NavigableString

import config
from crawler.modules.module import Module
from crawler.modules.sanitizer import Sanitization


class Converter(Module):
    local_subs = [
        (r"\n+", " "),
        (r"\s+", " "),
    ]

    global_subs = [
        (r"[\w\d_\-]+@\w+\.\w+", "e-mail"),
        (r"(www\.)?[\w\d_\-]+\.\w+", "website"),

        (r"^\s{4}", ""),  # indentation

        (r" ([.,:;!?])", "\g<1>"),  # split punctuation
        (r"([.,:;!?])(\w+)", "\g<1> \g<2>"),  # split punctuation
        (r"(\w+)\n", "\g<1>.\n"),  # split punctuation

        (r"\n", "\n\n\n"),  # spacing

        (r"<ul>", ""),  # ol_tags
        (r"<ol>", ""),  # ol_tags
        (r"<li>", "***"),  # li_tags

        (r"<\w+/?>", ""),  # open_tags
        (r"</\w+/?>", "\n\n\n"),  # close_tags
        (r"^\s+$", "\n\n\n"),  # too_many_nl
        (r"\n{4,}", "\n\n\n"),  # too_many_nl

        (r"[^A-Za-z0-9,.:;\\/\-\n\s(){}*?!]", ""),  # special characters
    ]

    global_regexps = [(re.compile(s[0], flags=re.MULTILINE), s[1]) for s in global_subs]
    local_regexps = [(re.compile(s[0], flags=re.MULTILINE), s[1]) for s in local_subs]

    def __init__(self):
        super(Converter, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def bootstrap(self):
        with open(os.path.abspath(config.sanitized_json), "r") as f:
            self.records = json.load(f)

    def run(self, p: Pool = None):
        self.logger.info("Converting to plain text")

        if p is None:
            plain = [self.plain_webpage(i) for i in set([r["processed_policy"] for r in self.records])]
        else:
            plain = p.map(self.plain_webpage, set(r["processed_policy"] for r in self.records))

        for item in self.records:
            for policy, plain_policy in plain:
                if policy == item["processed_policy"]:
                    item["plain_policy"] = plain_policy

    def finish(self):
        with open(os.path.abspath(config.plain_json), "w") as f:
            json.dump(self.records, f, indent=2)

    @classmethod
    def plain_webpage(cls, item):

        if item is None:
            return item, None

        with open(os.path.abspath(item), "r", encoding="utf-8") as f:
            text = f.read()

        soup = BeautifulSoup(text, "lxml")

        cls.wrap_rawtext(soup)
        cls.unwrap_some(soup)
        cls.trim_spaces(soup)

        text = Sanitization.prettify(soup)

        for r in cls.global_regexps:
            text = r[0].sub(r[1], text)

        policy = os.path.join(os.path.abspath(config.plain_policies), f"{os.path.basename(item)}.txt")
        with open(policy, "w", encoding="utf-8") as f:
            f.write(text)

        return item, policy

    @classmethod
    def unwrap_some(cls, element):

        if element.name == "strong" \
                or element.name == "em" \
                or element.name == "h1" \
                or element.name == "h2" \
                or element.name == "h3":
            element.replaceWith(NavigableString(element.text.upper()))

        for child in element.findAll(recursive=False):
            cls.unwrap_some(child)

    @classmethod
    def wrap_rawtext(cls, element):

        if len(element.contents) > 1 and \
                all([isinstance(c, NavigableString)
                     or c.name == "br" for c in element.contents]):
            for c in element.contents:
                e = Tag(name="p")
                c.wrap(e)

            element.unwrap()
            return

        for child in element.findAll(recursive=False):
            cls.wrap_rawtext(child)

    @classmethod
    def trim_spaces(cls, element):

        children = element.findAll(recursive=False)

        if (element.name == "p"
            or element.name == "li") \
                and len(children) == 0:

            e = Tag(name=element.name)

            text = element.text
            for r in cls.local_regexps:
                text = r[0].sub(r[1], text)

            e.insert(0, NavigableString(text))
            element.replaceWith(e)

        for child in children:
            cls.trim_spaces(child)

    @classmethod
    def fill_lists(cls, element):

        if len(element.contents) > 1 and \
                all([isinstance(c, NavigableString)
                     or c.name == "br" for c in element.contents]):
            for c in element.contents:
                e = Tag(name="p")
                c.wrap(e)

            element.unwrap()
            return

        for child in element.findAll(recursive=False):
            cls.fill_lists(child)
