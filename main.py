from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
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
Window.size=[w/2.3,h/5*4]
Window.left=w//2-Window.size[0]//2
Window.top=h//2-Window.size[1]//2

all_commands=[]
priority={"init":0,
          "donate":0,
          "update_resource":0}
def start_game():
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            obj.connect(("192.168.56.1",3945))
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
    elif command["action"]=="update_resource":
        heapq.heappush(all_commands,(priority["update_resource"],time.time(),command))
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

class StartMenu(Screen):
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
            print("true")
        except:
            self.Error_log.color=[15,0,0,1]
                       
class Register(Screen):
    name="register"
    def __init__(self, **kw):
        super().__init__(**kw)

class Menu(Screen):
    name="menu"
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

class ProgramApp(App):
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        all_windows.add_widget(StartMenu())
        all_windows.add_widget(Register())
        all_windows.add_widget(Menu())
        return all_windows
if __name__=="__main__":
    ProgramApp().run()