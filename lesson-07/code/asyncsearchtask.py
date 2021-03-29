# asyncsearchtask.py
#
# Replaces use of requests.get with async aiohttp.get 
#
# Michael Saunby, March 2021

import aiohttp
import json
from searchtask import SearchTask

class AsyncSearchTask(SearchTask):

    async def async_search_task(self, request_queue):
        '''This method is run by the asyncio loop.
        '''
        while request_queue is None:
                await asyncio.sleep(1)
        while True:
            query = await request_queue.get()
            await self.search(query)

    async def search(self,query):
        async with aiohttp.ClientSession() as session:
                async with session.get('https://api.duckduckgo.com',params={'q': query, 'format': 'json'}) as r:             
                    rj = json.loads(await r.text())
                    abstract = rj['AbstractText']
                    self.response["query"] = query
                    self.response["text"] = abstract
                    url = rj['AbstractURL']
                    self.response["url"] = url

