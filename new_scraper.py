import calendar
import json
import os
import platform
import sys
import urllib.request
import yaml
import utils
import argparse
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import pandas as pd
import csv
import urllib
from urllib.parse import urlparse
from urllib.parse import unquote
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import mysql.connector
from urllib.parse import urlparse, parse_qsl, parse_qs, urlunparse, urlencode
from lxml import html
from bs4 import BeautifulSoup as bs
import datefinder
from datetime import datetime
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
starttime = time.time()

def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options
            )
        except Exception:
            print(
                "Kindly replace the Chrome Web Driver with the latest one from "
                "http://chromedriver.chromium.org/downloads "
                "and also make sure you have the latest Chrome Browser version."
                "\nYour OS: {}".format(platform_)
            )
            exit(1)
        facebook_https_prefix = selectors.get("facebook_https_prefix")
        facebook_link_body = selectors.get("facebook_link_body")
        fb_path = facebook_https_prefix + facebook_link_body
        driver.get(fb_path)
        driver.maximize_window()

        # filling the form
        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_name("pass").send_keys(password)

        try:
            # clicking on login button
            driver.find_element_by_id("loginbutton").click()
        except NoSuchElementException:
            # Facebook new design
            driver.find_element_by_name("login").click()
        time.sleep(1)

    except Exception:
        print("There's some error in log in.")
        print(sys.exc_info())
        exit(1)
def scrap_profile(user_id):
    folder = os.path.join(os.getcwd(), "data")
    utils.create_folder(folder)
    os.chdir(folder)

    # execute for all profiles given in input.txt file

    driver.get(user_id)
    url = driver.current_url
    # user_id = create_original_link(url)

    print("\nScraping:", user_id)

    try:
        target_dir = os.path.join(folder, dbid)
        utils.create_folder(target_dir)
        os.chdir(target_dir)
    except Exception:
        print("Some error occurred in creating the profile directory.")

    to_scrap = ["Posts"]
    item = "Posts"
    # for item in to_scrap:
    #     print("----------------------------------------")
    #     print("Scraping {}..".format(item))

    #     if item == "Posts":
    #         scan_list = [None]
    #     elif item == "About":
    #         scan_list = [None] * 7
    #     else:
    #         scan_list = params[item]["scan_list"]

    section = params[item]["section"]
    elements_path = params[item]["elements_path"]
    file_names = params[item]["file_names"]
    save_status = params[item]["save_status"]

    scrape_data(
        user_id, [None], section, elements_path, save_status, file_names
    )

    print("{} Done!".format(item))

    print("\nProcess Completed.")
    os.chdir("../..")

    return

def scrape_data(user_id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []

    if save_status == 4:
        page.append(user_id)

    page += [user_id + s for s in section]

    for i, _ in enumerate(scan_list):
#        try:
        driver.get(page[i])
     
        if save_status != 3:
            utils.scroll(total_scrolls, driver, selectors, scroll_time, dbid)

        data = bs(driver.page_source, 'lxml').find_all('div', attrs={"class":"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"})
        if len(data) == 0:
            driver.refresh()
            time.sleep(0.5)
            driver.find_element_by_xpath("//a[contains(text(),'Timeline')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//a[contains(text(),'Timeline')]").click()
            time.sleep(3)
            data = bs(driver.page_source, 'lxml').find_all('div', attrs={"class":"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"})
        save_to_file(file_names[i], data, save_status, i)

def save_to_file(name, elements, status, current_section):
    """helper function used to save links to files"""

    # status 0 = dealing with friends list
    # status 1 = dealing with photos
    # status 2 = dealing with videos
    # status 3 = dealing with about section
    # status 4 = dealing with posts
    results = []
    img_names = []
    if status == 4:
        extract_and_write_posts(elements, name)
        return


def extract_and_write_posts(elements, filename):
    import time as tt
    start = tt.time()
    print(start,len(elements))
    try:
        f = open(filename, "w", newline="\r\n")
        f.writelines(
            "TIME||TYPE||TITLE||STATUS||LINKS"
            + "\n"
            + "\n"
        )

        for x in elements:
            try:
                title = " "
                status = " "
                link = ""

                # time
                # time = x.find_all('abbr')[0]['title']
                # url = x.find_element_by_xpath('//a[contains(@href,"href")]')
                # # title
                # title = utils.get_title_bs(x, selectors)
                # if title.text.find("shared a memory") != -1:
                #     x = x.find_all('div',attrs={'class':'_1dwg _1w_m'})
                #     title = utils.get_title_bs(x, selectors)

                # status = utils.get_status_bs(x, selectors)
                # if (
                #     title.text
                #     == driver.find_element_by_id(selectors.get("title_text")).text
                # ):
                #     if status == "":
                #         temp = utils.get_div_links_bs(x, "img", selectors)
                #         if (
                #             temp == ""
                #         ):  # no image tag which means . it is not a life event
                #             link = utils.get_div_links_bs(x, "a", selectors)[
                #                 "href"
                #             ]
                #             type = "status update without text"
                #         else:
                #             type = "life event"
                #             link = utils.get_div_links_bs(x, "a", selectors)[
                #                 "href"
                #             ]
                #             status = utils.get_div_links_bs(x, "a", selectors).text
                #     else:
                #         type = "status update"
                #         if utils.get_div_links_bs(x, "a", selectors) != "":
                #             link = utils.get_div_links_bs(x, "a", selectors)[
                #                 "href"
                #             ]

                # elif title.text.find(" shared ") != -1:

                #     x1, link = utils.get_title_links_bs(title)
                #     type = "shared " + x1

                # # elif title.text.find(" at ") != -1 or title.text.find(" in ") != -1:
                # #     if title.text.find(" at ") != -1:
                # #         x1, link = utils.get_title_links(title)
                # #         type = "check in"
                # #     elif title.text.find(" in ") != 1:
                # #         status = utils.get_div_links(x, "a", selectors).text

                # # elif (
                # #     title.text.find(" added ") != -1 and title.text.find("photo") != -1
                # # ):
                # #     type = "added photo"
                # #     link = utils.get_div_links(x, "a", selectors).get_attribute("href")

                # # elif (
                # #     title.text.find(" added ") != -1 and title.text.find("video") != -1
                # # ):
                # #     type = "added video"
                # #     link = utils.get_div_links(x, "a", selectors).get_attribute("href")

                # else:
                #     type = "others"

                # if not isinstance(title, str):
                #     title = title.text

                # status = status.replace("\n", " ")
                # title = title.replace("\n", " ")
                linkdata = x.find_all('a', href=True, role='link')
                timedata = x.find_all('a',role="link",tabindex="0")
                for i in range(len(timedata)):
                    try:
                        tryts = timedata[i]['aria-label']
                        if len(list(datefinder.find_dates(tryts))) != 0:
                            time = list(datefinder.find_dates(tryts))[0].strftime("%m/%d/%Y")
               
                            break
                    except:
                        pass
                if len(elements) <= 1:
                    time = datetime.now().strftime("%m/%d/%Y")
                for sub in linkdata:
                    try:
                        link = sub['href']
                        if ids in link or 'https://www.facebook.com/' in link:
                            link = ""
                        elif link != '#':
            #                 print(link)
                            break
                    except:
                        pass
                line = (
                    time
                    + " || "
                    + ' '
                    + " || "
                    + ' '
                    + " || "
                    + ' '
                    + " || "
                    + str(link)
                    + "\n"
                )

                try:
                    f.writelines(line)
                except Exception:
                    print("Posts: Could not map encoded characters")
            except Exception:
                pass
        f.close()
        print(tt.time() - start)
    except Exception:
        print("Exception (extract_and_write_posts)", "Status =", sys.exc_info()[0])

    return

driver = None
CHROMEDRIVER_BINARIES_FOLDER = "bin"
total_scrolls = 2500
scroll_time = 8
global dbco
global dbid
global dbpf
with open("/home/zijianan/fb_autoprocessing/selectors.json") as a, open("/home/zijianan/fb_autoprocessing/params.json") as b:
    selectors = json.load(a)
    params = json.load(b)
with open("/home/zijianan/fb_autoprocessing/credentials.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(stream=ymlfile)
login(cfg["email"], cfg["password"])
    # ids = [dbpf]

while True:
    time.sleep(1)
    server_db = read_db()
    if len(server_db)!= 0:
        for (dbid,dbpf) in server_db:
            ids = dbpf
            try:
                scrap_profile(ids)
                with open('/home/zijianan/fb_autoprocessing/data/'+dbid+'/file.csv', 'w') as csvfile:
                    spamwriter = csv.writer(csvfile, dialect='excel')
                    # 读要转换的txt文件，文件每行各词间以@@@字符分隔
                    with open('/home/zijianan/fb_autoprocessing/data/'+dbid+'/Posts.txt') as filein:
                        for line in filein:
                            line_list = line.strip('\n').split('||')
                            spamwriter.writerow(line_list)
                csvfile = pd.read_csv('/home/zijianan/fb_autoprocessing/data/'+dbid+'/file.csv')
                csvfile['CLEAN'] = ''
                csvfile['INCLUDE'] = ''
                csvfile['id'] = dbid
                csvfile['LINKS'].replace(' ', np.nan, inplace=True)
                csvfile = csvfile.dropna()
                csvfile['CLEAN'] = csvfile['LINKS'].apply(lambda x: urlparse(unquote(x)[33:]).netloc if unquote(x)[1:32] == 'https://l.facebook.com/l.php?u=' else urlparse(unquote(x[1:])).netloc)
                
                for index, row in csvfile.iterrows():
                    o = urlparse(row['LINKS'])
                    params = {x:y for x,y in parse_qsl(o.query)}
                    if 'u' not in params:
                        csvfile.at[index,'INCLUDE'] = 'NO'
                        # print("DO NOT INCLUDE IN AWS DATASET")
                    else:
                        link = params['u']
                        link_url = urlparse(link)
                        query = parse_qs(link_url.query, keep_blank_values=True)
                        query.pop('fbid', None)
                        query.pop('fbclid', None)
                        query.pop('smid', None)
                        link_url = link_url._replace(query=urlencode(query, True))
                        csvfile.at[index,'INCLUDE'] = 'YES'
                        csvfile.at[index,'LINKS'] = urlunparse(link_url)
                engine = create_engine('mysql://fb:12Q3qeqs,@database-fb.crzk6iszblmx.us-east-1.rds.amazonaws.com/fbidname')
                with engine.connect() as conn, conn.begin():
                    upload = csvfile.loc[csvfile['INCLUDE'] == 'YES']
                    upload[['id','TIME','CLEAN','LINKS']].to_sql('fbidname2', conn, if_exists='append',index=False)
                eend = time.time()
                print(eend-starttime)
            except:
                eend = time.time()
                print(eend-starttime)
                print(dbid,sys.exc_info())
                mydb = mysql.connector.connect(
                host="localhost",       # 数据库主机地址
                user="fb_local",    # 数据库用户名
                passwd="12Q3qeqs,",   # 数据库密码
                database='fbidname'
                )
                sql = "INSERT INTO fbidnameerrorlist (qid, page) VALUES (%s, %s)"
                val = (dbid,ids)
                mycursor = mydb.cursor()
                mycursor.execute(sql, val)
                mydb.commit()

            mydb = mysql.connector.connect(
                    host="database-fb.crzk6iszblmx.us-east-1.rds.amazonaws.com",       # 数据库主机地址
                    user="fb",    # 数据库用户名
                    passwd="12Q3qeqs,",   # 数据库密码
                    database='fbidname'
                )
            mycursor = mydb.cursor()
            change_state = "update machine_state set state = 'available' where id = '1'"
            mycursor.execute(change_state)
            mydb.commit()
            delete = "DELETE FROM final_d WHERE qid = %s"
            qid = (dbid, )
            mycursor.execute(delete,qid)
            mydb.commit()


