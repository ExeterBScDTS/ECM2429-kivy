#
#
# Michael Saunby, March 2021

# Try changing this value and see how the program
# behaves.  Values of 2, 5, and 10 would be good experiments.
delay_test_seconds = 0

import requests

class SearchTask:
    def __init__(self):
        self.response = {"query":"","text":"","url":""}

    def search(self,query):
        '''
        Make a GET call to 'https://api.duckduckgo.com'
        and save the query and response.
        This method call is synchronous and returns 
        when the web app call completes -
        success, failure, or timeout.
        '''
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

