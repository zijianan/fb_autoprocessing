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

from lxml import html
from bs4 import BeautifulSoup as bs
starttime = time.time()
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

def get_facebook_images_url(img_links):
    urls = []

    for link in img_links:
        if link != "None":
            valid_url_found = False
            driver.get(link)

            try:
                while not valid_url_found:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, selectors.get("spotlight"))
                        )
                    )
                    element = driver.find_element_by_class_name(
                        selectors.get("spotlight")
                    )
                    img_url = element.get_attribute("src")

                    if img_url.find(".gif") == -1:
                        valid_url_found = True
                        urls.append(img_url)
            except Exception:
                urls.append("None")
        else:
            urls.append("None")

    return urls


# -------------------------------------------------------------
# -------------------------------------------------------------

# takes a url and downloads image from that url
def image_downloader(img_links, folder_name):
    img_names = []

    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(os.getcwd(), folder_name)
            utils.create_folder(folder)
            os.chdir(folder)
        except Exception:
            print("Error in changing directory.")

        for link in img_links:
            img_name = "None"

            if link != "None":
                img_name = (link.split(".jpg")[0]).split("/")[-1] + ".jpg"

                # this is the image id when there's no profile pic
                if img_name == selectors.get("default_image"):
                    img_name = "None"
                else:
                    try:
                        urllib.request.urlretrieve(link, img_name)
                    except Exception:
                        img_name = "None"

            img_names.append(img_name)

        os.chdir(parent)
    except Exception:
        print("Exception (image_downloader):", sys.exc_info()[0])

    return img_names


# -------------------------------------------------------------
# -------------------------------------------------------------


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
                time = " "

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
                timedata = x.find_all('a', href=True, text=True)
                for sub in timedata:
                    try:
                        time = sub['aria-label']
            #             print(time)
                        break
                    except:
                        pass
                for sub in linkdata:
                    try:
                        link = sub['href']
                        if ids in link or 'https://www.facebook.com/' in link:
                            link = ""
                        else:
            #                 print(link)
                            break
                    except:
                        pass
                line = (
                    str(time)
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


# -------------------------------------------------------------
# -------------------------------------------------------------


def save_to_file(name, elements, status, current_section):
    """helper function used to save links to files"""

    # status 0 = dealing with friends list
    # status 1 = dealing with photos
    # status 2 = dealing with videos
    # status 3 = dealing with about section
    # status 4 = dealing with posts
    
    try:
        f = None  # file pointer

        if status != 4:
            f = open(name, "w", encoding="utf-8", newline="\r\n")

        results = []
        img_names = []

        # dealing with Friends
        if status == 0:
            # get profile links of friends
            results = [x.get_attribute("href") for x in elements]
            results = [create_original_link(x) for x in results]

            # get names of friends
            people_names = [
                x.find_element_by_tag_name("img").get_attribute("aria-label")
                for x in elements
            ]

            # download friends' photos
            try:
                if download_friends_photos:
                    if friends_small_size:
                        img_links = [
                            x.find_element_by_css_selector("img").get_attribute("src")
                            for x in elements
                        ]
                    else:
                        links = []
                        for friend in results:
                            try:
                                driver.get(friend)
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located(
                                        (
                                            By.CLASS_NAME,
                                            selectors.get("profilePicThumb"),
                                        )
                                    )
                                )
                                l = driver.find_element_by_class_name(
                                    selectors.get("profilePicThumb")
                                ).get_attribute("href")
                            except Exception:
                                l = "None"

                            links.append(l)

                        for i, _ in enumerate(links):
                            if links[i] is None:
                                links[i] = "None"
                            elif links[i].find("picture/view") != -1:
                                links[i] = "None"

                        img_links = get_facebook_images_url(links)

                    folder_names = [
                        "Friend's Photos",
                        "Mutual Friends' Photos",
                        "Following's Photos",
                        "Follower's Photos",
                        "Work Friends Photos",
                        "College Friends Photos",
                        "Current City Friends Photos",
                        "Hometown Friends Photos",
                    ]
                    print("Downloading " + folder_names[current_section])

                    img_names = image_downloader(
                        img_links, folder_names[current_section]
                    )
                else:
                    img_names = ["None"] * len(results)
            except Exception:
                print(
                    "Exception (Images)",
                    str(status),
                    "Status =",
                    current_section,
                    sys.exc_info()[0],
                )

        # dealing with Photos
        elif status == 1:
            results = [x.get_attribute("href") for x in elements]
            results.pop(0)

            try:
                if download_uploaded_photos:
                    if photos_small_size:
                        background_img_links = driver.find_elements_by_xpath(
                            selectors.get("background_img_links")
                        )
                        background_img_links = [
                            x.get_attribute("style") for x in background_img_links
                        ]
                        background_img_links = [
                            ((x.split("(")[1]).split(")")[0]).strip('"')
                            for x in background_img_links
                        ]
                    else:
                        background_img_links = get_facebook_images_url(results)

                    folder_names = ["Uploaded Photos", "Tagged Photos"]
                    print("Downloading " + folder_names[current_section])

                    img_names = image_downloader(
                        background_img_links, folder_names[current_section]
                    )
                else:
                    img_names = ["None"] * len(results)
            except Exception:
                print(
                    "Exception (Images)",
                    str(status),
                    "Status =",
                    current_section,
                    sys.exc_info()[0],
                )

        # dealing with Videos
        elif status == 2:
            results = elements[0].find_elements_by_css_selector("li")
            results = [
                x.find_element_by_css_selector("a").get_attribute("href")
                for x in results
            ]

            try:
                if results[0][0] == "/":
                    results = [r.pop(0) for r in results]
                    results = [(selectors.get("fb_link") + x) for x in results]
            except Exception:
                pass

        # dealing with About Section
        elif status == 3:
            results = elements[0].text
            f.writelines(results)

        # dealing with Posts
        elif status == 4:
            extract_and_write_posts(elements, name)
            return

        """Write results to file"""
        if status == 0:
            for i, _ in enumerate(results):
                # friend's profile link
                f.writelines(results[i])
                f.write(",")

                # friend's name
                f.writelines(people_names[i])
                f.write(",")

                # friend's downloaded picture id
                f.writelines(img_names[i])
                f.write("\n")

        elif status == 1:
            for i, _ in enumerate(results):
                # image's link
                f.writelines(results[i])
                f.write(",")

                # downloaded picture id
                f.writelines(img_names[i])
                f.write("\n")

        elif status == 2:
            for x in results:
                f.writelines(x + "\n")

        f.close()

    except Exception:
        print("Exception (save_to_file)", "Status =", str(status), sys.exc_info()[0])

    return


# ----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def scrape_data(user_id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []

    if save_status == 4:
        page.append(user_id)

    page += [user_id + s for s in section]

    for i, _ in enumerate(scan_list):
        try:
            driver.get(page[i])

            if (
                (save_status == 0) or (save_status == 1) or (save_status == 2)
            ):  # Only run this for friends, photos and videos

                # the bar which contains all the sections
                sections_bar = driver.find_element_by_xpath(
                    selectors.get("sections_bar")
                )

                if sections_bar.text.find(scan_list[i]) == -1:
                    continue

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

        except Exception:
            print(
                "Exception (scrape_data)",
                str(i),
                "Status =",
                str(save_status),
                sys.exc_info()[0],
            )


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = (
            facebook_https_prefix + facebook_link_body + ((url.split("="))[1])
        )

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = (
            facebook_https_prefix
            + facebook_link_body
            + ((url.split("/"))[-1].split("?")[0])
        )
    elif url.find("_tab") != -1:
        original_link = (
            facebook_https_prefix
            + facebook_link_body
            + (url.split("?")[0]).split("/")[-1]
        )
    else:
        original_link = url

    return original_link


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "data")
    utils.create_folder(folder)
    os.chdir(folder)

    # execute for all profiles given in input.txt file
    for user_id in ids:

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
            continue

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


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None


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

        # if your account uses multi factor authentication
        # mfa_code_input = safe_find_element_by_id(driver, "approvals_code")
        # try:
        #     driver.find_element_by_name("requests").click()
        #     time.sleep(3)
        # except:
        #     driver.refresh()
        #     time.sleep(2)
        #     driver.find_element_by_name("requests").click()
        #     time.sleep(3)
        # try:
        #     if len(driver.find_elements_by_name("actions[accept]")) > 1:
        #         for sub in driver.find_elements_by_name("actions[accept]"):
        #             sub.click()
        #             time.sleep(1)
            
        #     else:
        #         driver.find_element_by_name("actions[accept]").click()
        # except:
        #     pass

        
        # if mfa_code_input is None:
        #     return
        # mfa_code_input.send_keys(input("Enter MFA code: "))
        # driver.find_element_by_id("checkpointSubmitButton").click()

        # # there are so many screens asking you to verify things. Just skip them all
        # while safe_find_element_by_id(driver, "checkpointSubmitButton") is not None:
        #     dont_save_browser_radio = safe_find_element_by_id(driver, "u_0_3")
        #     if dont_save_browser_radio is not None:
        #         dont_save_browser_radio.click()

        #     driver.find_element_by_id("checkpointSubmitButton").click()

    except Exception:
        print("There's some error in log in.")
        print(sys.exc_info())
        exit(1)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def unfriends():
    # ids = [
    # line
    id = dbpf
    driver.get(id)
    driver.find_element_by_class_name('FriendButton').click()
    time.sleep(3)
    driver.find_element_by_partial_link_text('Unfriend').click()

def scraper(**kwargs):
    with open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/credentials.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(stream=ymlfile)

    if ("password" not in cfg) or ("email" not in cfg):
        print("Your email or password is missing. Kindly write them in credentials.txt")
        exit(1)

    ids = [dbpf]

    if len(ids) > 0:
        print("\nStarting Scraping...")

        login(cfg["email"], cfg["password"])
        scrap_profile(ids)
        # unfriends()
        driver.close()
    else:
        print("Input file is empty.")


# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

# if __name__ == "__main__":
ap = argparse.ArgumentParser()
# PLS CHECK IF HELP CAN BE BETTER / LESS AMBIGUOUS
ap.add_argument(
    "-dup",
    "--uploaded_photos",
    help="download users' uploaded photos?",
    default=True,
)
ap.add_argument(
    "-dfp", "--friends_photos", help="download users' photos?", default=True
)
ap.add_argument(
    "-fss",
    "--friends_small_size",
    help="Download friends pictures in small size?",
    default=True,
)
ap.add_argument(
    "-pss",
    "--photos_small_size",
    help="Download photos in small size?",
    default=True,
)
ap.add_argument(
    "-ts",
    "--total_scrolls",
    help="How many times should I scroll down?",
    default=2500,
)
ap.add_argument(
    "-st", "--scroll_time", help="How much time should I take to scroll?", default=8
)
ap.add_argument(
    "-dbco","--dbco",default='')
# ap.add_argument(
#     "-pf","--pf",default='')
args = vars(ap.parse_args())
print(args)

# ---------------------------------------------------------
# Global Variables
# ---------------------------------------------------------

# whether to download photos or not
download_uploaded_photos = utils.to_bool(args["uploaded_photos"])
download_friends_photos = utils.to_bool(args["friends_photos"])

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = utils.to_bool(args["friends_small_size"])
photos_small_size = utils.to_bool(args["photos_small_size"])

total_scrolls = int(args["total_scrolls"])
scroll_time = int(args["scroll_time"])
global dbco
global dbid
global dbpf
dbco = args["dbco"].split(',')
dbid = dbco[0]
dbpf = dbco[1]
dbw = dbco[2]
current_scrolls = 0
old_height = 0

driver = None
CHROMEDRIVER_BINARIES_FOLDER = "bin"

with open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/selectors.json") as a, open("/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/params.json") as b:
    selectors = json.load(a)
    params = json.load(b)

firefox_profile_path = selectors.get("firefox_profile_path")
facebook_https_prefix = selectors.get("facebook_https_prefix")
facebook_link_body = selectors.get("facebook_link_body")

# get things rolling
try:
    scraper()
    with open('/home/zijianan/fb_processing/data/'+dbid+'/file.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        # 读要转换的txt文件，文件每行各词间以@@@字符分隔
        with open('/home/zijianan/fb_processing/data/'+dbid+'/Posts.txt') as filein:
            for line in filein:
                line_list = line.strip('\n').split('||')
                spamwriter.writerow(line_list)
    csvfile = pd.read_csv('/home/zijianan/fb_processing/data/'+dbid+'/file.csv')
    csvfile['CLEAN'] = ''
    csvfile['INCLUDE'] = ''
    csvfile['id'] = dbid
    csvfile['LINKS'].replace(' ', np.nan, inplace=True)
    csvfile = csvfile.dropna()
    csvfile['CLEAN'] = csvfile['LINKS'].apply(lambda x: urlparse(unquote(x)[33:]).netloc if unquote(x)[1:32] == 'https://l.facebook.com/l.php?u=' else urlparse(unquote(x[1:])).netloc)
    from urllib.parse import urlparse, parse_qsl, parse_qs, urlunparse, urlencode
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
    engine = create_engine('mysql://test:12Q3qeqs,@3.21.245.114/fbidname')
    with engine.connect() as conn, conn.begin():
        upload = csvfile.loc[csvfile['INCLUDE'] == 'YES']
        upload[['id','TIME','CLEAN','LINKS']].to_sql('fbidname2', conn, if_exists='append')
    if dbw == 'w1':
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt','w+')
        f.truncate()
        f.close()
    elif dbw == 'w2':
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w2.txt','w+')
        f.truncate()
        f.close()
    else:
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w3.txt','w+')
        f.truncate()
        f.close()
    eend = time.time()
    print(eend-starttime)
except:
    if dbw == 'w1':
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt','w+')
        f.truncate()
        f.close()
    elif dbw == 'w2':
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w2.txt','w+')
        f.truncate()
        f.close()
    else:
        f = open('/home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w3.txt','w+')
        f.truncate()
        f.close()
    eend = time.time()
    print(eend-starttime)
    print(dbid,sys.exc_info())
    mydb = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="test",    # 数据库用户名
    passwd="12Q3qeqs,",   # 数据库密码
    database='fbidname'
    )
    sql = "INSERT INTO fbidnamelog (id, page) VALUES (%s, %s)"
    val = (dbid,sys.exc_info)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "INSERT INTO fbidnameerrorlist (id, page) VALUES (%s, %s)"
    val = (dbid,dbpf)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    driver.close()
