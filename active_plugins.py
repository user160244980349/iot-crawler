from crawler.plugins.amazon import Amazon

plugins = [

    # Walmart(["smart scales"], 1, cooldown=10., sync=True),
    Amazon(["smart scales"], 1, cooldown=3.),

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
    # ], 50, cooldown=10.),
    #
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
    # ], 50, cooldown=3.),

]
