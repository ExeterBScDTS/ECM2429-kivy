#
from kivy.app import App
from kivy.uix.widget import Widget

class MyTextInput(Widget):
    def print_text(self,text):
        print(text)

class Example(Widget):

   def update(self, dt):
        print(dt)

class DemoLayoutApp(App):
    
    def build(self):
        example = Example()
        return example

DemoLayoutApp().run()
