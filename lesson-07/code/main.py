#
import asyncio

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

import requests
from datetime import datetime

queues = (None,None)
response = {"query":"","text":"","url":""}

class MyTextInput(Widget):
    '''See search.kv'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_my_widget, 1 / 10.)

    def update_my_widget(self,delta):
        words = response["text"].split()
        text = ""
        line_len = 0
        max_len = 100
        line_count = 0
        max_lines = 5
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

        self.ids.searchResult.text = response["query"] +"\n" + text + "  " + response["url"]

    def web_search(self, query, button):
        queues["query"].put_nowait(query)

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

class MyTask:
    async def my_other_task(self):
        '''This method is run by the asyncio loop.
        '''
        while queues["query"] is None:
                await asyncio.sleep(1)

        while True:
            global response
            query = await queues["query"].get()
            r = requests.get('https://api.duckduckgo.com', 
                params={'q': query, 'format': 'json'})
            if r:
                abstract = r.json()['AbstractText']
                response["query"] = query
                response["text"] = abstract
                url = r.json()['AbstractURL']
                response["url"] = url


class SearchApp(App):
    
    def build(self):
        return MyLayout()

    def app_func(self):
        '''Wrapper functions for the async processes.
        '''
        async def run_wrapper():
            global queues
            queues = {"query":asyncio.Queue(), "response":asyncio.Queue()}
            # Run the Kivy UI
            await self.async_run()
            exit(0)

        async def my_task_wrapper():
            my_task = MyTask()
            await my_task.my_other_task()

        return asyncio.gather(run_wrapper(), my_task_wrapper())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(SearchApp().app_func())
    loop.close()
