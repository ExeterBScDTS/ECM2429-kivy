#
import asyncio

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

import requests
from datetime import datetime

queues = (None,None)

class MyTextInput(Widget):

    def web_search(self, query, button):
        queues["query"].put_nowait(query)

class MyClock(Widget):
    def __init__(self, **kwargs):
        super(type(self),self).__init__(**kwargs)
        Clock.schedule_interval(self.update_my_widget, 1 / 10.)
    
    def update_my_widget(self,delta):
        self.ids.date.text = str(datetime.today().date())
        self.ids.time.text = str(datetime.today().time())[0:8]

class MyLayout(Widget):
    pass

#   def update(self, dt):
#        print(dt)



class MyTask:

    async def my_other_task(self):
        '''This method is also run by the asyncio loop.
        '''
        while queues["query"] is None:
                await asyncio.sleep(1)

        while True:
            query = await queues["query"].get()
            print("Really searching for...", query)
            r = requests.get('https://api.duckduckgo.com', 
                params={'q': query, 'format': 'json'})
            print(r)
            #print(r.text)
            print(r.json()['AbstractText'])
            print(r.json()['AbstractURL'])


class SearchApp(App):
    
    def build(self):
        return MyLayout()

    def app_func(self):
        async def run_wrapper():
            global queues
            queues = {"query":asyncio.Queue(), "response":asyncio.Queue()}
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
