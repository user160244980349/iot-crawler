import logging
import re
from os import getpid

import requests
from http_request_randomizer.requests.proxy.ProxyObject import Protocol
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

import config


class Proxy:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = _Proxy(config.webdriver_settings)
        return cls._instance


class _Proxy:

    @staticmethod
    def get_ip():
        return re.search(r"\d+\.\d+\.\d+\.\d+",
                         requests.get('http://icanhazip.com/').text).group(0)

    def __init__(self, conf, file=None):

        self.config = conf

        self.req_proxy = RequestProxy(protocol=Protocol.HTTP)
        if file is not None:
            self.proxies_list = self.config["proxies"]
        else:
            self.proxies_list = self.req_proxy.get_proxy_list()

    def get_proxy(self):
        logger = logging.getLogger(f"pid={getpid()}")

        while True:
            p = self.proxies_list.pop(0).get_address()

            try:
                logger.info(f"Trying {p}")
                proxy = {
                    'http': f"http://{p}",
                    # 'https': f"https://{p}"
                }
                ip = re.search(r"\d+\.\d+\.\d+\.\d+",
                               requests.get('http://icanhazip.com/',
                                            proxies=proxy,
                                            timeout=2).text)
                if ip.group(0) is None:
                    raise Exception

                if ip.group(0) == self.get_ip():
                    raise Exception

                if requests.get('http://google.com/',
                                proxies=proxy,
                                timeout=5).status_code != 200:
                    raise Exception

                return p

            except IndexError:
                logger.info(f"Loading more proxies")
                self.proxies_list = self.req_proxy.get_proxy_list()
                pass

            except:
                pass
