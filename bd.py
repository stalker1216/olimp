import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    port=2023  
)

cursor = connection.cursor()

name_base="program3"
cursor.execute("DROP DATABASE IF EXISTS {0}".format(name_base))
connection.commit()

cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(name_base))

cursor.execute("USE {0}".format(name_base))

users="users"
cursor.execute("""CREATE TABLE IF NOT EXISTS {0} (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(16) NOT NULL,
    name VARCHAR(12) NOT NULL,
    password VARCHAR(12) NOT NULL
)""".format(users))

