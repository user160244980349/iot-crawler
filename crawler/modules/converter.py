import json
import os
import re
from multiprocessing import Pool
from bs4 import BeautifulSoup, Tag, NavigableString

from crawler.modules.module import Module
from crawler.modules.sanitizer import Sanitization


class Converter(Module):
    local_subs = [
        (r"[^ёа-яa-z0-9,.:;\\/\-\n\s\(\)\{\}*?!\[\]]", ""),
        (r"\n+", ""),
        (r"\s+", " "),
        (r"^[\n ]+", ""),
    ]

    global_subs = [
        (r"[\w\-]+@[a-z]+\.[a-z]{2,}/?", "{removed e-mail}"),
        (r"(https?://)?(www\.)?(([\w\-]+\.)+[a-z]{2,})(/[\w\-]+)*/?",
         "{removed hyperref}"),

        (r"^\s{4}", ""),

        (r" ([.,:;!?\)\}\]])", "\g<1>"),
        (r"([.,:;!?\)\}\]])(\w+)", "\g<1> \g<2>"),
        (r"(\w|[\}\]\)])\n", "\g<1>.\n"),
        (r"([\[\(\{]) ", "\g<1>"),
        (r"([\}\]\)])([\{\[\(])", "\g<1> \g<2>"),

        (r"</?.*/?>", ""),

        (r"\n{4,}", "\n\n\n")
    ]

    global_regexps = [(re.compile(s[0], flags=re.MULTILINE | re.IGNORECASE),
                       s[1]) for s in global_subs]
    local_regexps = [(re.compile(s[0], flags=re.MULTILINE | re.IGNORECASE),
                      s[1]) for s in local_subs]
    empty_tag = re.compile(r"^[ \n]*$")

    def __init__(self, sanitized_json, plain_json, plain_dir, threshold=2000):
        super(Converter, self).__init__()
        self.sanitized_json = sanitized_json
        self.plain_json = plain_json
        self.plain_dir = plain_dir
        self.threshold = threshold

    def bootstrap(self):
        with open(os.path.relpath(self.sanitized_json), "r") as f:
            self.records = json.load(f)

    def run(self, p: Pool = None):
        self.logger.info("Converting to plain text")

        jobs = filter(None, set([r["processed_policy"] for r in self.records]))
        plain = p.map(self.plain_webpage, jobs)

        for item in self.records:
            for policy, plain_policy in plain:
                if policy == item["processed_policy"]:
                    item["plain_policy"] = plain_policy

    def finish(self):
        with open(os.path.relpath(self.plain_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def plain_webpage(self, item):
        with open(os.path.relpath(item), "r", encoding="utf-8") as f:
            text = f.read()

        soup = BeautifulSoup(text, "lxml")
        self.walk(soup, preprocess=(self.replace_a,))
        self.walk(soup, preprocess=(self.mark_li,))
        self.walk(soup, preprocess=(self.unwrap_accents,))
        self.walk(soup, postprocess=(self.wrap_raw_text,))
        self.walk(soup, preprocess=(self.clear_paragraphs,))
        self.walk(soup, postprocess=(self.unwrap_nested,))
        self.walk(soup, preprocess=(self.remove_empty,))
        text = Sanitization.prettify(soup, indent_width=0)

        for r in self.global_regexps:
            text = r[0].sub(r[1], text)

        policy = os.path.join(os.path.relpath(self.plain_dir),
                              f"{os.path.basename(item)}.txt")
        if len(text) < self.threshold:
            return item, None
        with open(policy, "w", encoding="utf-8") as f:
            f.write(text)
        return item, policy

    @classmethod
    def walk(cls, element, preprocess=(), postprocess=(),
             ignore=("html", "head", "meta", "title")):
        if element.name not in ignore:
            for p in preprocess:
                p(element)
        if not isinstance(element, NavigableString):
            for child in element.children:
                cls.walk(child, preprocess=preprocess,
                         postprocess=postprocess, ignore=ignore)
        if element.name not in ignore:
            for p in postprocess:
                p(element)

    @classmethod
    def unwrap_accents(cls, element):
        if element.name == "strong" \
                or element.name == "em":
            element.replaceWith(NavigableString(element.text.upper()))
            return

    @classmethod
    def unwrap_nested(cls, element):
        if isinstance(element, NavigableString):
            return
        for cn in element.children:
            if isinstance(cn, NavigableString):
                continue
            if all([isinstance(c, Tag) for c in cn]):
                cn.unwrap()

    @classmethod
    def wrap_raw_text(cls, element):
        if isinstance(element, NavigableString):
            return

        groups = []
        group = []

        for c in element.children:
            if isinstance(c, NavigableString):
                group.append(c)
            if isinstance(c, Tag):
                groups.append(group)
                group = []

        if len(group) > 0:
            groups.append(group)

        for g in groups:
            if len(g) == 0:
                continue
            par = Tag(name="p")
            g[0].wrap(par)
            for i in range(1, len(g)):
                par.append(g[i])

    @classmethod
    def remove_empty(cls, element):
        if isinstance(element, NavigableString):
            return
        if element.name == "br" or cls.empty_tag.match(element.text):
            element.extract()

    @classmethod
    def replace_a(cls, element):
        if isinstance(element, NavigableString):
            return
        if element.name == "a":
            label = "{removed href}"
            element.replaceWith(NavigableString(f"{label} {element.text}"))

    @classmethod
    def clear_paragraphs(cls, element):
        if isinstance(element, NavigableString):
            return
        if all([isinstance(c, NavigableString) for c in element.children]):
            text = element.text
            for r in cls.local_regexps:
                text = r[0].sub(r[1], text)
            e = Tag(name=element.name)
            e.append(NavigableString(text))
            element.replaceWith(e)

    @classmethod
    def mark_li(cls, element):
        if isinstance(element, NavigableString):
            return
        if element.name == "li":
            element.insert(0, NavigableString("{list item}"))
        if element.name == "ol":
            element.insert(0, NavigableString("{bullet list}"))
        if element.name == "ul":
            element.insert(0, NavigableString("{number list}"))
