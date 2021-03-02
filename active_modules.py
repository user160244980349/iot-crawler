from crawler.modules.converter import Converter
from crawler.modules.efficiency import Efficiency
from crawler.modules.sanitizer import Sanitization

modules = [

    # Products(),
    # Websites(),
    # Policies(),
    # Downloader(),
    Sanitization(),
    Converter(),
    Efficiency(),

]
