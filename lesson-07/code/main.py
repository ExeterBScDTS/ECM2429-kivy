##
# Kivy example calling a web API using asyncio and aiohttp
# Compare with the simpler version using requests
#
# Michael Saunby, March 2021

import asyncio

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

from datetime import datetime
import aiohttp
import json

request_queue = None

class MyTextInput(Widget):
    '''See search.kv'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_my_widget, 1 / 10.)

    def summary_block(self, words:str, max_len=100, max_lines=4):
        text = ""
        line_len = 0
        line_count = 0
        for w in words:
            if line_count > max_lines:
                text += "..."
                break
            if line_len + 1 + len(w) < max_len:
                text += " " + w
                line_len += 1 + len(w)
            else:
                line_count += 1
                text += "\n"
                text += w
                line_len = len(w)
        return text

    def update_my_widget(self,delta):
        response = search_task.get_response()
        summary = self.summary_block(response["text"].split())
        self.ids.searchResult.text = response["query"] +"\n" + summary + "\n" + response["url"]

    def web_search(self, query, button):
        request_queue.put_nowait(query)

class MyClock(Widget):
    '''See search.kv'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_my_widget, 1 / 10.)
    
    def update_my_widget(self,delta):
        self.ids.date.text = str(datetime.today().date())
        self.ids.time.text = str(datetime.today().time())[0:8]

class MyLayout(Widget):
    '''See search.kv'''
    pass

class SearchTask:
    def __init__(self):
        self.response = {"query":"","text":"","url":""}

    async def my_other_task(self):
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

    def get_response(self):
        '''
        Returns the most recent response.
        If a new request has been submitted, this won't wait, it simply 
        returns the previous response.
        '''
        return self.response


class SearchApp(App):
    
    def build(self):
        return MyLayout()

    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        async def run_wrapper():
            global request_queue
            request_queue = asyncio.Queue()
            # Run the Kivy UI
            await self.async_run()
            exit(0)

        async def my_task_wrapper():
            global search_task
            search_task = SearchTask()
            await search_task.my_other_task()

        return asyncio.gather(run_wrapper(), my_task_wrapper())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SearchApp().app_func())
    loop.close()
