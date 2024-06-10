import json
import httpx
import asyncio

class AsyncHTTP:
    def get_or_create_eventloop(self):
        # https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
        try:
            return asyncio.get_event_loop()
        except RuntimeError as err:
            if "There is no current event loop in thread" in str(err):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def _read_lines(self, url: str, client: httpx.AsyncClient):
        assert len(url) > 10
        try:
            async with client.stream("GET", url) as resp:
                async for line in resp.aiter_lines():
                    yield json.loads(line)
        except httpx.RemoteProtocolError as e:
            print('read_lines: ', e)
            yield e


async def get_catalog_v2():
    url = 'https://a.4cdn.org/wg/catalog.json'
    client = httpx.AsyncClient()
    aa = AsyncHTTP()
    async_gen = aa._read_lines(url, client)

    all_posts = []
    # _type = ''
    async for page in async_gen:
        # _type = type(page)
        for thread in page:
            for item in thread['threads']:
                all_posts.append(item)

            # all_posts.append(thread)
            # thread = jsonable_encoder(thread)
            # all_posts.append(CatalogThread(**thread))
    # print(_type)
    await async_gen.aclose()
    await client.aclose()
    return all_posts
