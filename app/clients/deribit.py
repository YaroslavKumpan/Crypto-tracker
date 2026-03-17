import aiohttp
import asyncio


class DeribitClient:
    URL = "https://www.deribit.com/api/v2/public/get_index_price"

    async def get_price(self, index_name: str) -> float:
        for attempt in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.URL,
                        params={"index_name": index_name},
                        timeout=5
                    ) as resp:
                        data = await resp.json()
                        return data["result"]["index_price"]

            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)