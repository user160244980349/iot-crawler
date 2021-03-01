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

    def __init__(self, sim=.6, delay=0., random_delay=0.):
        self.similarity = sim
        self.delay = delay
        self.random_delay = random_delay
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def search(self, content):

        driver = Driver()

        timeout_attempts = 0
        error_attempts = 0
        captcha_attempts = 0

        while True:

            try:
                return self.results(content)

            except TimeoutException:
                self.logger.warning("Slow connection")
                driver.change_proxy()
                if timeout_attempts > config.max_timeout_attempts:
                    return None

            except CaptchaException:
                self.logger.warning("Google knows that this is automation script")
                driver.change_proxy()
                if captcha_attempts > config.max_captcha_attempts:
                    return None

            except WebDriverException:
                self.logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                if error_attempts > config.max_error_attempts:
                    return None

    def results(self, content):
        driver = Driver()

        sleep(self.delay + random.random() * self.random_delay)
        driver.get(f"https://www.google.com")
        sleep(self.delay + random.random() * self.random_delay)

        search = driver.manage().find_element_by_name("q")
        search.send_keys(content)
        search.send_keys(Keys.RETURN)

        driver.wait(ec.presence_of_element_located((By.TAG_NAME, "cite")))

        soup = BeautifulSoup(driver.source(), "lxml")

        if re.search(r"captcha", str(soup), flags=re.IGNORECASE) is not None:
            raise CaptchaException

        return self.similarity_filter(content, soup, threshold=self.similarity)

    @staticmethod
    def similarity_filter(content, soup, threshold=.6):
        best_url = None
        best_similarity = threshold

        for c in soup.find_all("cite"):

            m = re.match(r"^((https?://)?(www\.)?([\w\d.\-_]+)(\.\w+)).*$", c.text)

            content = re.sub(r"([^\w ]+)|(\s{2,})", " ", content)
            content_pieces = content.split()
            if len(content_pieces) > 1:
                content_pieces.append("".join(content_pieces))

            for piece in content_pieces:
                if m is not None:
                    domain = m.group(4)
                    sim = similarity(piece, domain)

                    if sim > best_similarity:

                        w3 = m.group(3)
                        if w3 is None:
                            w3 = ""

                        best_url = f"https://{w3}{m.group(4)}{m.group(5)}"
                        best_similarity = sim

        if best_url is not None:
            return best_url
