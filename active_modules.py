from crawler.modules.converter import Converter
from crawler.modules.downloader import Downloader
from crawler.modules.efficiency import Efficiency
from crawler.modules.policies import Policies
from crawler.modules.products import Products
from crawler.modules.sanitizer import Sanitization
from crawler.modules.websites import Websites

modules = [

    # Products(),
    # Websites(),
    # Policies(),
    # Downloader(),
    Sanitization(),
    Converter(),
    Efficiency(),

]
