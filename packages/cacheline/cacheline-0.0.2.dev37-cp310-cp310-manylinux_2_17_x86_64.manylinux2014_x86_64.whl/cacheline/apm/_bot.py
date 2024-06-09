from urllib.parse import urljoin

import aiohttp


class Bot:
    def __init__(self, server: str):
        self._server = server

    async def send_msg(self, msg: str, *, channel: str = "", thread: str = ""):
        if thread and not channel:
            raise ValueError("thread must be used with channel")
        path = "/api/v1/send_text"
        if channel:
            path = f"/api/v1/send_text/{channel}"
        if thread:
            path = f"/api/v1/send_text/{channel}/{thread}"
        async with aiohttp.ClientSession() as session:
            await session.post(urljoin(self._server, path), data=msg)


