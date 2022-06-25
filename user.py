#from os import O_RSYNC
import pymysql
from connect import connection

def insertUser(userName = "jerry", password = "123456798", email = "jerry@gmail.com", identity = '0'):
    """
    insert a user account in database
    parameter:
    str: userName ,
    str: passward,
    str: email,

    """

    sql = "INSERT INTO users (userName, password , email , identity ) VALUES (%s,%s,%s,%s)"
    cursor = connection.cursor()
    cursor.execute(sql,(userName , password , email,identity))
    connection.commit()

def isValidMail(email):
    after = email.split('@')[1]
    if after == 'gmail.com' or after == 'gapps.ntust.edu.tw':
        return True
    else:
        return False

def register(data):
    """
    register a account
    """
    email = data['email'] + "@gmail.com"
    if not isValidMail(email):
        return False
    sql = "select * from  users where userName=%s"
    cursor = connection.cursor()
    cursor.execute(sql,(data['userName'],))
    connection.commit()
    result = cursor.fetchone()
    if result != None:
        return False
    insertUser(userName = data['userName'],  password = data['password'], email = email, identity = '0' )
    return True

#login and return user information. return status,result
#status:
# 0:success 1:wrong email 2:wrong passward
def validateLogin(email , password):
    if email == "" or email == None:
        return (1 , None)
    sql = "SELECT userName , password FROM users WHERE email = %s"
    cursor = connection.cursor()
    cursor.execute(sql,(email,))
    connection.commit()
    result = cursor.fetchone()
    #1 : wrong email
    if result == None:
        return (1 , None)
    print(result)
    print(password)
    #2 : wrong passward
    if result["password"] != password:
        return (2,None)
    else:
        return (0,result['userName'])

#for cookie
def loginCheck(email : str ,password : str):
    if email == "" or email == None:
        return (False,None)
    sql = "SELECT password , identity FROM users WHERE email = %s"
    cursor = connection.cursor()
    cursor.execute(sql,(email,))
    connection.commit()
    result = cursor.fetchone()
    #wrong email
    if result == None:
        return (False,None)
    #wrong passward
    if result["password"] != password:
        return (False,None)
    else:
        if result["identity"] == 0:
            admin = 'normal'
        else:
            admin = 'admin'
        return (True,admin)


def deleteAccount(userID):
    """
    remove an account by userID
    """
    sql = "DELETE FROM users WHERE userID = %s"
    cursor = connection.cursor()
    cursor.execute(sql,(userID,))
    connection.commit()
    return True


def getAllUserName():
    """
    get all users' name
    """
    sql = "SELECT userName FROM users"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

    for i in range(len(result)):
        result[i] = result[i]['userName']
    return result

#display all users
def showUsers():
    sql = "SELECT * FROM users"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    print(result)
    return result

# return all information about users ["userID","userName", "password" , "email" , "identity" ]
def getUser(userName):
    sql = "SELECT * FROM users WHERE userName=%s"
    cursor = connection.cursor()
    cursor.execute(sql,(userName,))
    connection.commit()
    result = cursor.fetchone()
    if result == None:
        return (False,None)
    result = dict(result)
    return (True , result)

def getUserMail(userName):
    """
    get user's mail by userName
    """
    if userName == None or len(userName) == 0:
        return []
    sql = "SELECT email FROM users WHERE userName IN ({seq})".format(seq=','.join(['%s']*len(userName)))
    print(sql)
    print(userName)
    cursor = connection.cursor()
    cursor.execute(sql,(userName,))
    connection.commit()
    results = cursor.fetchall()
    if results == None:
        return []
    email_list = []
    for result in results:
        email_list.append(result['email'])
    return email_list
