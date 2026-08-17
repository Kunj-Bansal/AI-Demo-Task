import asyncio
import aiohttp

class DataScraper:
    def __init__(self, concurrency_limit: int = 20):
        self.semaphore = asyncio.Semaphore(concurrency_limit)

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        async with self.semaphore:
            try:
                async with session.get(url, timeout=10) as response:
                    return await response.text()
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return ""