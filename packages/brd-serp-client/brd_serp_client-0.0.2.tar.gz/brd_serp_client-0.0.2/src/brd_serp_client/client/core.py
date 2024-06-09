import aiohttp


################################################################
# Base Class
################################################################
class BRDProxy:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.api_token = api_token
        self.proxy = "https://brd.superproxy.io:22225"
        self.proxy_auth = aiohttp.BasicAuth(username, password)

    async def get(self, **params):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, proxy=self.proxy, proxy_auth=self.proxy_auth, params=params
            ) as response:
                response.raise_for_status()
                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()