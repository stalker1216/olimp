from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
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
Window.size = [w / 2.3, h / 5 * 4]
Window.left = w // 2 - Window.size[0] // 2
Window.top = h // 2.5 - Window.size[1] // 2

all_commands = []
priority = {"init": 0,
            "donate": 0,
            "update_resource": 0}

def start_game():
    obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            obj.connect(("192.168.56.1", 3945))  # miha01lojb@gmail.com
            break
        except:
            pass
    with open(path + "file/userdata.json", "r") as f:
        text = f.read()
    obj.sendall(text.encode("utf-8"))
    text = json.loads(text)
    date = obj.recv(1024)
    command = json.loads(date)
    print(json.dumps(command))
    if command["action"] == "init":
        text["token"] = command["token"]
        text["id"] = command["id"]
        heapq.heappush(all_commands, (priority["init"], time.time(), command))
    with open(path + "file/userdata.json", "w") as g:
        g.write(json.dumps(text))
    obj.close()

server_thread = threading.Thread(target=start_game)

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

class Command(Screen):
    name = "command"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="command"))

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

class Menu(Screen):
    name = "menu"
    def __init__(self, **kw):
        super().__init__(**kw)

        box = BoxLayout(orientation="vertical")
        self.add_widget(box)

        self.all_game_screen = ScreenManager(transition=SwapTransition(), size_hint=[1, 0.9])
        self.all_game_screen.add_widget(Task())
        self.all_game_screen.add_widget(Calendar())
        self.all_game_screen.add_widget(Command())
        self.all_game_screen.add_widget(Daybook())
        self.all_game_screen.add_widget(Chat())
        box.add_widget(self.all_game_screen)

        panel = BoxLayout(size_hint=[1, 0.1])
        box.add_widget(panel)

        self.go_task_button = Button(size_hint=[1, 1], background_normal=path + "sprites/task_off.jpg",
                                     background_down=path + "sprites/task_off.jpg", color=[0, 0, 0, 1], on_press=self.go_task)
        panel.add_widget(self.go_task_button)

        go_calendar_button = Button(size_hint=[1, 1], background_normal=path + "sprites/calendar_off.jpg",background_down=path + "sprites/task_off.jpg", color=[0, 0, 0, 1], on_press=self.go_calendar)
        panel.add_widget(go_calendar_button)

        go_command_button = Button(size_hint=[1, 1], background_normal=path + "sprites/command_off.jpg",
                                   background_down=path + "sprites/task_off.jpg", color=[0, 0, 0, 1], on_press=self.go_command)
        panel.add_widget(go_command_button)

        go_daybook_button = Button(size_hint=[1, 1], background_normal=path + "sprites/daybook_off.jpg",
                                   background_down=path + "sprites/task_off.jpg", color=[0, 0, 0, 1], on_press=self.go_daybook)
        panel.add_widget(go_daybook_button)

        go_chat_button = Button(size_hint=[1, 1], background_normal=path + "sprites/daybook_off.jpg",
                                background_down=path + "sprites/task_off.jpg", color=[0, 0, 0, 1], on_press=self.go_chat)
        panel.add_widget(go_chat_button)

    def go_task(self, button):
        self.all_game_screen.current = "task"
    def go_calendar(self, button):
        self.all_game_screen.current = "calendar"
    def go_command(self, button):
        self.all_game_screen.current = "command"
    def go_daybook(self, button):
        self.all_game_screen.current = "daybook"
    def go_chat(self, button):
        self.all_game_screen.current = "chat"

class Register(Screen):
    name = "register"
    def __init__(self, **kw):
        super().__init__(**kw)

class ProgramApp(App):
    def build(self):
        all_windows = ScreenManager(transition=WipeTransition())
        all_windows.add_widget(Menu())
        all_windows.add_widget(Register())
        
        return all_windows

if __name__ == "__main__":
    ProgramApp().run()