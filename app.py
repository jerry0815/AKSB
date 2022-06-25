import flask
from flask import Flask, request , render_template
from flask import redirect , url_for, make_response
import os
import re
import pymysql
import pytz
from user import *
from record import *
from classroom import *
import datetime

app = Flask(__name__)


dummy_record = {'recordID':'1', 'title':'dummy', 'startDate':'2021-02-01', 'startSection':1, 'endDate':'2021-01-31', 'endSection':10,
'roomName':'TR-411', 'building':'研揚大樓(TR)', 'participant':[]}

"""
#test DB route
@app.route('/testDB_classroom',methods=['POST','GET'])
def testDB_classroom():
    result = showClassroom()
    return render_template("testDB_classroom.html" , data = result)
    #return result

@app.route('/testDB_users',methods=['POST','GET'])
def testDB_users():
    result = validateLogin("jerry","123456789")
    if result == None:
        return render_template("testDB_users.html" , data = result , status = 1)
    return render_template("testDB_users.html" , data = result , status = 0)
    #return result

@app.route('/testDB_record',methods=['POST','GET'])
def testDB_record():
    result = getRecordByBooker('jerry')
    print(result)
    return render_template("testDB_record.html" , data = result)
    #return result
"""


#================================================================
#new
#buildings=['研揚大樓(TR)','第四教學大樓(T4)','綜合研究大樓(RB)','國際大樓(IB)','電資館(EE)']
buildings = ["工程一館(EA)" , "工程二館(EB)" , "工程三館(EC)" , "工程四館(ED)" , "工程五館(EE)", 
        "科學一館(SA)", "科學二館(SB)", "基礎科學教學研究大樓(SC)", "學生活動中心(AC)", "綜合一館(A)", 
        "綜合一館地下室(AB)", "人社一館(HA)", "光電大樓(EO)"]
weekdays= ['一', '二', '三', '四','五','六','日']

def cookie_check():
    """
    check cookie's correctness
    """
    email = request.cookies.get("email")
    password = request.cookies.get('password')
    return loginCheck(email, password)

def get_current_time():
    taipei = pytz.timezone('Asia/Taipei')
    return datetime.datetime.strftime(datetime.datetime.now(taipei), "%Y-%m-%d")
@app.route('/logout')
def logout():
    res = make_response(redirect(url_for("login_page")))
    res.set_cookie(key='email', value='', expires=0)
    res.set_cookie(key='password', value='', expires=0)
    res.set_cookie(key='userName', value='', expires=0)
    return res

@app.route('/register',methods=['POST','GET'])
def register_page():
    if cookie_check()[0]:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        result = request.form
        if register(result):
            #註冊成功
            return render_template("register.html", message="register_success")
        else:
            #註冊失敗
            return render_template("register.html", message="register_error")
    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login_page():
    if cookie_check()[0]:
        return redirect(url_for('main_page'))
    if request.method =='POST':
        #TODO encryption
        email = request.form['email'] + "@gmail.com"
        login_status = validateLogin(email, request.form['password'])
        #login fail
        if login_status[0]:
            if login_status[0] == 1: #email error
                return render_template("login.html", message="email_error")
            elif login_status[0] == 2: #password error
                return render_template("login.html", message="password_error")
        #login success
        else:
            # resp = make_response(redirect('authorize'))
            # #set cookie
            # resp.set_cookie('email', email) 
            # resp.set_cookie('password', request.form['password'])
            # resp.set_cookie('userName', login_status[1])
            resp = make_response(redirect(url_for("main_page")))#,admin=loginCheck(email, request.form['password'])[1])))
            #resp = make_response(render_template("main.html", admin=loginCheck(email, request.form['password'])[1]))
            resp.set_cookie('email', email) 
            resp.set_cookie('password', request.form['password'])
            resp.set_cookie('userName', login_status[1])
            return resp
    return render_template("login.html", message=None)

@app.route('/search',methods=['POST','GET'])
def search_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method =='POST':
        result = request.form
        building = re.findall("[A-Z0-9]+",result['building'])
        if(len(building) > 0):
            building = building[0]
        else:
            building = ""
        search_result = searchClassroom(building = building , capacity = result['capacity'] , roomname = result['roomName'] , date = result['date'])
        return render_template("search.html", buildings=buildings, date=result['date'], result=search_result, admin = check[1] )
    return render_template("search.html", buildings=buildings, date=get_current_time(), result=None, admin = check[1] )
    
@app.route('/borrow',methods=['POST','GET'])
def borrow_page():
    message = ""
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))

    userData = getUser(request.cookies.get('userName'))

    allUserNames = getAllUserName()
    allUserNames.remove(request.cookies.get('userName'))

    if request.method == "POST":
        result = borrow(request.form, request.form['borrow_type'] , request.cookies.get("userName"))
        if request.form['borrow_type'] == "borrow":
            if result: 
                message="borrow_success"
            else:
                message="borrow_fail"
        elif request.form['borrow_type'] == "ban":
            if result: 
                message="ban_success"
            else:
                message="ban_fail"
        
        return render_template("borrow.html", buildings=buildings, admin=check[1], message=message, allUserNames=allUserNames)
      
    
    return render_template("borrow.html", buildings=buildings, admin=check[1], allUserNames=allUserNames)

@app.route('/borrow_search',methods=['POST','GET'])
def borrow_search_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))

    if request.method == "POST":
        print('borrow_search:',request.form)
        #to to search for boroow
        result = filter_classroom(request.form)
        return render_template("borrow_search.html", result=result)

    return render_template("borrow_search.html")

@app.route('/record',methods=['POST','GET'])
def record_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    records = []
    email = request.cookies.get("email")
    if email != None:
        records = getRecordByBookerEmail(email)
    return render_template("record.html", userName = request.cookies['userName'], records=records, admin = check[1])

@app.route('/single_record',methods=['POST'])
def single_record_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))

    if request.method =='POST':
        if request.form['postType'] == 'get':
            allUserNames = getAllUserName()
            allUserNames.remove(request.cookies.get('userName'))
            record = getRecordById(request.form['recordID'])
            remainingUserNames = []
            for name in allUserNames:
                if name not in record['participant']:
                    remainingUserNames.append(name)
            return render_template("single_record.html",record = record, admin = check[1], remainingUserNames = remainingUserNames)
        elif request.form['postType'] == 'modify':
            modify_record(request.form)
            return render_template("single_record.html",record = dummy_record, admin = check[1], message="modify_success")
        elif request.form['postType'] == 'delete':
            deleteRecord(request.form['recordID'])
            return redirect(url_for('record_page'))
    return redirect(url_for('main_page'))

@app.route('/', methods=['POST', 'GET'])
def main_page():
    check = cookie_check()
    #if cookie exists and user information is correct, then enter main page 
    if check[0]:
        return render_template("main.html", user_name = request.cookies.get('email'), admin=check[1])
    return redirect(url_for('login_page'))
         
@app.route('/account_management', methods=['POST', 'GET'])
def account_management_page():
    #if cookie exists and user information is correct, then enter main page 
    check = cookie_check()
    message = ""
    if check[0] and check[1] == "admin":
        allUserNames = getAllUserName()
        allUserNames.remove(request.cookies.get('userName'))
        if request.method == "POST":

            #do operation
            if request.form['postType'] == "search":
                result = getUser(request.form['userName'])
                if not result[0]:
                    message = "error"
                return render_template("account_management.html", user = result[1], admin=check[1], message = message, allUserNames = allUserNames)
            elif request.form['postType'] == "delete":
                result = deleteAccount(request.form['userID'])

            #check operation result
            if result:
                result = request.form['postType'] + '_success'
                if request.form['postType'] == "delete":
                    allUserNames.remove(request.form['userName'])
            else:
                result = request.form['postType'] + '_fail'

            return render_template("account_management.html", user = None, admin=check[1], message = result, allUserNames = allUserNames)
        return render_template("account_management.html", user = None, admin=check[1], allUserNames = allUserNames)
    else:
        return redirect(url_for('login_page'))
      
@app.route('/search_single',methods=['POST','GET'])
def search_single_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method =='POST':
        classroom_data = searchOneClassroom(CR_ID = request.form['CR_ID'] , date = request.form['start_date'])
    

        today = datetime.datetime.fromisoformat(request.form['start_date'])

        start_date = today - datetime.timedelta(days = today.weekday())
        
        dates = [start_date]
        for i in range(1,7):
            dates.append(start_date + datetime.timedelta(i))
        for i in range(7):
            dates[i] = datetime.datetime.strftime(dates[i], "%Y-%m-%d")

        return render_template("search_single.html",classroom = classroom_data,
                                                    dates = dates,
                                                    dates_weekdays = weekdays,
                                                    admin = check[1])
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test Key"
    app.run()