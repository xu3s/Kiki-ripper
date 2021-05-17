import os
import asyncio
import aiohttp
import aiofiles


async def series_detail(data):
    author = data['author']
    stitle = data['name']
    site = data['site']
    comicid = data['comicid']
    cover = data['cover_image_url']
    desc = data['desc']
    surl = data['source_url']
