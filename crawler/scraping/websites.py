import re
from random import random
from time import sleep

from bs4 import BeautifulSoup

from config import cooldown, manufacturers_csv, websites_csv, multiplier
from crawler.web.driver_factory import DriverFactory
from tools.read.csv import csv_read, csv_write


def scrap_sites(request):
    sleep(cooldown + random() * multiplier)
    driver = DriverFactory.get()
    markup = driver.get(f"https://www.google.com/search?q={request[0]}+com")
    soup = BeautifulSoup(markup, "html.parser").find("body").find("cite")
    if soup is not None:
        return f"{soup.text}"


def websites(pipe_data: dict):
    threadpool = pipe_data["threadpool"]
    manufacturers = csv_read(manufacturers_csv)
    web = threadpool.map(scrap_sites, manufacturers)
    pattern = r"(^http://|^https://|www\.|/$)"
    csv_write([[f"https://{re.sub(pattern, '', w)}"] for w in web
               if re.match(r"^.*\.(com|org|eu)$", w) is not None], websites_csv)
    return pipe_data
