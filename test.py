from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
import socket
import heapq
import pygame
pygame.init()
import json
import threading
import os
import time

path = os.path.abspath('') + '/'

w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
Window.size = [w / 3, h / 5 * 4]
Window.left = w // 2 - Window.size[0] // 2
Window.top = h // 2.5 - Window.size[1] // 2

all_commands = []
priority = {"init": 0, "donate": 0, "update_resource": 0}

file = open(path + "file/options.json", "r")
options = json.loads(file.read())
options["text_size"] = Window.size[0] / 13
options["server_run"] = False

class Task(Screen):
    name = "task"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="task"))

class Calendar(Screen):
    name = "calendar"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="calendar"))

class Daybook(Screen):
    name = "daybook"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="daybook"))

class Chat(Screen):
    name = "chat"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="chat"))

class Register(Screen):
    name = "register"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.lable_register = Label(font_size=30, text="Вкажіть дані для входу", size_hint=[2,1], pos_hint={"center_x":0.5, "center_y":0.94}, color=[255,255,255,1])
        self.add_widget(self.lable_register)
        self.lable_login = Label(font_size=20, text="Вкажіть ім`я яке буде відображатися для інших користувачів", size_hint=[2,1], pos_hint={"center_x":0.5, "center_y":0.8}, color=[255,255,255,1])
        self.add_widget(self.lable_login)
        self.input_login = TextInput(hint_text="Логін", size_hint=[0.9, 0.05], pos_hint={"center_x":0.5, "center_y":0.75})
        self.add_widget(self.input_login)
        self.lable_password = Label(font_size=20, text="Придумайте власний пароль", size_hint=[2,1], pos_hint={"center_x":0.27, "center_y":0.65}, color=[255,255,255,1])
        self.add_widget(self.lable_password)
        self.input_password = TextInput(hint_text="Пароль", size_hint=[0.9, 0.05], pos_hint={"center_x":0.5, "center_y":0.6})
        self.add_widget(self.input_password)
        self.log_in_button = Button(text="Вхід в систему", size_hint=[0.4, 0.1], pos_hint={"center_x":0.5, "center_y":0.45}, font_size=30, color=[1,1,1], background_color=[0,0.8,255], on_press=self.log_in)
        self.add_widget(self.log_in_button)
        self.error_input = Label(font_size=20, text="Неправильний логін чи пароль", size_hint=[2,1], pos_hint={"center_x":0.5, "center_y":0.55}, color="#F52626")

    def log_in(self, button):
        global input_login_text, input_password_text
        input_login_text = self.input_login.text
        input_password_text = self.input_password.text
        test_log = {"name": input_login_text, "password": input_password_text}
        if not options["server_run"]:
            options["server_run"] = True
            server_thread.start()
        with open(path + "file/userdata.json", "r") as f:
            text = f.read()
        text = json.loads(text)
        if len(input_login_text) <= 3 and len(input_password_text) <= 3:
            try:
                self.add_widget(self.error_input)
            except:
                pass
        elif len(input_login_text) >= 12 and len(input_password_text) <= 12:
            try:
                self.add_widget(self.error_input)
            except:
                pass
        elif not text["name"] == test_log["name"]:
            try:
                self.add_widget(self.error_input)
            except:
                pass
        elif not text["password"] == test_log["password"]:
            try:
                self.add_widget(self.error_input)
            except:
                pass
        else:
            self.manager.current = "menu"

class Command(Screen):
    name = "command"
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical")
        self.add_widget(box)
        panel = BoxLayout(size_hint=[0.25,1])
        box.add_widget(panel)

        resource = GridLayout(size_hint=[4,1], rows=3)

        self.create_button = Button(size_hint=[1,0.15], color=[1,1,1,1], text='')  # Create button
        resource.add_widget(self.create_button)

        panel.add_widget(resource)

class BottomPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(BottomPanel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.size_hint_y = None
        self.height = Window.height * 0.3

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        row = BoxLayout(orientation='horizontal', spacing=10)
        img_button = Button(background_normal='', size_hint_x=0.1)
        text_button = Button(text='Створити команду', background_color=[255,255,255,1], color=[0,0,0,1], size_hint_x=0.8, on_press=self.open_popup)
        row.add_widget(img_button)
        row.add_widget(text_button)
        self.add_widget(row)

        row1 = BoxLayout(orientation='horizontal', spacing=10)
        img_button1 = Button(background_normal='', size_hint_x=0.1)
        text_button1 = Button(text='a', background_color=[255,255,255,1], color=[0,0,0,1], size_hint_x=0.8)
        row1.add_widget(img_button1)
        row1.add_widget(text_button1)
        self.add_widget(row1)

        row2 = BoxLayout(orientation='horizontal', spacing=10)
        img_button2 = Button(background_normal='', size_hint_x=0.1)
        text_button2 = Button(text='a', background_color=[255,255,255,1], color=[0,0,0,1], size_hint_x=0.8)
        row2.add_widget(img_button2)
        row2.add_widget(text_button2)
        self.add_widget(row2)
        
    def open_popup(self, button):
        popup_content = BoxLayout(orientation='vertical')
        self.lable_register = Label(font_size=15, text="Ім`я команди", size_hint=[1,0.01], pos_hint={"center_x":0.1, "center_y":1}, color=[1,1,1,1])
        self.input_name = TextInput(hint_text="Допустимі букви, цифри і пробіли", size_hint=[1,0.05])
        self.create_button_window = Button(size_hint=[1,0.15], background_color=[255,255,255,1], color=[0,0,0,1], text="Створити", font_size=options['text_size']*0.3)
        self.create_button_window.bind(on_press=self.set_button_text)  # Bind button press to set_button_text
        popup_content.add_widget(self.lable_register)
        popup_content.add_widget(self.input_name)
        popup_content.add_widget(self.create_button_window)
        self.popup = Popup(title="Створення команди", content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def set_button_text(self, instance):
        self.parent.children[-1].children[0].children[-1].text = self.input_name.text
        self.popup.dismiss()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class MainApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Register(name='register'))
        sm.add_widget(Task(name='task'))
        sm.add_widget(Calendar(name='calendar'))
        sm.add_widget(Daybook(name='daybook'))
        sm.add_widget(Chat(name='chat'))
        sm.add_widget(Command(name='command'))

        root = FloatLayout()
        root.add_widget(sm)

        panel = BottomPanel(size_hint_y=None, height='48dp')
        root.add_widget(panel)

        return root

server_thread = threading.Thread()
if __name__ == '__main__':
    MainApp().run()
