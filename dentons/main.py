from flask import Flask, url_for, redirect, session
import os


#資料庫連線
from MySQL.MySQLDatabase import mysql


#匯入blueprints
from login.loginapp import Login_blueprints
from logout.logoutapp import Logout_blueprints
from user_1.user_1_app import user_1_blueprints
from user_2.user_2_app import user_2_blueprints

#建立dentons 這個 app
dentons = Flask(__name__)


#引入blueprint
dentons.register_blueprint(Login_blueprints, url_prefix='/login')
dentons.register_blueprint(Logout_blueprints, url_prefix='/logout')
dentons.register_blueprint(user_1_blueprints, url_prefix='/user_1')
dentons.register_blueprint(user_2_blueprints, url_prefix='/user_2')

#session的secret_key 設置
dentons.secret_key = os.urandom(24)



#MySQL Database
mysql.init_app(dentons)
dentons.config['MYSQL_DATABASE_HOST'] = 'arfiligol.xn--kpry57d'
dentons.config['MYSQL_DATABASE_USER'] = 'falling_flowers'
dentons.config['MYSQL_DATABASE_PASSWORD'] = 'Dragon@25468'
dentons.config['MYSQL_DATABASE_DB'] = 'dentons'


#連線伺服器位址時 Redirect to login page
@dentons.route('/')
def toLogin():
    # default session['loggedin'] = False
    session['loggedin'] = False
    return redirect(url_for('Login.login'))



#使用內建網頁伺服器執行 為了讓safari也可以讀取 暫時把https刪除 （  ssl_context=('fullchain.pem', 'privkey.pem')  ）
dentons.run(debug=True, host="0.0.0.0", port=443, ssl_context=('fullchain.pem', 'privkey.pem'))
