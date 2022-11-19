# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 21:13:20 2022

@author: abika
"""

from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db, re
from sendmail1 import sendgridmail
app = Flask(__name__)
app.secret_key = 'a'



dsn_hostname = "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud" 
dsn_uid = "wtv78446"        
dsn_pwd = "UUNUuJQDGrGpjRkP"      
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"            
dsn_port = "32716"                
dsn_protocol = "TCPIP"            
dsn_security = "SSL"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

conn = ibm_db.connect(dsn, "", "")

@app.route("/")

def home():
    return render_template('home.html', methods =['GET', 'POST'])
	 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        stmt = ibm_db.prepare(conn,"select * from user where username = ?")
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_tuple(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            stmt = ibm_db.prepare(conn,"INSERT INTO user(username, password, email) VALUES(?,?,?)")
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.bind_param(stmt, 3, email)
            ibm_db.execute(stmt)
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for registring at MONEYDEED$ """ 
            sendgridmail(TEXT,email)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('/register.html', msg = msg)


@app.route('/login', methods =['GET', 'POST'])
def login():
    global userid
    msg = '' 
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        stmt = ibm_db.prepare(conn,"select * from user where username = ? and password = ?")
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_tuple(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        
        else:
            msg = 'Incorrect username / password !'
    return render_template('/login.html', msg = msg)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/wallet',methods =['GET', 'POST'])
def wallet():
    msg = ''
    if request.method == 'POST' :
        #user_id= session["id"]
        #balance = "SELECT skills FROM job where userid = id"
        stmt = ibm_db.prepare(conn,"select * from credit where userid = ?")
        ibm_db.bind_param(stmt, 1, session['id'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_tuple(stmt)
        income = request.form.get("income")
        if account:
         print(account)
         #username = request.form['username']
         #email = request.form['email']
         balance = account[1]  + float(request.form.get("income"))
         #income = float(request.form.get("income"))
         print(balance)
         stmt = ibm_db.prepare(conn,"UPDATE credit SET income = ? WHERE userid = ?")
         ibm_db.bind_param(stmt, 1, balance)
         ibm_db.bind_param(stmt, 2, session['id'])
         ibm_db.execute(stmt)
                  
        else:
            stmt = ibm_db.prepare(conn,"insert into credit(userid, income) VALUES(?,?)")
            ibm_db.bind_param(stmt, 1, session['id'])
            ibm_db.bind_param(stmt, 2, income)
            ibm_db.execute(stmt)
            
        msg = 'You have successfully added your money to your wallet !'
        session['loggedin'] = True
     
                   
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('wallet.html', msg = msg)

@app.route('/debit',methods =['GET', 'POST'])
def debit():
    msg =''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        debit = request.form['debit']
        reason = request.form['s']
        stmt = ibm_db.prepare(conn,"select * from credit where userid = ?")
        ibm_db.bind_param(stmt, 1, session['id'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_tuple(stmt)
        print(account)
        balance = account[1]  - float(request.form.get("debit"))
        print(balance)
        stmt = ibm_db.prepare(conn,"UPDATE credit SET income = ? WHERE userid = ?")
        ibm_db.bind_param(stmt, 1, balance)
        ibm_db.bind_param(stmt, 2, session['id'])
        ibm_db.execute(stmt)
        msg = 'You have successfully debited your money from your wallet !'
        session['loggedin'] = True
         
        if balance == 0 or balance < 0:
            TEXT = "Hello   "+username + ", \n\n"+ """ALERT: You have exceeded your limit """ 
            sendgridmail(TEXT,email)
        
         
         
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('debit.html', msg = msg)
        


@app.route('/display')
def display():
    
    print(session["username"],session['id'])
    stmt = ibm_db.prepare(conn,"select * from user where id = ?")
    ibm_db.bind_param(stmt, 1, session['id'])
    ibm_db.execute(stmt)
    account = ibm_db.fetch_tuple(stmt)
    print("accountdislay",account)
    
    stmt1 = ibm_db.prepare(conn,"select * from credit where userid = ?")
    ibm_db.bind_param(stmt1, 1, session['id'])
    ibm_db.execute(stmt1)
    acct = ibm_db.fetch_tuple(stmt1)
    print(acct)    

    
    return render_template('display.html',account = account, acct = acct)

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')



if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 5000)
   
#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
