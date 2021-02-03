import logging
import os
import random

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

import config
from crawler.web.proxy import Proxy
from tools.text import parse_proxy


class Driver:

    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = _DriverInstance(config.webdriver_settings)
        return cls._instance

    @classmethod
    def close(cls, *args, **kwargs):
        if cls._instance is not None:
            cls._instance.__del__()
            cls._instance = None


class _DriverInstance:

    def __init__(self, conf):

        self.config = conf

        self.logger = logging.getLogger(f"pid={os.getpid()} | Webdriver")
        self.logger.setLevel(self.config["log_level"])

        self._executable_path = None
        self._service_log_path = os.path.join(os.path.abspath(self.config["log_path"]))
        self._check_installation()

        self._capabilities = DesiredCapabilities.FIREFOX
        self._capabilities["unexpectedAlertBehaviour"] = "accept"

        self._profile = webdriver.FirefoxProfile(os.path.abspath(self.config["profile_path"]))
        if self.config["no_cache"]:
            self._profile.set_preference("browser.cache.disk.enable", False)
            self._profile.set_preference("browser.cache.memory.enable", False)
            self._profile.set_preference("browser.cache.offline.enable", False)
            self._profile.set_preference("network.http.use-cache", False)
            self._profile.set_preference("intl.accept_languages", "en-us")
        self._profile.update_preferences()

        self._options = webdriver.FirefoxOptions()
        self._options.add_argument(f"--user-agent='{random.choice(self.config['user_agents'])}'")
        self._options.add_argument("--disable-blink-features")
        self._options.add_argument("--disable-gpu")
        self._options.add_argument("--no-sandbox")

        if self.config["headless"]:
            self._options.add_argument("--headless")

        self._driver = webdriver.Firefox(
            firefox_profile=self._profile,
            firefox_options=self._options,
            executable_path=self._executable_path,
            capabilities=self._capabilities,
            service_log_path=self._service_log_path
        )

    def _check_installation(self):

        self.logger.info("Checking installed driver")

        try:
            with open(os.path.abspath(self.config["dotfile"]), "r") as f:
                self._executable_path = f.read()

        except FileNotFoundError:
            self.logger.info("Driver not found, installing...")
            self._executable_path = GeckoDriverManager().install()
            with open(os.path.abspath(self.config["dotfile"]), "w") as f:
                f.write(self._executable_path)

        self.logger.info(f"Loading driver: {self._executable_path}")

    def manage(self):
        return self._driver

    def source(self):
        return self._driver.page_source

    def get(self, url):

        if url is None:
            raise ValueError("Null url")

        self.logger.info(f"Going to {url}")

        self._driver.get(url)

        return self._driver.page_source

    def wait(self, event, timeout=15):
        WebDriverWait(self._driver, timeout).until(event)

    def change_proxy(self):

        if not self.config["use_proxy"]:
            return

        p_str = Proxy().get_proxy()
        p = parse_proxy(p_str)

        self.logger.info(f"Switching to {p_str} proxy")

        self._profile.set_preference("network.proxy.type", 1)
        self._profile.set_preference("network.proxy.http", p[0])
        self._profile.set_preference("network.proxy.http_port", p[1])
        self._profile.set_preference("network.proxy.ssl", p[0])
        self._profile.set_preference("network.proxy.ssl_port", p[1])
        self._profile.set_preference("network.proxy.ftp", p[0])
        self._profile.set_preference("network.proxy.ftp_port", p[1])

        self._driver.quit()
        self._driver = webdriver.Firefox(
            firefox_profile=self._profile,
            firefox_options=self._options,
            executable_path=self._executable_path,
            capabilities=self._capabilities,
            service_log_path=self._service_log_path
        )

    def reset(self):

        self._driver.quit()
        self._driver = webdriver.Firefox(
            firefox_profile=self._profile,
            firefox_options=self._options,
            executable_path=self._executable_path,
            capabilities=self._capabilities,
            service_log_path=self._service_log_path
        )

    def __del__(self):
        self._driver.quit()
        self.logger.info("Driver has been closed")
