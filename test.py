"""import smtplib
from email.mime.text import MIMEText

# Настройка SMTP сервера и отправка письма
server = smtplib.SMTP('smtp.example.com', 587)
server.starttls()
server.login("miha00lojb@gmail.com", "micha121nicha")

msg = MIMEText("Текст письма")
msg['Subject'] = "Тема письма"
msg['From'] = "miha00lojb@gmail.com"
msg['To'] = "miha01lojb@gmail.com"

server.sendmail("miha00lojb@gmail.com", "miha01lojb@gmail.com", msg.as_string())
server.quit()"""

"""import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class EmailValidatorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.email_input = TextInput(hint_text='Введите email')
        layout.add_widget(self.email_input)
        
        validate_button = Button(text='Проверить Email')
        validate_button.bind(on_press=self.validate_email)
        layout.add_widget(validate_button)
        
        self.result_label = Label(text='')
        layout.add_widget(self.result_label)
        
        return layout
    
    def validate_email(self, instance):
        email = self.email_input.text
        if re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            self.result_label.text = "Email правильный"
        else:
            self.result_label.text = "Email неправильный"

if __name__ == '__main__':
    EmailValidatorApp().run()"""

"""import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class EmailValidator(App):
    def build(self):
        self.email_input = TextInput(hint_text='Enter your email')
        self.result_label = Label(text='')

        validate_button = Button(text='Validate')
        validate_button.bind(on_press=self.validate_email)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.email_input)
        layout.add_widget(validate_button)
        layout.add_widget(self.result_label)

        return layout

    def validate_email(self, instance):
        email = self.email_input.text
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.result_label.text = 'Email is valid.'
        else:
            self.result_label.text = 'Invalid email format.'

if __name__ == '__main__':
    EmailValidator().run()"""


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.app import App



class EmailSender(App):
    def build(self):
        """self.email_input = TextInput(hint_text='Recipient Email')
        self.subject_input = TextInput(hint_text='Subject')
        self.message_input = TextInput(hint_text='Message', multiline=True)"""

    def send_email(self, instance):
        sender_email = 'miha00lojb@gmail.com' 
        sender_password = 'mzok jlmw fhky aqul'  
        recipient_email = self.email_input.text
        subject = self.subject_input.text
        message = self.message_input.text

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    EmailSender().run()