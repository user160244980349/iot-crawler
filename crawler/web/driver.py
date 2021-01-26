import logging
from os import getpid
from os.path import join
from time import sleep, time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager

from config import resources, request_interval
from crawler.web.useragent import get_user_agent


class Driver(object):

    @classmethod
    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)

            cls._instance._path = None
            cls._instance._last_request = time()
            cls._instance._check_installation()

            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--lang=en-US")
            options.add_argument(f"--user-agent='{get_user_agent()}'")

            cls._instance._driver = webdriver.Firefox(
                executable_path=cls._instance._path,
                firefox_options=options,
            )

        return cls._instance

    @classmethod
    def close(cls, *args, **kwargs):
        if hasattr(cls, "_instance"):
            del cls._instance

    def _check_installation(self):

        logger = logging.getLogger(f"pid={getpid()}")
        logger.info("Checking driver")

        try:
            with open(join(resources, ".driver"), "r") as f:
                self._path = f.read()
                f.close()

        except FileNotFoundError:
            logger.info("Driver not found, installing...")
            with open(join(resources, ".driver"), "w") as f:
                self._path = GeckoDriverManager().install()
                f.write(self._path)
                f.close()

        logger.info(f"Loading driver: {self._path}")

    def get(self, url, delayed=False):
        try:
            if delayed:
                sleep(request_interval - (time() - self._last_request))
            self._driver.get(url)
            self._last_request = time()
        except WebDriverException:
            logger = logging.getLogger(f"pid={getpid()}")
            logger.warning("Cant establish the connection")
            return None
        return self._driver.page_source

    def __del__(self):
        logger = logging.getLogger(f"pid={getpid()}")
        logger.info("Closing driver")
        self._driver.quit()
