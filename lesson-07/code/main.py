##
# Kivy example calling a web API using asyncio and aiohttp
# Compare with the simpler version using requests
#
# Michael Saunby, March 2021

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

from datetime import datetime

import asyncio
from asyncsearchtask import AsyncSearchTask

# Global variables use to communicate between async tasks
request_queue : asyncio.Queue = None
search_task : AsyncSearchTask = None

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

class SearchApp(App):
    
    def build(self):
        return MyLayout()

    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        async def run_wrapper():
            # Run the Kivy UI
            await self.async_run()
            exit(0)

        async def my_task_wrapper():
            # Run the web search task
            global search_task, request_queue
            search_task = AsyncSearchTask()
            request_queue = asyncio.Queue()
            await search_task.async_search_task(request_queue)

        return asyncio.gather(run_wrapper(), my_task_wrapper())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SearchApp().app_func())
    loop.close()
