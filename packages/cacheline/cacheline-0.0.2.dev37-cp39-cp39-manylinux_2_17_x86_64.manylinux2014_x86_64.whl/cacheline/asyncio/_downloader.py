from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable, Optional

import aiofiles
import aiohttp

from cacheline.logging import getLogger

if TYPE_CHECKING:
    from pathlib import Path

logger = getLogger(__name__)


async def download(
    uri: str,
    path: Path,
    *,
    chunk_size: int = 8192,
    on_progress: Optional[Callable[[int, int], None]] = None,
):
    """
    asynchronous download file from uri to local path
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiohttp.ClientSession() as session, session.get(
        uri,
    ) as resp:
        if resp.status != 200:
            raise RuntimeError(f"download bag failed, status {resp.status}")
        total_size = int(resp.headers.get("content-length", 0))
        logger.debug("downloading %s bytes to %s", total_size, path)
        percent = 0.0
        async with aiofiles.open(f"{path}.wip", "wb") as f:
            chunk = await resp.content.read(chunk_size)
            acc = 0
            while chunk:
                acc += await f.write(chunk)
                _p = round(acc / total_size * 100, 1)
                if _p != percent or acc == total_size:
                    percent = _p
                    _ = on_progress and on_progress(acc, total_size)
                    logger.debug("downloaded %s", percent)
                chunk = await resp.content.read(chunk_size)
        os.rename(f"{path}.wip", path)
