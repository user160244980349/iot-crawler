from config import paths
from config import sanitizer_settings
from crawler.link_matcher import LinkMatcher
from crawler.modules.converter import Converter
from crawler.modules.downloader import Downloader
from crawler.modules.efficiency import Efficiency
from crawler.modules.pack import Pack
from crawler.modules.policies import Policies
from crawler.modules.sanitizer import Sanitization
from crawler.modules.urls import Urls
from crawler.modules.websites import Websites
from crawler.link_matcher import LinkMatcher


# Modules for IoT mining
modules = [

    Urls(),

    Websites(
        paths.json.products,
        paths.json.websites,
    ),

    Policies(
        paths.json.websites,
        paths.json.policies,
        LinkMatcher((r"privacy(policy)?",)),
    ),

    Downloader(
        paths.json.policies,
        paths.explicit,
        paths.json.downloaded,
        paths.dir.original,
    ),

    Sanitization(
        paths.json.downloaded,
        paths.json.sanitized,
        paths.dir.processed,
        sanitizer_settings=sanitizer_settings
    ),

    Converter(
        paths.json.sanitized,
        paths.json.plain,
        paths.dir.plain
    ),

    Efficiency(
        paths.json.plain,
        paths.metrics
    ),

    Pack(paths.resources, paths.deploy, paths.json.downloaded,
         paths.json.sanitized, paths.json.plain, paths.archive)

]
