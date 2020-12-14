import threading
from os.path import join

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager

from config import resources
from crawler.web.useragent import get_user_agent


threadLocal = threading.local()


class DriverFactory:

    path = None

    @classmethod
    def _install(cls):

        print("Checking driver")

        try:
            with open(join(resources, ".driver"), "r") as f:
                cls.path = f.read()
                f.close()

        except FileNotFoundError:
            print("Driver not found, installing")
            with open(join(resources, ".driver"), "w") as f:
                cls.path = GeckoDriverManager().install()
                f.write(cls.path)
                f.close()

        print(f"Loading driver: {cls.path}")

    @classmethod
    def _instantiate(cls):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--lang=en-US")
        options.add_argument(f"--user-agent='{get_user_agent()}'")
        caps = webdriver.DesiredCapabilities().FIREFOX
        return webdriver.Firefox(
            executable_path=DriverFactory.path,
            firefox_options=options,
        )

    @classmethod
    def get(cls):
        wrapper = getattr(threadLocal, "driver", None)

        if wrapper is None:
            DriverFactory._install()
            wrapper = DriverWrapper(DriverFactory._instantiate())

            setattr(threadLocal, "driver", wrapper)

        return wrapper


class DriverWrapper:

    def __init__(self, driver):
        self._driver = driver
        self._tab = None

    def get(self, url):
        try:
            self._driver.get(url)
        except WebDriverException:
            print("Cant establish the connection")
            return "<body></body>"
        return self._driver.page_source

    def __del__(self):
        self._driver.quit()
