import argparse
import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import mysql.connector

def read_db(dbid):
    mydb = mysql.connector.connect(
        host="3.21.245.114",       # 数据库主机地址
        user="test",    # 数据库用户名
        passwd="12Q3qeqs,",   # 数据库密码
        database='fbidname'
    )
    mycursor = mydb.cursor()
    dbid = "'"+dbid+"'"
    mycursor.execute("SELECT * FROM fbidname3 WHERE userid=%s" % dbid)
    
    myresult = mycursor.fetchall()     # fetchall() 获取所有记录
    if len(myresult) != 0:
        return True
    else:
        return False
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
        
        
def scroll(total_scrolls, driver, selectors, scroll_time, dbid):
    global old_height
    current_scrolls = 0
    starting_time = time.time()
    while True:
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script(selectors.get("height_script"))
            driver.execute_script(selectors.get("scroll_script"))
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height(driver, selectors, old_height)
            )
            current_scrolls += 1
        except TimeoutException:
            break
        current_time = time.time()
        if current_time - starting_time >= 600:
            break
        if read_db(dbid):
            break

    return
