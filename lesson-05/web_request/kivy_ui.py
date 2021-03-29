'''Example shows the recommended way of how to run Kivy with the Python built
in asyncio event loop as just another async coroutine.
'''
import asyncio

from kivy.app import App
from kivy.lang.builder import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        ToggleButton:
            id: btn1
            group: 'a'
            text: 'Sleeping'
            allow_no_selection: False
            on_state: if self.state == 'down': label.status = self.text
        ToggleButton:
            id: btn2
            group: 'a'
            text: 'Swimming'
            allow_no_selection: False
            on_state: if self.state == 'down': label.status = self.text
        ToggleButton:
            id: btn3
            group: 'a'
            text: 'Reading'
            allow_no_selection: False
            state: 'down'
            on_state: if self.state == 'down': root.bump(self.text)
    Label:
        id: label
        status: 'Reading'
        text: 'Beach status is "{}"'.format(self.status)
'''

async def waste_time_freely(kivy_app):
        '''This method is also run by the asyncio loop and periodically prints
        something.
        '''
        while True:
            await asyncio.sleep(2)
            print("Hello there", kivy_app)

class AsyncApp(App):

    other_task = None

    def build(self):
        class MyTextInput(Widget):
    def print_text(self,text):
        print(text)
        return Builder.load_string(kv)

    def app_func(self):
        '''This will run both methods asynchronously and then block until they
        are finished
        '''

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.other_task.cancel()
        
        self.other_task = asyncio.ensure_future(waste_time_freely(self))

        global queue
        queue = asyncio.Queue()

        return asyncio.gather(run_wrapper(), self.other_task)

 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncApp().app_func())
    loop.close()
