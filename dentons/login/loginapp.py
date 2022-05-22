from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from flask.helpers import get_flashed_messages

from MySQL.MySQLDatabase import mysql

from func import password_encryption



Login_blueprints = Blueprint('Login', __name__, template_folder='templates', static_folder='static')


@Login_blueprints.route('/', methods=['GET', 'POST'])
def login():
    #檢查request方式是否為post (form我們的method設為post)   以及檢查 form 裡的 username 跟 password 是否有東西
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #如果都有  先把值放進變數等待使用
        username = request.form['username']
        password = request.form['password']


        #先對password做加密，再去驗證是否存在於資料庫中


        #check if account exists with MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()


        # if account exists in account table
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['Account_id'] = account[0] # index 0 is "Account_id" in database
            session['username'] = account[1] # index 1 is "username" in database
            session['account_level'] = account[6] # index 6 is "account_level" in database
            session['codename'] = account[5] # index 5 is "codename" in database


            # 依照帳號等級切換頁面  預設皆 Redirect to A1
            if session['account_level'] == 1:
                return redirect(url_for('user_1.A1'))
            elif session['account_level'] == 2:
                return redirect(url_for('user_2.A1'))


        else:
            flash('帳號或密碼錯誤')
    

    return render_template('login.html')

