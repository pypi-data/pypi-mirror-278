import aiohttp


################################################################
# Base Class
################################################################
class BRDProxy:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.proxy = "https://brd.superproxy.io:22225"
        self.proxy_auth = aiohttp.BasicAuth(username, password)
