
import asyncio
from typing import Any

from playwright.async_api import Page

from harambe import SDK


async def scrape(sdk: SDK, url: str, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await asyncio.sleep(20)
    await page.wait_for_selector("div.table_wrapper table tbody tr td a")
    links = await page.query_selector_all("div.table_wrapper table tbody tr td a")
    for link in links:
        href = await link.get_attribute("href")
        await sdk.enqueue(href)

if __name__ == "__main__":
    asyncio.run(SDK.run(scrape, "https://account.bonfirehub.com/login", {}))
