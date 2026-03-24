import aiohttp
import asyncio


class DeribitClient:
    URL = "https://www.deribit.com/api/v2/public/get_index_price"

    async def get_price(self, index_name: str, session: aiohttp.ClientSession | None = None) -> float:
        if session is not None:
            return await self._fetch_price(session, index_name)

        async with aiohttp.ClientSession() as internal_session:
            return await self._fetch_price(internal_session, index_name)

    async def _fetch_price(self, session: aiohttp.ClientSession, index_name: str) -> float:
        for attempt in range(3):
            try:
                async with session.get(
                    self.URL,
                    params={"index_name": index_name},
                    timeout=5
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data["result"]["index_price"]
            except (aiohttp.ClientError, asyncio.TimeoutError, KeyError):
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def get_prices(self, index_names: list[str]) -> list[float | Exception]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_price(index_name, session=session) for index_name in index_names]
            return await asyncio.gather(*tasks, return_exceptions=True)
