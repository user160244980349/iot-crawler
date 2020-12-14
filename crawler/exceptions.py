

class UrlNotFound(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"Url not found in str: {self.url}"


class PageNotReceived(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"Page on {self.url} has not been received"
