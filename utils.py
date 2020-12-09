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
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def to_bool(x):
    if x in ["False", "0", 0, False]:
        return False
    elif x in ["True", "1", 1, True]:
        return True
    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


# -------------------------------------------------------------
# Helper functions for Page scrolling
# -------------------------------------------------------------
# check if height changed
def check_height(driver, selectors, old_height):
    new_height = driver.execute_script(selectors.get("height_script"))
    return new_height != old_height


# helper function: used to scroll the page
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


# -----------------------------------------------------------------------------
# Helper Functions for Posts
# -----------------------------------------------------------------------------


def get_status(x, selectors):
    status = ""
    try:
        status = x.find_element_by_xpath(
            selectors.get("status")
        ).text  # use _1xnd for Pages
    except Exception:
        try:
            status = x.find_element_by_xpath(selectors.get("status_exc")).text
        except Exception:
            pass
    return status
def get_status_bs(x, selectors):
    status = ""
    try:
        status = x.find_all('div',attrs={'class':'_5_jv _58jw'})[0].text  # use _1xnd for Pages
    except Exception:
        try:
            status = x.find_all('div',attrs={'class':'userContent'})[0].text
        except Exception:
            pass
    return status

def get_div_links(x, tag, selectors):
    try:
        temp = x.find_element_by_xpath(selectors.get("temp"))
        return temp.find_element_by_tag_name(tag)
    except Exception:
        return ""
def get_div_links_bs(x, tag, selectors):
    try:
        temp = x.find_all('div',attrs={'class':'_3x-2'})[0]
        return temp.find(tag)
    except Exception:
        return ""

def get_title_links(title):
    l = title.find_elements_by_tag_name("a")
    return l[-1].text, l[-1].get_attribute("href")
def get_title_links_bs(title):
    l = title.find("a")
    return l[-1].text, l[-1]["href"]

def get_title(x, selectors):
    title = ""
    try:
        title = x.find_element_by_xpath(selectors.get("title"))
    except Exception:
        try:
            title = x.find_element_by_xpath(selectors.get("title_exc1"))
        except Exception:
            try:
                title = x.find_element_by_xpath(selectors.get("title_exc2"))
            except Exception:
                pass
    finally:
        return title
def get_title_bs(x, selectors):
    title = ""
    try:
        title = x.find_all('span',attrs={'class':'fwb fcg'})[0]
    except Exception:
        try:
            title = x.find_all('span',attrs={'class':'fcg'})[0]
        except Exception:
            try:
                title = x.find_all('span',attrs={'class':'fwn fcg'})[0]
            except Exception:
                pass
    finally:
        return title

def get_time(x):
    time = ""
    try:
        time = x.find_element_by_tag_name("abbr").get_attribute("title")
        time = (
            str("%02d" % int(time.split(", ")[1].split()[1]),)
            + "-"
            + str(
                (
                    "%02d"
                    % (
                        int(
                            (
                                list(calendar.month_abbr).index(
                                    time.split(", ")[1].split()[0][:3]
                                )
                            )
                        ),
                    )
                )
            )
            + "-"
            + time.split()[3]
            + " "
            + str("%02d" % int(time.split()[5].split(":")[0]))
            + ":"
            + str(time.split()[5].split(":")[1])
        )
    except Exception:
        pass

    finally:
        return time
