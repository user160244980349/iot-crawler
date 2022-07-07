from crawler.modules.converter import Converter
from crawler.modules.efficiency import Efficiency
from crawler.modules.fix_abs_paths import FixAbsPaths
from crawler.modules.pack import Pack
from crawler.modules.sanitizer import Sanitization
from crawler.modules.downloader import Downloader

modules = [

    # Products(),
    # Websites(),
    # Policies(),
    # Downloader(),
    # Sanitization(),
    # Converter(),
    # Efficiency(),
    FixAbsPaths(),
    Pack(),

]
