import mysql.connector
import asyncio
import json
import time
import random

connection = mysql.connector.connect(
    host='localhost', 
    user='admin',
    password='admin',
    port=4539,
    database="program3"
)

cursor=connection.cursor()

async def new_connect(input_message,output_message):
    #connect,adress=obj.accept()
    data=await input_message.read(1024)
    data=data.decode("utf-8")
    
    command=json.loads(data)
    if command["action"]=="autorization":
        print(command["token"])
        with open("file/token.txt","r") as f:
            all_token=f.readlines()
        if command["token"]+"\n" in all_token:
            print("OK")
        else:
            print("New user")
            command = "INSERT INTO {0} (token, name, password) VALUES (%s, %s, %s)".format("users")
            with open("file/user_number.txt","r") as f:
                user_number=f.read()
            token=user_number
            for i in range(16-len(user_number)):
                token=token+chr(int(str(time.time())[-1::])+random.randint(97,113))
            data2 = (token, "user", "")
            cursor.execute(command, data2)
            #user_id=cursor.lastrowid # отримаэмо id щойноствореного користувача
            with open("file/user_number.txt","w") as f:
                f.write(str(int(user_number)+1))
            with open("file/token.txt","a") as f:
                f.write(token+"\n")
            info={"token":token,"id":int(user_number)}
            info["action"]="init"
            print(json.dumps(info))
            output_message.write(json.dumps(info).encode("utf-8"))
            print("New user1")

async def main():
    server = await asyncio.start_server(new_connect,"192.168.56.1",3945)
    async with server:
        await server.serve_forever()
if __name__=="__main__":
    asyncio.run(main())
