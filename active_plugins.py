from crawler.plugins.amazon import Amazon
from crawler.plugins.walmart import Walmart

plugins = [

    # Amazon(["smart scales"], 1, cooldown=3.),
    Walmart(["smart scales"], 1, cooldown=10.),
    # Amazon([
    #     "smart scales",
    #     "smart watches",
    #     "smart locks",
    #     "smart bulbs",
    #     "indoor camera",
    #     "outdoor camera",
    #     "smart navigation systems",
    #     "gps tracking device",
    #     "voice controller",
    #     "tracking sensor",
    #     "tracking device",
    #     "smart alarm clock",
    #     "smart thermostat",
    #     "smart plug",
    #     "smart light switch"
    #     "smart tv",
    #     "smart speaker",
    #     "smart thermometer",
    #     "smart video doorbell",
    # ], 50),
    # Walmart([
    #     "smart scales",
    #     "smart watches",
    #     "smart locks",
    #     "smart bulbs",
    #     "indoor camera",
    #     "outdoor camera",
    #     "smart navigation systems",
    #     "gps tracking device",
    #     "voice controller",
    #     "tracking sensor",
    #     "tracking device",
    #     "smart alarm clock",
    #     "smart thermostat",
    #     "smart plug",
    #     "smart light switch"
    #     "smart tv",
    #     "smart speaker",
    #     "smart thermometer",
    #     "smart video doorbell",
    # ], 50)

]
