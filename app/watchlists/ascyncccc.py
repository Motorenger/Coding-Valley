import asyncio

import aiohttp


API_KEY = "427c3e4e"


def get_tasks(session, series_data):
    tasks = []
    for season_number in range(1, int(series_data[1]) + 1):
        url = f"https://www.omdbapi.com?apikey={API_KEY}&i={series_data[0]}&Season={season_number}"
        tasks.append(session.get(url))
    return tasks


async def download_seasons():
    async with aiohttp.ClientSession() as session:
        series_data = ("tt1632701", 9)
        tasks = get_tasks(session, series_data)
        response = await asyncio.gather(*tasks)
        resp = []
        for s in response:
            resp.append(await s.json())
        return resp


a = asyncio.run(download_seasons())

print(a)