import re
from flask import Blueprint, blueprints, render_template, session, url_for, redirect, request
from pymysql import NULL

from MySQL.MySQLDatabase import mysql

from together.table import case_detail, case_detail_object

from datetime import date
user_2_blueprints = Blueprint('user_2', __name__, template_folder='templates', static_folder='static')


@user_2_blueprints.route('/A1', methods=['GET', 'POST'])
def A1():
    #檢查是否有登入 if not, redirect to login page
    if session['loggedin']:
        #案件登入頁面

        #先從資料庫取下拉式選單要用的值
        #建立游標
        cursor = mysql.get_db().cursor()
        #抓取下拉式選單所需資料
        cursor.execute('SELECT personal_or_company_id, personal_or_company FROM personal_or_company')
        pers_or_com = cursor.fetchall()

        # 如果案件登入按鈕被啟動
        if request.method == 'POST' and 'identity_id' in request.form and 'name' in request.form and 'cause' in request.form and 'inverse' in request.form and 'contract_lawyer' in request.form and 'personal_or_company_select' in request.form:
            #抓取表單中的資料
            identity_id = request.form.get('identity_id')
            name = request.form.get('name')
            cause = request.form.get('cause')
            inverse = request.form.get('inverse')
            contract_lawyer = request.form.get('contract_lawyer')
            personal_or_company = request.form.get('personal_or_company_select')


            #檢查客戶資料是否已經存在
            cursor.execute('SELECT name FROM client WHERE name = %s', (name,))
            client = cursor.fetchone()
            if client:
                # 如果client 存在，重新抓取資料
                cursor.execute('SELECT identity_id FROM client WHERE name = %s', (name,))
                client_identity_id = cursor.fetchone()
                # 如果identity_id 不等於"" 且 client_identity 為空
                if identity_id != "" and client_identity_id[0] == "":
                    # 更新identity_id資料
                    cursor.execute('UPDATE client SET identity_id = %s WHERE name = %s', (identity_id, name,))
            else:     
                #先做客戶資料登入
                cursor.execute('INSERT INTO client VALUES (NULL, %s, %s, %s)', (name, identity_id, personal_or_company,))

            #客戶資料抓取客戶ID
            cursor.execute('SELECT Client_id FROM client WHERE name = %s', (name,))
            Client = cursor.fetchone()
            Client_id = Client[0]

            #從系統抓取時間
            today = date.today()
            
            #做案件登入
            cursor.execute('INSERT INTO dentons_case VALUES (NULL, %s, %s, %s, %s, %s, 0)', (today, Client_id, cause, inverse, contract_lawyer,))
            

        #pers_or_com 為下拉式選單所需資料
        return render_template('user_2_A1.html', pers_or_com = pers_or_com)
    else:
        return redirect(url_for('Login.login'))


@user_2_blueprints.route('/A2', methods=['GET', 'POST'])
def A2():
    # Check if they've loggedin, if not redirect to login page
    if session['loggedin']:
        #利衝檢索頁面
        #建立資料庫游標
        cursor = mysql.get_db().cursor()

        #建立欲顯示資料的list
        search_data = [("案件編號", "日期", "當事人", "案由", "對造", "承辦律師", "結案")]

        # default錯誤訊息與是否衝突
        data_exist = False
        msg = ""

        #從表單獲取欲搜尋的資料
        if request.method == 'POST' and 'profit_search_input' in request.form:
            search_name = request.form.get('profit_search_input')

            #從資料庫獲取inverse為輸入姓名的案件資料
            cursor.execute('SELECT Case_id, date_time, Client_id, cause, inverse, contract_lawyer, over_id FROM dentons_case WHERE inverse = %s', (search_name,))
            case_data = cursor.fetchall()


            if case_data:
                data_exist = True

                #分別讀取Client_name over_or_not 資料
                for Case_id, date_time, Client_id, cause, inverse, contract_lawyer, over_id in case_data:
                    # 用Client_id讀取該案件當事人(非對造)資料
                    cursor.execute('SELECT name FROM client WHERE Client_id = %s', (Client_id,))
                    name = cursor.fetchone()
                    Client_name = name[0]

                    #用over_id 讀取是否已結案
                    cursor.execute('SELECT yes_or_no FROM over_or_not WHERE over_id = %s', (over_id,))
                    yes_or_not = cursor.fetchone()
                    over_or_not = yes_or_not[0]

                    #將資料加入search_data
                    search_data.append((Case_id, date_time, Client_name, cause, inverse, contract_lawyer, over_or_not))

            else:
                msg="查無相關案件"
                
        return render_template('user_2_A2.html', search_data=search_data, data_exist=data_exist, msg=msg)
    else:
        return redirect(url_for('Login.login'))


@user_2_blueprints.route('/A3')
def A3():
    # Check if they've loggedin, if not redirect to login page
    if session['loggedin']:
        #案件刪除頁面

        #建立cases_list
        cases_list = []
        #從session 抓取Account_id
        Account_id = session['Account_id']
        
        #建立游標
        cursor = mysql.get_db().cursor()

        #從帳號資料庫抓取帳號名稱
        cursor.execute('SELECT name FROM account WHERE Account_id = %s', (Account_id,))
        Account_name = cursor.fetchone()
        #若要取用--> Account_name[0]
        
        #從案件資料庫搜尋承辦律師為此account的案件
        cursor.execute('SELECT Case_id, date_time, Client_id, cause, inverse, contract_lawyer, over_id FROM dentons_case WHERE contract_lawyer = %s', (Account_name[0],))
        cases = cursor.fetchall()

        for Case_id, date_time, Client_id, cause, inverse, contract_lawyer, over_id in cases:
            # 用Client_id讀取該案件當事人資料
            cursor.execute('SELECT name FROM client WHERE Client_id = %s', (Client_id,))
            name = cursor.fetchone()
            Client_name = name[0]

            #用over_id 讀取是否已結案
            cursor.execute('SELECT yes_or_no FROM over_or_not WHERE over_id = %s', (over_id,))
            yes_or_not = cursor.fetchone()
            over_or_not = yes_or_not[0]

            cases_list.append(case_detail_object(Case_id, date_time, Client_name, cause, inverse, contract_lawyer, over_or_not))


        msg="您尚未登記任何案件"

        if cases:
            msg=""
            table = case_detail(cases_list)
            return render_template('user_2_A3.html', table=table)
        else:
            return render_template('user_2_A3.html', msg=msg)
    else:
        return redirect(url_for('Login.login'))


@user_2_blueprints.route('/edit/<int:Case_id>', methods=['GET', 'POST'])
def edit(Case_id):
    #建立游標
    cursor = mysql.get_db().cursor()
    
    #把案件編號為Case_id的資料取出來
    cursor.execute('SELECT Case_id, date_time, Client_id, cause, inverse, contract_lawyer, over_id FROM dentons_case WHERE Case_id = %s', (Case_id,))
    case_data = cursor.fetchone()
    print(case_data, type(case_data))
    return redirect(url_for('user_2.A3'))