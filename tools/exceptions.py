class UrlNotFound(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"Url not found in str: {self.url}"


class CaptchaException(Exception):

    def __str__(self):
        return f"The website have gave out a captcha"
