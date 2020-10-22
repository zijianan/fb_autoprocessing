import mysql.connector


def read_db():
    mydb = mysql.connector.connect(
        host="3.21.245.114",       # 数据库主机地址
        user="test",    # 数据库用户名
        passwd="12Q3qeqs,",   # 数据库密码
        database='fbidname'
    )
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM fbidnameT")
    
    myresult = mycursor.fetchall()     # fetchall() 获取所有记录
    return myresult

