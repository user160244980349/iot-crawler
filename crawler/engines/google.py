import logging
import os
import random
import re
from time import sleep

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

import config
from crawler.engines.engine import Engine
from crawler.web.driver import Driver
from tools.exceptions import CaptchaException
from tools.text import similarity


class GoogleEngine(Engine):
    href = re.compile(r"^((https?://)?(www\.)?([\w.\-_]+)(\.\w+)).*$")
    request = re.compile(r"([^\w ]+)|(\s{2,})")
    captcha = re.compile(r"captcha", flags=re.IGNORECASE)

    def __init__(self, sim=.6, delay=0., random_delay=0.):
        self.similarity = sim
        self.delay = delay
        self.random_delay = random_delay
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def search(self, manufacturer, keyword):

        net_error = 0

        while True:

            driver = Driver()

            driver.change_proxy()
            driver.change_useragent()
            driver.restart_session()

            try:
                return self.results(manufacturer, keyword)

            except TimeoutException:
                self.logger.warning("Slow connection")
                net_error += 1
                if net_error > config.max_timeout_attempts:
                    return None

            except CaptchaException:
                self.logger.warning("Google knows that this is automation script")
                net_error += 1
                if net_error > config.max_captcha_attempts:
                    return None

            except WebDriverException:
                self.logger.warning(f"Web driver exception, potentially net error")
                net_error += 1
                if net_error > config.max_error_attempts:
                    return None

    def results(self, manufacturer, keyword):
        driver = Driver()

        sleep(self.delay + random.random() * self.random_delay)
        driver.get(f"https://www.google.com")
        sleep(self.delay + random.random() * self.random_delay)

        search = driver.manage().find_element_by_name("q")
        search.send_keys(f"{manufacturer} {keyword}")
        search.send_keys(Keys.RETURN)

        driver.wait(ec.presence_of_element_located((By.TAG_NAME, "cite")))

        soup = BeautifulSoup(driver.source(), "lxml")

        if GoogleEngine.captcha.match(str(soup)) is not None:
            raise CaptchaException()

        return self.similarity_filter(manufacturer, soup, threshold=self.similarity)

    @classmethod
    def similarity_filter(cls, content, soup, threshold=.6):
        best_url = None
        best_similarity = threshold

        for c in soup.findAll("cite"):

            m = cls.href.match(c.text)

            content_list = cls.request.sub(" ", content).split()
            if len(content_list) > 1:
                content_list.append("".join(content_list))

            for piece in content_list:
                if m is not None:
                    domain = m.group(4)
                    sim = similarity(piece, domain)

                    if sim > best_similarity or domain in piece:

                        w3 = m.group(3)
                        if w3 is None:
                            w3 = ""

                        best_url = f"https://{w3}{m.group(4)}{m.group(5)}"
                        best_similarity = sim

        return best_url
