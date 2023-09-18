import logging
import os
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from crawler.engines.engine import Engine
from crawler.web.driver import Driver
from tools.text import similarity


class GoogleEngine(Engine):
    href = re.compile(r"^((https?://)?(www\.)?([\w.\-_]+)(\.\w+)).*$")
    request = re.compile(r"([^\w ]+)|(\s{2,})")

    def __init__(self, similarity_threshold=.6, cooldown=0.,
                 random_cooldown=0.):
        self.logger = logging.getLogger(f"pid={os.getpid()}")

        self.similarity = similarity_threshold
        self.cooldown = cooldown
        self.random_cooldown = random_cooldown

    def search(self, manufacturer, keyword):
        Driver().sleep(self.cooldown, self.random_cooldown)
        Driver().manage().get(f"https://www.google.com")
        search = Driver().manage().find_element_by_name("q")
        search.send_keys(f"{manufacturer} {keyword}")
        search.send_keys(Keys.RETURN)
        Driver().wait(ec.presence_of_element_located((By.TAG_NAME, "cite")))
        soup = BeautifulSoup(Driver().source(), "lxml")
        return self.similarity_filter(manufacturer, soup,
                                      threshold=self.similarity)

    def similarity_filter(self, content, soup, threshold=.6):
        best_url = None
        best_similarity = threshold

        for c in soup.findAll("cite"):
            m = self.href.match(c.text)
            if m is None:
                break

            content_list = self.request.sub(" ", content).split()
            if len(content_list) > 1:
                content_list.append("".join(content_list))

            domain = m.group(4)
            for piece in content_list:
                sim = similarity(piece, domain)

                if sim > best_similarity or domain in piece:
                    w3 = m.group(3)
                    if w3 is None:
                        w3 = ""

                    best_url = f"http://{w3}{m.group(4)}{m.group(5)}"
                    best_similarity = sim

        return best_url
