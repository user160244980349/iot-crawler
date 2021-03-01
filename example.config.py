import logging
import os

from html_sanitizer.sanitizer import \
    sanitize_href, anchor_id_to_name, \
    target_blank_noopener, tag_replacer, \
    italic_span_to_em, bold_span_to_strong

# Paths to resources
resources_abs = os.path.abspath("./resources")
products_json = f"{resources_abs}/json/products.json"
websites_json = f"{resources_abs}/json/websites.json"
policies_json = f"{resources_abs}/json/policies.json"
downloaded_json = f"{resources_abs}/json/downloaded.json"
sanitized_json = f"{resources_abs}/json/sanitized.json"
plain_json = f"{resources_abs}/json/plain.json"
explicit_json = f"{resources_abs}/explicit.json"
metrics_json = f"{resources_abs}/metrics.json"

original_policies = f"{resources_abs}/original_policies"
processed_policies = f"{resources_abs}/processed_policies"
plain_policies = f"{resources_abs}/plain_policies"

# Subprocesses count, 0 for all available
sub_proc_count = 1

max_timeout_attempts = 3
max_error_attempts = 3
max_captcha_attempts = 3

# Webdriver settings
webdriver_settings = {
    "profile_path": "C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/pkvhrtp3.default-release",
    "log_path": f"{resources_abs}/.geckodriver.log",
    "dotfile": f"{resources_abs}/.driver",
    "log_level": logging.INFO,
    "no_cache": False,
    "headless": True,
    "use_proxy": False,
    "user_agents": [
        "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; InfoPath.1; HbTools 4.8.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7pre) Gecko/20070901 BonEcho/2.0.0.7pre",
        "Mozilla/5.0 (X11; U; OpenBSD ppc; en-US; rv:1.8.1.9) Gecko/20070223 BonEcho/2.0.0.9",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1a2) Gecko/20060512 BonEcho/2.0a2",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.9) Gecko/20071103 BonEcho/2.0.0.9",
    ],
    "proxies": [
        "37.135.121.10:80",
        "104.248.90.212:80",
        "50.206.25.111:80",
        "139.162.78.109:3128",
    ]
}

# Html-sanitizer settings
sanitizer_settings = {
    "tags": {
        "h1", "h2", "h3", "strong", "em",
        "p", "ul", "ol", "li", "br"
    },
    "attributes": {},
    "empty": {"br"},
    "separate": {"p", "li"},
    "whitespace": {"br"},
    "keep_typographic_whitespace": False,
    "add_nofollow": False,
    "autolink": False,
    "sanitize_href": sanitize_href,
    "element_preprocessors": [
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer("b", "strong"),
        tag_replacer("i", "em"),
        target_blank_noopener,
        anchor_id_to_name,
    ],
    "element_postprocessors": [],
}
