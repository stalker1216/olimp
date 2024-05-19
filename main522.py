from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
#from kivy.uix.gridlayout import GridLayout
import socket
import heapq
import pygame
pygame.init()
import json
import threading
import os
import time

path=os.path.abspath('')+'/'

w,h=pygame.display.Info().current_w,pygame.display.Info().current_h
Window.size=[w/3,h/5*4]
Window.left=w//2-Window.size[0]//2
Window.top=h//2.5-Window.size[1]//2

all_commands=[]
priority={"init":0,
          "donate":0,
          "update_resource":0}
def start_game():
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    while True:
        try:
            obj.connect(("192.168.56.1",3945))#miha01lojb@gmail.com
            break
        except:
            pass
    with open(path+"file/userdata.json","r") as f:
        text=f.read()
    #text="token ({0})".format(text)
    obj.sendall(text.encode("utf-8"))
    text=json.loads(text)
    date=obj.recv(1024)
    command=json.loads(date)
    print(json.dumps(command))
    if command["action"]=="init":
        text["token"]=command["token"]
        text["id"]=command["id"]
        heapq.heappush(all_commands,(priority["init"],time.time(),command))
    """elif command["action"]=="update_resource":
        heapq.heappush(all_commands,(priority["update_resource"],time.time(),command))"""
    #all_commands.update(command)
    with open(path+"file/userdata.json", "w") as g:
        g.write(json.dumps(text))
    #print(date.decode("utf-8"))
    obj.close()

server_thread=threading.Thread(target=start_game)

file=open(path+"file/options.json","r")
options=json.loads(file.read())
options["text_size"]=Window.size[0]/13
options["server_run"]=False

class Task(Screen):
    name="task"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="task"))

class Calendar(Screen):
    name="calendar"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="calendar"))

class Command(Screen):
    name="command"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="command"))

class Daybook(Screen):
    name="daybook"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="daybook"))

class Chat(Screen):
    name="chat"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="chat"))

class Menu(Screen):
    name="menu"
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

        panel=BoxLayout(size_hint=[1,0])#test
        box.add_widget(panel)

        self.go_task_button=Button(size_hint=[0.27,1],background_normal=path+"sprites/1.png",background_down=path+"sprites/task_off.jpg",color=[0,0,0,1],on_press=self.go_task)
        panel.add_widget(self.go_task_button)

        go_calendar_button=Button(size_hint=[0.3,1],background_normal=path+"sprites/2.jpg",background_down=path+"sprites/task_off.jpg",color=[0,0,0,1],on_press=self.go_calendar)
        panel.add_widget(go_calendar_button)

        go_command_button=Button(size_hint=[0.3,1],background_normal=path+"sprites/3.png",background_down=path+"sprites/task_off.jpg",color=[0,0,0,1],on_press=self.go_command)
        panel.add_widget(go_command_button)

        go_daybook_button=Button(size_hint=[0.24,1],background_normal=path+"sprites/4.jpg",background_down=path+"sprites/task_off.jpg",color=[0,0,0,1],on_press=self.go_daybook)
        panel.add_widget(go_daybook_button)

        go_chat_button=Button(size_hint=[0.3,1],background_normal=path+"sprites/5.png",background_down=path+"sprites/task_off.jpg",color=[0,0,0,1],on_press=self.go_chat)#добавить спрайт чата
        panel.add_widget(go_chat_button)

    def go_task(self,button):
        self.all_game_screen.current="task"
    def go_calendar(self,button):
        self.all_game_screen.current="calendar"
    def go_command(self,button):
        self.all_game_screen.current="command"
    def go_daybook(self,button):
        self.all_game_screen.current="daybook"
    def go_chat(self,button):
        self.all_game_screen.current="chat"

"""class StartMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.input_login=TextInput(hint_text="Логін",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.8})
        self.add_widget(self.input_login)
        self.input_password=TextInput(hint_text="Пароль",size_hint=[0.4,0.05],pos_hint={"center_x":0.5,"center_y":0.73})
        self.add_widget(self.input_password)
        self.log_in_button=Button(text="Вхід",size_hint=[0.3,0.1],
        pos_hint={"center_x":0.2,"center_y":0.6},
        font_size=options["text_size"], color=[1,1,1],
        background_color=[0,0.8,255],#[50,130,180]
        on_press=self.log_in
        )
        self.add_widget(self.log_in_button)
        self.register_button=Button(text="Реєстрація",size_hint=[0.4,0.1],
        pos_hint={"center_x":0.75,"center_y":0.6},
        font_size=options["text_size"], color=[1,1,1],
        background_color=[0,0.8,255],#[50,130,180]
        on_press=self.register
        )
        self.add_widget(self.register_button)
        self.Error_log=Label(text="Неправильний логін чи пароль",color=[15,0,0,0],pos_hint={"center_x":0.1,'center_y':0.72},halign="right",text_size=[Window.size[0],Window.size[1]//10])
        self.add_widget(self.Error_log)
        
    def log_in(self,button):
        if not options["server_run"]:
            options["server_run"]=True
            server_thread.start()
        self.manager.current="menu"#test
    def register(self,button):#доработать сохранение почти
        if not options["server_run"]:
            options["server_run"]=True
            server_thread.start()

        sender_email='miha00lojb@gmail.com' 
        sender_password='mzok jlmw fhky aqul' 
        recipient_email=self.input_login.text
        subject="Вітаємо з успішною реєстрацією!"
        message="Ви успішно пройшли етап реєстрації"

        msg = MIMEMultipart()
        msg['From']=sender_email
        msg['To']=recipient_email
        msg['Subject']=subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            self.manager.current="register"
        except:
            self.Error_log.color=[15,0,0,1]"""

                       
class Register(Screen):
    name="register"
    def __init__(self, **kw):
        super().__init__(**kw)

class ProgramApp(App):
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        all_windows.add_widget(Menu())
        all_windows.add_widget(Register())
        
        return all_windows
if __name__=="__main__":
    ProgramApp().run()