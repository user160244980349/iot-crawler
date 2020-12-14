import re
from time import sleep

from bs4 import BeautifulSoup

from config import cooldown, websites_csv, policies_csv
from crawler.web.driver_factory import DriverFactory
from tools.read.csv import csv_read, csv_write


def scrap_policies(url):
    sleep(cooldown)
    driver = DriverFactory.get()
    markup = driver.get(url[0])
    soup = BeautifulSoup(markup, "html.parser").find("body")
    refs = soup.findAll('a')

    for r in reversed(refs):
        if re.match(r"Privacy Policy", r.text) is not None:

            if re.match(r"^.*\.(com|org|eu).*$", r.get('href')) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                p = f"https://{re.sub(pattern, '', r.get('href'))}"
                return p

            pattern = rf"(^/|/$|//)"
            p = re.sub(pattern, '', r.get('href'))
            return f"{url[0]}/{p}"

    for r in reversed(refs):
        if re.match(r"Privacy", r.text) is not None:

            if re.match(r"^.*\.(com|org|eu).*$", r.get('href')) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                p = f"https://{re.sub(pattern, '', r.get('href'))}"
                return p

            pattern = rf"(^/|/$|//)"
            p = re.sub(pattern, '', r.get('href'))
            return f"{url[0]}/{p}"


def policies(pipe_data: dict):
    threadpool = pipe_data["threadpool"]
    websites = csv_read(websites_csv)
    ps = threadpool.map(scrap_policies, websites)
    ps = [[p] for p in ps if p is not None]
    csv_write(ps, policies_csv)
    return pipe_data
