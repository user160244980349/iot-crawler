from crawler.plugins.amazon import Amazon
from crawler.plugins.walmart import Walmart

plugins = [

    # Walmart(["smart scales"], 1, cooldown=4., random_cooldown=10.)
    # Amazon(["smart scales"], 1, cooldown=2., random_cooldown=4.),

    Walmart([
        "smart scales",
        "smart watches",
        "smart locks",
        "smart bulbs",
        "smart navigation systems",
        "smart alarm clock",
        "smart thermostat",
        "smart plug",
        "smart light switch",
        "smart tv",
        "smart speaker",
        "smart thermometer",
        "smart video doorbell",
        "smart vacuum cleaner",
        "smart air purifier",
        "gps tracking device",
        "tracking sensor",
        "tracking device",
        "indoor camera",
        "outdoor camera",
        "voice controller",
    ], 50, cooldown=4., random_cooldown=15.),

    Amazon([
        "smart scales",
        "smart watches",
        "smart locks",
        "smart bulbs",
        "smart navigation systems",
        "smart alarm clock",
        "smart thermostat",
        "smart plug",
        "smart light switch",
        "smart tv",
        "smart speaker",
        "smart thermometer",
        "smart video doorbell",
        "smart vacuum cleaner",
        "smart air purifier",
        "gps tracking device",
        "tracking sensor",
        "tracking device",
        "indoor camera",
        "outdoor camera",
        "voice controller",
    ], 50, cooldown=2., random_cooldown=4.),

]
