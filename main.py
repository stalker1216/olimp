from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        textinput=TextInput(text='Hello world')

class ProgramApp(App):
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        all_windows.add_widget(Menu())
        return all_windows
if __name__=="__main__":
    ProgramApp().run()