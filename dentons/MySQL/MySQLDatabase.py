from flaskext.mysql import MySQL

#autocommit 要 = True 資料才會真的存進去
mysql = MySQL(autocommit=True)