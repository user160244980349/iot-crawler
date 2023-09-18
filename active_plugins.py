from config import paths
from crawler.plugins.amazon import Amazon
from crawler.plugins.walmart import Walmart


# Plugins for mining IoT privacy policies
plugins = [

    # Walmart(["voice controller", "outdoor camera", "indoor camera",
    #          "tracking device", "tracking sensor", "gps tracking device",
    #          "smart air purifier", "robot vacuum cleaner",
    #          "smart video doorbell", "smart air conditioner",
    #          "smart thermometer", "smart speaker", "smart tv",
    #          "smart light switch", "smart plug", "smart thermostat",
    #          "smart alarm clock", "smart navigation system", "smart bulb",
    #          "smart lock", "smart bracelet", "smart watch", "smart scale"],
    #         1, paths.json.products, cooldown=2., random_cooldown=2.),

    Amazon(["voice controller", "outdoor camera", "indoor camera",
            "tracking device", "tracking sensor", "gps tracking device",
            "smart air purifier", "robot vacuum cleaner",
            "smart video doorbell", "smart air conditioner",
            "smart thermometer", "smart speaker", "smart tv",
            "smart light switch", "smart plug", "smart thermostat",
            "smart alarm clock", "smart navigation system", "smart bulb",
            "smart lock", "smart bracelet", "smart watch", "smart scale"],
           1, paths.json.products, cooldown=2., random_cooldown=2.),

]
