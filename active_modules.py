import config
from crawler.modules.converter import Converter
from crawler.modules.efficiency import Efficiency
from crawler.modules.fix_abs_paths import FixAbsPaths
from crawler.modules.pack import Pack
from crawler.modules.policies import Policies
from crawler.modules.urls import Urls
from crawler.modules.sanitizer import Sanitization
from crawler.modules.downloader import Downloader

modules = [

    # Urls(),

    # Websites(),

    # Policies(
    #     (r"политика конфиденциальности",
    #      r"пользовательское соглашение",
    #      r"политика безопасности"),
    #     wj=config.mrt_websites,
    #     pj=config.mrt_policies
    # ),

    # Downloader(
    #     pj=config.mrt_policies,
    #     ej=config.mrt_explicit,
    #     dj=config.mrt_downloaded,
    #     op=config.mrt_original_policies
    # ),

    # Sanitization(
    #      dj=config.mrt_downloaded,
    #      sj=config.mrt_sanitized,
    #      pp=config.mrt_processed_policies,
    #      sc=config.sanitizer_settings
    # ),

    Converter(
         sj=config.mrt_sanitized,
         pj=config.mrt_plain,
         pl=config.mrt_plain_policies
    ),

    # Efficiency(
    #      pj=config.mrt_plain,
    #      mj=config.mrt_metrics
    # ),

    # FixAbsPaths(),

    # Pack(),

]
