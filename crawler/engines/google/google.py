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
from crawler.engines.google.filters import check_similarity, check_first, similarity
from crawler.web.driver import Driver
from tools.exceptions import CaptchaException


class GoogleEngine(Engine):

    def __init__(self, delay=0., random_delay=0.):
        self.delay = delay
        self.random_delay = random_delay
        self.logger = logging.getLogger(f"pid={os.getpid()} | GoogleEngine")

    def search(self, content):

        driver = Driver()

        timeout_attempts = 0
        error_attempts = 0
        captcha_attempts = 0

        while True:

            try:
                return self.results(content)

            except TimeoutException as e:
                self.logger.warning("Slow connection")
                driver.change_proxy()
                if timeout_attempts > config.max_timeout_attempts:
                    return None

            except CaptchaException as e:
                self.logger.warning("Google knows that this is automation script")
                driver.change_proxy()
                if captcha_attempts > config.max_captcha_attempts:
                    return None

            except WebDriverException as e:
                self.logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                if error_attempts > config.max_error_attempts:
                    return None

    def results(self, content):
        driver = Driver()

        sleep(self.delay + random.random() * self.random_delay)
        driver.get(f"http://www.google.com")
        sleep(self.delay + random.random() * self.random_delay)

        search = driver.manage().find_element_by_name('q')
        search.send_keys(content)
        search.send_keys(Keys.RETURN)

        driver.wait(ec.presence_of_element_located((By.TAG_NAME, "cite")))

        soup = BeautifulSoup(driver.source(), "lxml")

        if re.search(r"captcha", str(soup), flags=re.IGNORECASE) is not None:
            raise CaptchaException

        return check_similarity(content, soup)

