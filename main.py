from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy import platform
import random
import socket
import heapq
import pygame
pygame.init()
import json
import threading
import os
import time

path=''

if platform == 'win':  
    local_path = os.path.join(os.environ['LOCALAPPDATA'],'civa')

w,h=pygame.display.Info().current_w,pygame.display.Info().current_h
Window.size=[w/3,h/5*4]
Window.left=w//2-Window.size[0]//2
Window.top=h//2.5-Window.size[1]//2

if not os.path.exists(local_path): 
    os.makedirs(local_path) 
if not os.path.exists(os.path.join(local_path,"options.json")): 
    options={"font": "font/7fonts_Knight2.ttf", "text_size": 45, "server_run":False} 
    options["text_size"]=int((max(w,h)//40)*1.2)
    open(os.path.join(local_path,"options.json"),"w").write(json.dumps(options))
    print(1)
else: 
    options=json.loads(open(os.path.join(local_path,"options.json"),"r").read()) 
if not os.path.exists(os.path.join(local_path,"userdata.json")): 
    userdata={"action": "autorization", "token": "", "id": 0, "name": "", "password": "", "invite_token": "", "command_token": "", "command_name": ""}
    open(os.path.join(local_path,"userdata.json"),"w").write(json.dumps(userdata))
    print(2)
else: 
    userdata=json.loads(open(os.path.join(local_path,"userdata.json"),"r").read()) 
    
all_commands=[]
priority={"init":0,
          "donate":0,
          "update_resource":0}


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

class Register(Screen):
    name="register"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.lable_register=Label(font_size=30,text="Вкажіть дані для входу",size_hint=[2,1],pos_hint={"center_x":0.5,"center_y":0.94},color=[255,255,255,1])
        self.add_widget(self.lable_register)
        self.lable_login=Label(font_size=20,text="Вкажіть ім`я яке буде відображатися для інших користувачів",size_hint=[2,1],pos_hint={"center_x":0.5,"center_y":0.8},color=[255,255,255,1])
        self.add_widget(self.lable_login)
        self.input_login=TextInput(hint_text="Логін",size_hint=[0.9,0.05],pos_hint={"center_x":0.5,"center_y":0.75})
        self.add_widget(self.input_login)
        self.lable_password=Label(font_size=20,text="Придумайте власний пароль",size_hint=[2,1],pos_hint={"center_x":0.27,"center_y":0.65},color=[255,255,255,1])
        self.add_widget(self.lable_password)
        self.input_password=TextInput(hint_text="Пароль",size_hint=[0.9,0.05],pos_hint={"center_x":0.5,"center_y":0.6})
        self.add_widget(self.input_password)
        self.log_in_button=Button(text="Вхід в систему",size_hint=[0.4,0.1],
        pos_hint={"center_x":0.5,"center_y":0.45},
        font_size=30, color=[1,1,1],
        background_color=[0,0.8,255],#[50,130,180]
        on_press=self.log_in
        )
        self.add_widget(self.log_in_button)
        self.error_input=Label(font_size=20,text="Неправильний логін чи пароль",size_hint=[2,1],pos_hint={"center_x":0.5,"center_y":0.55},color="#F52626")
        
    def log_in(self,button):
        global input_login_text, input_password_text
        input_login_text=self.input_login.text
        input_password_text=self.input_password.text
        test_log={"name":input_login_text,"password":input_password_text}
        if not options["server_run"]:
            options["server_run"]=True
            server_thread.start()
        with open(os.path.join(local_path,"userdata.json"),"r") as f:
            text=f.read()
        text=json.loads(text)
        if len(input_login_text)<=3 and len(input_password_text)<=3:
            try:
                self.add_widget(self.error_input)
            except:
                pass
        elif len(input_login_text)>=12 and len(input_password_text)>=12:###########################################><
            try:
                self.add_widget(self.error_input)
            except:
                pass
        
        else:
            self.manager.current="menu"#test
"""elif not text["name"]==test_log["name"]:######################################################################################## работає з 2 раза
            try:
                self.add_widget(self.error_input)
            except:
                pass
        elif not text["password"]==test_log["password"]:
            try:
                self.add_widget(self.error_input)
            except:
                pass"""
class Command(Screen):
    name="command"
    def __init__(self, **kw):
        super().__init__(**kw)

        box=BoxLayout(orientation="vertical")
        self.add_widget(box)
        panel=BoxLayout(size_hint=[0.25,1])
        box.add_widget(panel)

        self.resource=GridLayout(size_hint=[4,1],cols=1)

        """self.create_button=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[255,255,255,1],text='',on_press=self.create_test)
        self.resource.add_widget(self.create_button)"""

        panel.add_widget(self.resource)

        Clock.schedule_interval(self.update,1/2)
    
    def update(self,button):
        try:
            #self.create_button.text=global_input_name
            self.create_button=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[255,255,255,1],text=global_input_name[-1],on_press=self.actions_create_button)
            self.resource.add_widget(self.create_button)
            global_input_name[-1]=None
        except:
            pass
        

    #def create_test(self,button):
        
        #global_input_name=""

    def actions_create_button(self,button):
        global command_token
        self.manager.current="new_command"
        """for i in range(len(global_input_name)):
            print(1)
            screen = NewCommand(name=f'Screen {i}')"""
        command_token=""
        for i in range(16):
            command_token+=chr(int(str(time.time())[-1::])+random.randint(97,113))
    
class NewCommand(Screen):
    name="new_command"
    def __init__(self, **kw):
        super().__init__(**kw)
        box=BoxLayout(orientation="vertical")
        self.add_widget(box)
        """panel=BoxLayout(size_hint=[0.25,1])
        box.add_widget(panel)"""

        self.input_invite_token=TextInput(hint_text="token",size_hint=[1,0.05])
        box.add_widget(self.input_invite_token)


        self.enter_token_button=Button(size_hint=[0.3,1],background_color=[255,255,255,1],color=[255,255,255,1],text='add',on_press=self.save_token)
        box.add_widget(self.enter_token_button)

        #self.exit_command_button=Button(size_hint=[0.3,1],background_color=[255,255,255,1],color=[255,255,255,1],text='exit',on_press=self.exit_command)
        #panel.add_widget(self.exit_command_button)

        

        """self.settings_command_button=Button(size_hint=[0.3,1],background_color=[255,255,255,1],color=[255,255,255,1],text='settings',on_press=self.settings_command)
        panel.add_widget(self.settings_command_button)"""


    def save_token(self,button):
        with open(path+"file/userdata.json","r") as f:
            text=f.read()#ijahniahibhauwbu
        text=json.loads(text)
        text["invite_token"]=self.input_invite_token.text
        text["command_token"]=command_token
        text["command_name"]=global_save_name[-1]
        with open(path+"file/userdata.json", "w") as g:
            g.write(json.dumps(text))
        self.input_invite_token.text=""
        

    def settings_command(self,button):
        pass

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

        row=BoxLayout(orientation='horizontal', spacing=10)
        img_button=Button(background_normal='', size_hint_x=0.1)
        text_button=Button(text='Створити команду',background_color=[255,255,255,1],color=[0,0,0,1], size_hint_x=0.8,on_press=self.open_popup)
        row.add_widget(img_button)
        row.add_widget(text_button)
        self.add_widget(row)

        row1=BoxLayout(orientation='horizontal', spacing=10)
        img_button1=Button(background_normal='', size_hint_x=0.1)
        text_button1=Button(text='a',background_color=[255,255,255,1],color=[0,0,0,1], size_hint_x=0.8)
        row1.add_widget(img_button1)
        row1.add_widget(text_button1)
        self.add_widget(row1)

        row2=BoxLayout(orientation='horizontal', spacing=10)
        img_button2=Button(background_normal='', size_hint_x=0.1)
        text_button2=Button(text='a',background_color=[255,255,255,1],color=[0,0,0,1], size_hint_x=0.8)
        row2.add_widget(img_button2)
        row2.add_widget(text_button2)
        self.add_widget(row2)

    def open_popup(self, button):
        popup_content = BoxLayout(orientation='vertical')
        self.lable_register=Label(font_size=15,text="Ім`я команди",size_hint=[1,0.01],pos_hint={"center_x":0.1,"center_y":1},color=[1,1,1,1])
        self.input_name=TextInput(hint_text="Допустимі букви, цифри і пробіли",size_hint=[1,0.05])
        self.create_button_popup=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Створити",font_size=options['text_size']*0.3,on_press=self.save_text)
        #self.create_button_popup.bind(on_release=self.global_create_test)
        popup_content.add_widget(self.lable_register)
        popup_content.add_widget(self.input_name)
        popup_content.add_widget(self.create_button_popup)
        popup = Popup(title='Створити команду', content=popup_content, size_hint=(None, None), size=(500, 600))#655, 960
        popup.open()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def save_text(self, button):
        global global_input_name,global_save_name
        global_input_name=[]
        global_input_name.append(self.input_name.text)
        global_save_name=[]
        global_save_name.append(self.input_name.text)
        self.input_name.text=""

class Menu(Screen):
    name="menu"
    def __init__(self, **kw):
        super().__init__(**kw)
        

        box=BoxLayout(orientation="vertical")
        self.add_widget(box)

        up_panel=BoxLayout(orientation="vertical",size_hint=[1,0.1])
        box.add_widget(up_panel)
        
        screen_button=GridLayout(size_hint=[4,1],cols=7)

        self.open_bottompanel=Button(size_hint=[0.1,0.1],background_color=[255,255,255,1],color=[0,0,0,1],text="відкрити",on_press=self.toggle_panel)
        up_panel.add_widget(self.open_bottompanel)

        self.all_game_screen=ScreenManager(transition=SwapTransition(),size_hint=[4,1])
        self.all_game_screen.add_widget(Task())
        self.all_game_screen.add_widget(Calendar())
        self.all_game_screen.add_widget(Command())
        self.all_game_screen.add_widget(Daybook())
        self.all_game_screen.add_widget(Chat())
        self.all_game_screen.add_widget(NewCommand())
        box.add_widget(self.all_game_screen)

        panel=BoxLayout(size_hint=[1,0.2])
        box.add_widget(panel)

        task_box=BoxLayout(orientation="vertical")
        self.go_task_button=Button(size_hint=[1,1],background_normal=path+"sprites/1.png",background_down=path+"sprites/1.png",color=[0,0,0,1],on_press=self.go_task)
        task_box.add_widget(self.go_task_button)
        self.people_text=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Завдання",bold=True,font_size=options['text_size']*0.3)
        task_box.add_widget(self.people_text)
        screen_button.add_widget(task_box)

        calendar_box=BoxLayout(orientation="vertical")
        self.go_calendar_button=Button(size_hint=[1,1],background_normal=path+"sprites/2.jpg",background_down=path+"sprites/2.jpg",color=[0,0,0,1],on_press=self.go_calendar)
        calendar_box.add_widget(self.go_calendar_button)
        self.people_text=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Календар",bold=True,font_size=options['text_size']*0.3)
        calendar_box.add_widget(self.people_text)
        screen_button.add_widget(calendar_box)

        command_box=BoxLayout(orientation="vertical")
        self.go_command_button=Button(size_hint=[1,1],background_normal=path+"sprites/3.png",background_down=path+"sprites/3.png",color=[0,0,0,1],on_press=self.go_command)
        command_box.add_widget(self.go_command_button)
        self.people_text=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Команди",bold=True,font_size=options['text_size']*0.3)
        #self.go_command_button.bind(on_release=self.toggle_panel)
        command_box.add_widget(self.people_text)
        screen_button.add_widget(command_box)

        daybook_box=BoxLayout(orientation="vertical")
        self.go_daybook_button=Button(size_hint=[1,1],background_normal=path+"sprites/4.jpg",background_down=path+"sprites/4.jpg",color=[0,0,0,1],on_press=self.go_daybook)
        daybook_box.add_widget(self.go_daybook_button)
        self.people_text=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Успішність",bold=True,font_size=options['text_size']*0.3)
        daybook_box.add_widget(self.people_text)
        screen_button.add_widget(daybook_box)

        chat_box=BoxLayout(orientation="vertical")
        self.go_chat_button=Button(size_hint=[1,1],background_normal=path+"sprites/5.png",background_down=path+"sprites/5.png",color=[0,0,0,1],on_press=self.go_chat)
        chat_box.add_widget(self.go_chat_button)
        self.people_text=Button(size_hint=[1,0.15],background_color=[255,255,255,1],color=[0,0,0,1],text="Чат",bold=True,font_size=options['text_size']*0.3)
        chat_box.add_widget(self.people_text)
        screen_button.add_widget(chat_box)

        panel.add_widget(screen_button)

        self.layout=FloatLayout()
        self.add_widget(self.layout)

        self.bottom_panel=BottomPanel(size_hint=(1, 0.3), pos_hint={'x': 0, 'y': -0.3})
        self.layout.add_widget(self.bottom_panel)

        self.overlay_button = Button(size_hint=(1, 0.8),pos_hint={"center_x":0.5,"center_y":0.6}, background_color=(0, 0, 0, 0))
        self.overlay_button.bind(on_release=self.toggle_panel)
        self.overlay_button.opacity = 0
     
        

    def toggle_panel(self, button):
        try:
            self.layout.add_widget(self.overlay_button)
        except:
            pass
        if self.bottom_panel.pos_hint['y'] == -0.3:
            anim = Animation(pos_hint={'x': 0, 'y': 0}, duration=0.3)
            self.overlay_button.opacity = 0.5  
        else:
            anim = Animation(pos_hint={'x': 0, 'y': -0.3}, duration=0.3)
            self.overlay_button.opacity = 0 
            self.layout.remove_widget(self.overlay_button)
        anim.start(self.bottom_panel)

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
                       
class ProgramApp(App):
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        """with open(path+"file/userdata.json","r") as f:
            text=f.read()
        text=json.loads(text)
        if text["action"]=="autorization":
            text["action"]="game"""
        all_windows.add_widget(Register())
        all_windows.add_widget(Menu())
     
        return all_windows

def start_game(): 
    global obj
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    while True:
        try:
            obj.connect(("134.249.176.108",2024))
            break
        except:
            pass
    with open(os.path.join(local_path,"userdata.json"),"r") as f:
        text=f.read()
    #text="token ({0})".format(text)
    obj.sendall(text.encode("utf-8"))
    text=json.loads(text)
    date=obj.recv(1024)
    command=json.loads(date)
    if command["action"]=="init":
        #text["action"]="game"
        text["token"]=command["token"]
        text["id"]=command["id"]
        text["name"]=input_login_text
        text["password"]=input_password_text
        heapq.heappush(all_commands,(priority["init"],time.time(),command))
    """elif command["action"]=="update_resource":
        heapq.heappush(all_commands,(priority["update_resource"],time.time(),command))"""
    #all_commands.update(command)
    with open(os.path.join(local_path,"userdata.json"),"w") as g:
        g.write(json.dumps(text))
    #print(date.decode("utf-8"))
    obj.close()

server_thread=threading.Thread(target=start_game)

"""if not options["server_run"]:#############################test
    options["server_run"]=True
    server_thread.start()"""

if __name__=="__main__":
    ProgramApp().run()
