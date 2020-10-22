from read_db import read_db
import mysql.connector
import os
import pandas as pd
import csv
import urllib
from urllib.parse import urlparse
from urllib.parse import unquote
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import numpy as np
import json
import time

def main(que):
    server_db = read_db()
    mydb = mysql.connector.connect(
        host="localhost",       # 数据库主机地址
        user="test",    # 数据库用户名
        passwd="12Q3qeqs,",   # 数据库密码
        database='fbidname'
    )
    
    #if len(que) != 0:
    
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM fbidname1")

    local_db = mycursor.fetchall() 

    mycursore = mydb.cursor()

    mycursore.execute("SELECT * FROM fbidnameerrorlist")

    local_dbe = mycursore.fetchall() 
    
    if len(local_db) < len(server_db):
        starting_point = len(local_db)
        sql = ""
        for i in range(starting_point,len(server_db)):
            que.append(server_db[i])
            sql = "INSERT INTO fbidname1 (id, page) VALUES (%s, %s)"
            val = (server_db[i][0], server_db[i][1])
            mycursor.execute(sql, val)
            mydb.commit()
    if len(local_dbe) != 0:
        for sub in local_dbe:
            que.append(sub)
    if len(que) != 0:

        print('que',que)
    if os.path.getsize("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt") == 0 and len(que) != 0:
        
        input_text = open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt", "w")
        input_text.write(que[0][0]+','+que[0][1]+',w1\n')
        input_text.close()
        que.pop(0)
            # que.pop(1)
            # user_id_o = create_original_link(server_db[i][1])
            # folder = os.path.join(os.getcwd(), "data")
            # user_id = os.path.join(folder, user_id_o.split("/")[-1])
    if os.path.getsize("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w2.txt") == 0 and len(que) != 0:
        input_text = open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w2.txt", "w")
        input_text.write(que[0][0]+','+que[0][1]+',w2\n')
        input_text.close()
        que.pop(0)
    
    if os.path.getsize("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w3.txt") == 0 and len(que) != 0:
        input_text = open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w3.txt", "w")
        input_text.write(que[0][0]+','+que[0][1]+',w3\n')
        input_text.close()
        que.pop(0)

            # for i in range(starting_point,len(server_db)):
            #     input_text = open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/input.txt", "w")
            #     input_text.write(server_db[i][1])
            #     input_text.close()
    # print('quea',que)
if __name__ == '__main__':
    que = []
    while True:
        main(que)
        time.sleep(1)
