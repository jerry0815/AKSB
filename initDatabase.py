from connect import connection
name_list = ['Wade', 'Dave', 'Seth', 'Ivan', 'Riley', 'Gilbert', 'Jorge', 'Dan', 'Brian', 'Roberto', 'Ramon', 'Miles', 'Liam', 'Nathaniel', 'Ethan', 'Lewis', 'Milton', 'Claude', 'Joshua', 'Glen', 'Harvey', 'Blake', 'Antonio', 'Connor', 'Julian', 'Aidan', 'Harold', 'Conner', 'Peter', 'Hunter', 'Eli', 'Alberto', 'Carlos', 'Shane', 'Aaron', 'Marlin', 'Paul', 'Ricardo', 'Hector', 'Alexis', 'Adrian', 'Kingston', 'Douglas', 'Gerald', 'Joey', 'Johnny', 'Charlie', 'Scott', 'Martin', 'Tristin', 'Troy', 'Tommy', 'Rick', 'Victor', 'Jessie', 'Neil', 'Ted', 'Nick', 'Wiley', 'Morris', 'Clark', 'Stuart', 'Orlando', 'Keith', 'Marion', 'Marshall', 'Noel', 'Everett', 'Romeo', 'Sebastian', 'Stefan', 'Robin', 'Clarence', 'Sandy', 'Ernest', 'Samuel', 'Benjamin', 'Luka', 'Fred', 'Albert', 'Greyson', 'Terry', 'Cedric', 'Joe', 'Paul', 'George', 'Bruce', 'Christopher', 'Mark', 'Ron', 'Craig', 'Philip', 'Jimmy', 'Arthur', 'Jaime', 'Perry', 'Harold', 'Jerry', 'Shawn', 'Walter']
cursor = connection.cursor()
cursor.execute(
'''CREATE TABLE users
(userID INTEGER  PRIMARY KEY AUTOINCREMENT,
userName TEXT NOT NULL,
password TEXT NOT NULL,
email TEXT NOT NULL,
identity INT NOT NULL);''')

cursor.execute(
'''CREATE TABLE record
(recordID INTEGER  PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
participant LONGTEXT,
startDate DATE NOT NULL,
startSection INT NOT NULL,
endDate DATE NOT NULL,
endSection INT NOT NULL,
CR_ID INT NOT NULL,
B_ID INT NOT NULL,
type INT);''')

cursor.execute(
'''CREATE TABLE classroom
(CR_ID INTEGER  PRIMARY KEY AUTOINCREMENT,
building TEXT NOT NULL,
roomname TEXT NOT NULL,
capacity INT NOT NULL);''')
sql = "INSERT INTO 'users' ('userName', 'password' , 'email' , 'identity' ) VALUES (?,?,?,?)"

users = [["Jerry" ,  "123456789" , "jerrylulala@gmail.com", 0 ],
        ['Alex',"123456789" , "Alex@gmail.com", 0 ],
        ['samshih', "123456789" , "samshih@gmail.com", 0 ],
        ['johnnysu', "123456789" , "johnnysu@gmail.com", 0 ],
        ['sb8787', "123456789" , "sb8787@gmail.com", 0 ]]
for i in range(15):
    users.append([name_list[i],"123456789", name_list[i]+'@gmail.com',0])
cursor.executemany(sql,users)

sql = "INSERT INTO `classroom` (`building`, `roomname` , `capacity`) VALUES (?, ? , ?)"
record = []
build = ["EA" , "EB" , "EC" , "ED" , "EE", "SA", "SB", "SC", "AC", "A", "AB", "HA", "EO"]
for b in build:
    for story in range(101,121):
            name = b + str(story)
            l = [b , name , "50"]
            record.append(l)
cursor.executemany(sql,record)

connection.commit()