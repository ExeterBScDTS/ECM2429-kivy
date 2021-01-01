#
from kivy.app import App
from kivy.uix.widget import Widget

class Example(Widget):

   def update(self, dt):
        print(dt)

class EffectApp(App):
    
    def build(self):
        example = Example()
        return example

EffectApp().run()
