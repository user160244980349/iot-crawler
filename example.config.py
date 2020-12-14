#!/usr/bin/env python
from html_sanitizer.sanitizer import (
    target_blank_noopener, tag_replacer,
    italic_span_to_em, bold_span_to_strong,
    sanitize_href
)

# Paths to resources
resources = "D:/source/repos/privacy-ontolicy/resources"

# Paths to resources
original_policies = "D:/source/repos/privacy-ontolicy/resources/original_policies"

# Paths to resources
processed_policies = "D:/source/repos/privacy-ontolicy/resources/processed_policies"

# Path to database
database = "database.db"

# Settings for sanitizer
sanitizer_settings = {
    "tags": {
        "a", "h1", "h2", "h3", "strong", "em", "p", "ul", "ol",
        "li", "br", "sub", "sup", "hr",
    },
    "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
    "empty": {"hr", "a", "br"},
    "separate": {"a", "p", "li"},
    "whitespace": {"br"},
    "keep_typographic_whitespace": False,
    "add_nofollow": False,
    "autolink": False,
    "sanitize_href": sanitize_href,
    "element_preprocessors": [
        # convert span elements into em/strong if a matching style rule
        # has been found. strong has precedence, strong & em at the same
        # time is not supported
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer("b", "strong"),
        tag_replacer("i", "em"),
        tag_replacer("form", "p"),
        target_blank_noopener,
    ],
    "element_postprocessors": [],
    "is_mergeable": lambda e1, e2: True,
}

# Privacy policy urls
urls = [
    "https://policies.google.com/privacy",
    "https://august.com/pages/privacy-policy",
    "https://www.mi.com/global/about/privacy/",
]
