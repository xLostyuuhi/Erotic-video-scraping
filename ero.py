import aiohttp
import asyncio
from bs4 import BeautifulSoup
from numpy import random as rnd

redirects = []

async def send_to_discord(url):
    webhook_url = "webhookurl"
    async with aiohttp.ClientSession() as session:
        payload = {
            "content": url
        }
        async with session.post(webhook_url, json=payload) as response:
            pass 

async def image_get():
    url = ""
    async with aiohttp.ClientSession() as session:
        rnd.shuffle(redirects)
        redirect = redirects.pop()
        async with session.get(redirect) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            price = soup.select('a')
            for elem in price:
                if (elem.get('href').find('/ext_tw_video/') != -1):
                    url = elem.get('href')
                    await send_to_discord(url)
    return url

async def user_get():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://monsnode.com/") as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            price = soup.select('a')
            for elem in price:
                if (elem.get('href').find('/redirect.php?v=') != -1):
                    redirects.append(elem.get('href'))

async def main():
    await user_get()
    for i in range(100):
        await image_get()

asyncio.run(main())