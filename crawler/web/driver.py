import logging
import os
import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

import config
from crawler.web.proxy import Proxy
from tools.text import parse_proxy


class Driver:

    @classmethod
    def __new__(cls, *args, **kwargs):

        if hasattr(cls, "_instance"):
            return cls._instance

        setattr(cls, "_instance", _DriverInstance(config.webdriver_settings))
        return getattr(cls, "_instance")

    @classmethod
    def close(cls, *args, **kwargs):

        if not hasattr(cls, "_instance"):
            return

        delattr(cls, "_instance")


class _DriverInstance:

    def __init__(self, conf):

        self.config = conf

        self.logger = logging.getLogger(f"pid={os.getpid()}")
        self.logger.setLevel(self.config["log_level"])

        self._executable_path = None
        self._service_log_path = os.path.join(os.path.abspath(self.config["log_path"]))
        self._check_installation()

        self._profile = webdriver.FirefoxProfile(os.path.abspath(self.config['profile_path']))
        if self.config["no_cache"]:
            self._profile.set_preference("browser.cache.disk.enable", False)
            self._profile.set_preference("browser.cache.memory.enable", False)
            self._profile.set_preference("browser.cache.offline.enable", False)
            self._profile.set_preference("network.http.use-cache", False)
            self._profile.set_preference("dom.webdriver.enabled", False)
            self._profile.set_preference("marionette.enabled", False)
        self._profile.set_preference("general.useragent.override", random.choice(self.config['user_agents']))
        self._profile.set_preference("intl.accept_languages", "en-US, en")
        self._profile.update_preferences()

        self._options = webdriver.FirefoxOptions()
        self._options.add_argument("--no-sandbox")

        if self.config["headless"]:
            self._options.add_argument("--headless")
            self._options.add_argument('--disable-gpu')

        self._capabilities = self._options.to_capabilities()
        self._capabilities["unexpectedAlertBehaviour"] = "accept"

        self._driver = webdriver.Firefox(
            firefox_profile=self._profile,
            firefox_options=self._options,
            executable_path=self._executable_path,
            capabilities=self._capabilities,
            service_log_path=self._service_log_path
        )
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _check_installation(self):

        self.logger.info("Checking installed driver")

        try:
            with open(os.path.abspath(self.config["dotfile"]), "r") as f:
                self._executable_path = f.read()

        except FileNotFoundError:
            self.logger.info("Driver is not found, installing...")
            self._executable_path = GeckoDriverManager().install()
            with open(os.path.abspath(self.config["dotfile"]), "w") as f:
                f.write(self._executable_path)

        self.logger.info(f"Loading driver: {self._executable_path}")

    def manage(self):
        return self._driver

    def source(self):
        return self._driver.page_source

    def get(self, url, remove_invisible=False):

        if url is None:
            raise ValueError("Null url")

        self.logger.info(f"Going to {url}")
        self._driver.get(url)

        if remove_invisible:
            self._driver.execute_script(
                """
                (function() {
                
                  function load_jq(callback) {
                    var script = document.createElement("script")
                    script.type = "text/javascript";
                    script.src = "https://code.jquery.com/jquery-3.5.1.min.js";
                    document.getElementsByTagName("head")[0].appendChild(script);
                  }
                
                  function remove_invisible() {
                    var $ = window.jQuery;
                    $('*').each(function() {
                      if ($(this).css('visibility') == 'hidden' ||
                        $(this).css('display') == 'none') {
                        $(this).remove()
                      }
                    });
                  }
                
                
                  function try_remove() {
                
                    try {
                      remove_invisible()
                    } catch (e) {
                      setTimeout(try_remove, 100)
                    }
                
                  }
                
                
                  try {
                    remove_invisible()
                  } catch (e) {
                    load_jq()
                    setTimeout(try_remove, 100)
                  }
                
                })();
                """
            )

        return self._driver.page_source

    def wait(self, event, timeout=15):
        WebDriverWait(self._driver, timeout).until(event)

    def clear_cookies(self):
        self._driver.delete_all_cookies()

    def change_useragent(self):
        self._profile.set_preference("general.useragent.override",
                                     random.choice(self.config['user_agents']))
        self._profile.update_preferences()

    def restart_session(self):
        self._driver.close()
        self._driver.start_session(capabilities=self._capabilities,
                                   browser_profile=self._profile)

    def change_proxy(self):

        if not self.config["use_proxy"]:
            return

        proxy = Proxy()
        p_str = proxy.get_proxy()
        p = parse_proxy(p_str)

        self.logger.info(f"Switching to {p_str} proxy")

        self._profile.set_preference("network.proxy.type", 1)
        self._profile.set_preference("network.proxy.http", p[0])
        self._profile.set_preference("network.proxy.http_port", p[1])
        self._profile.set_preference("network.proxy.ssl", p[0])
        self._profile.set_preference("network.proxy.ssl_port", p[1])
        self._profile.set_preference("network.proxy.ftp", p[0])
        self._profile.set_preference("network.proxy.ftp_port", p[1])
        self._profile.update_preferences()

    def __del__(self):

        if self._driver is None:
            return

        self._driver.quit()
        del self._driver
        self.logger.info("Driver has been closed")
