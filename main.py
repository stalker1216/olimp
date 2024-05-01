from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import pygame
pygame.init()
import json
import os

path=os.path.abspath('')+'/'

w,h=pygame.display.Info().current_w,pygame.display.Info().current_h
Window.size=[w/2.3,h/5*4]
Window.left=w//2-Window.size[0]//2
Window.top=h//2-Window.size[1]//2

file=open(path+"file/options.json","r")
options=json.loads(file.read())
options["text_size"]=Window.size[0]/13

class StartMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        input_login=TextInput(hint_text="Логін",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.8})
        self.add_widget(input_login)
        input_password=TextInput(hint_text="Пароль",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.73})
        self.add_widget(input_password)
        self.play=Button(text="Play",size_hint=[0.3,0.05],
        pos_hint={"center_x":0.5,"center_y":0.65},
        font_size=options["text_size"], color=[0,0,0.2],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.log_in
        )
    def log_in(button):
        pass

class Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        input_login=TextInput(hint_text="Логін",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.8})
        self.add_widget(input_login)
        input_password=TextInput(hint_text="Пароль",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.73})
        self.add_widget(input_password)
        self.log_in_button=Button(text="Вхід",size_hint=[0.3,0.1],
        pos_hint={"center_x":0.2,"center_y":0.6},
        font_size=options["text_size"], color=[1,1,1],
        background_color=[0,0.8,255],#[50,130,180]
        on_press=self.log_in
        )
        self.add_widget(self.log_in_button)
    def log_in(self,button):
        pass

class ProgramApp(App):
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        all_windows.add_widget(Menu())
        return all_windows
if __name__=="__main__":
    ProgramApp().run()