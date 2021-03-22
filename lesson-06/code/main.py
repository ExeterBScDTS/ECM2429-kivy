#
# Kivy example calling a web API using requests.
# Demonstrates how the UI will freeze while fetching data.
# Set delay_test_seconds to a small integer value (say 5)
# To see the effect
#
# Michael Saunby, March 2021

delay_test_seconds = 0

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

from datetime import datetime
import requests



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
        search_task.search(query)

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

    def search(self,query):
        r = requests.get('https://api.duckduckgo.com', 
            params={'q': query, 'format': 'json'})
        if r:
            abstract = r.json()['AbstractText']
            self.response["query"] = query
            self.response["text"] = abstract
            url = r.json()['AbstractURL']
            self.response["url"] = url
        
        if delay_test_seconds:
            from time import sleep
            sleep(delay_test_seconds)

    def get_response(self):
        return self.response

class SearchApp(App):
    '''
    A Kivy UI for a simple web search app.
    See search.kv for the widget layout.
    '''    
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    search_task = SearchTask()
    SearchApp().run()