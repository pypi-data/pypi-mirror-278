import aiohttp
import asyncio


class BanChecker:
    def __init__(self):
        self.urls = [
            "https://lols.bot/?a={user_id}",
            "https://api.cas.chat/check?user_id={user_id}",
            "https://api.spamwat.ch/banlist/{user_id}",
        ]

    async def fetch(
        self, url: str, session: aiohttp.ClientSession, user_id: int
    ) -> dict:
        try:
            headers = {}
            f_api = {
                "https://api.spamwat.ch/banlist/{user_id}".format(
                    user_id=user_id
                ): "xgBmNRqHZFeTu24IqhDarerUSXk4mPpu~ken9~Q1l1RhFb1Pmx5mA1bvZgvTRfp9"
            }
            if url in f_api:
                headers["Authorization"] = f"Bearer {f_api[url]}"
            async with session.get(
                url,
                ssl=False,
                timeout=aiohttp.ClientTimeout(total=10, connect=5),
                headers=headers,
            ) as response:
                if response.status < 200 and response.status >= 400:
                    return {}
                return await response.json()
        except Exception as e:
            return {"Error": e}

    async def get_ban_status(self, user_id: int) -> bool:
        formatted_urls = [url.format(user_id=user_id) for url in self.urls]
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(url, session, user_id) for url in formatted_urls]
            responses = await asyncio.gather(*tasks)
        results = []
        lols = []
        for response in responses:
            print(response) # for debug
            if "Error" in response:
                results.append(False)
                continue
            if "banned" in response:
                results.append(response.get("banned", False))
            elif "ok" in response:
                results.append(response.get("ok", False))
            elif "code" in response and (
                response["code"] == 404 or response["code"] == 401
            ):
                results.append(False)
            else:
                results.append(True)
            if "spam_factor" in response:
                lols.append(response.get("spam_factor", 0))
            else:
                lols.append(None)

        return await check(results, lols)


async def check(answer: list, answer2: list) -> bool:
    if True in answer or (answer2[0] is not None and answer2[0] > 10):
        return True
    else:
        return False