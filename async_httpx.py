import asyncio
import time
import requests
import httpx

sites = (
    "https://www.google.com",
    "https://www.facebook.com",
    "https://instagram.com",
    "https://bing.com",
    "https://web.whatsapp.com",
    "https://youtube.com",
    "https://amazon.com",
    "https://yahoo.com",
    "https://wikipedia.org",
    "https://reddit.com",
    "https://walmart.com",
    "https://ebay.com",
    "https://twitter.com",
    "https://fandom.com",
    "https://cnn.com",
    "https://pinterest.com",
    "https://foxnews.com"
)

def syn_requester(site):
    modified = 0
    text = requests.get(site).text
    for i in text:
        if i in "<>":
            modified+=1
    for i in text[-1:]:
        if i in "<>":
            modified+=1
    print(f"{site=}")

    


def syn_main_caller():
    routines = [syn_requester(site) for site in sites]
    


async def requester(site, klient):
    modified = 0
    data = await klient.get(site)
    print(f"{site=}")
    # return requests.get(site).text
    
async def main_caller():
    async with httpx.AsyncClient() as klient:
        routines = [requester(site, klient) for site in sites]
        await asyncio.gather(*routines)


def main():

    import cProfile
    import pstats
    
    with cProfile.Profile() as profiler:
        asyncio.run(main_caller())
        # syn_main_caller()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats("py_stats.prof")


def main2():
    start = time.perf_counter()
    asyncio.run(main_caller())
    # syn_main_caller()
    print("time taken = ", time.perf_counter() - start)


if __name__=="__main__":
    main2()
