import smtplib
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
server.quit()