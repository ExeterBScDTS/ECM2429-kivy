#
#
# Michael Saunby, March 2021

delay_test_seconds = 0

import requests

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

