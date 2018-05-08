#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, sys, os, time
from selenium import webdriver, common
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import traceback

url = "http://pms.sustc.edu.cn/"
home_val = subprocess.Popen("echo $HOME", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)\
    .stdout\
    .readline()\
    .strip()
gk_path = "%s/Desktop/scripts/geckodriver" % home_val
file_dir_path = "%s/Desktop/need_to_print/" % home_val


def login(browser, username, password):
    try:
        username_box = browser.find_element_by_id("username")
        username_box.send_keys(username)
        password_box = browser.find_element_by_id("password")
        password_box.send_keys(password)
        submit_btn = browser.find_element_by_css_selector("#logindlg > p:nth-child(3) > button:nth-child(1)")
        submit_btn.click()
        return True
    except common.exceptions.NoSuchElementException:
        print(common.exceptions.NoSuchElementException)
        return False
    except Exception:
        print(traceback.print_exc())
        return False


def dealBusy(wait_loop):
    try:
        browser.find_element_by_css_selector("#msgdlg > p:nth-child(2) > button").click()
    except Exception:
        time.sleep(5)
        if wait_loop > 120:
            return
        dealBusy(wait_loop + 1)

def uploadFile(file_path):
    upload = browser.find_element_by_id("file")

    upload.send_keys(file_path)
    Select(browser.find_element_by_name("double")).select_by_value("duphorizontal")

    # logindlg > p:nth-child(3) > button:nth-child(1)
    browser.find_element_by_css_selector("body > form:nth-child(1) > p:nth-child(4) > button:nth-child(1)").click()

    time.sleep(10)
    #dealBusy(0);

    browser.get(url)
    # browser.find_element_by_css_selector("button.close:nth-child(1)").click()



if __name__ == '__main__':
    browser = webdriver.Firefox(executable_path=gk_path)  # geckodriver 路径
    browser.get(url)  # enter website
    login_success = False
    account = sys.argv[1]
    password = sys.argv[2]
    browser.find_element_by_id("UploadDoc").click()
    time.sleep(1)
    login_success = login(browser, account, password)
    if login_success:
        print("登录成功！")
        browser.get(url)
        # upload_menu = browser.find_element_by_css_selector("#UploadDocDlg > iframe:nth-child(2)")
#       a = ActionChains(browser).move_to_element(browser.find_element_by_id("UploadDocDlg"))
        for file in os.listdir(file_dir_path):
            print("uploading %s..." % file)
            browser.find_element_by_id("UploadDoc").click()
            time.sleep(2)
            browser.switch_to.frame(browser.find_element_by_css_selector("html body div#UploadDocDlg.modal iframe"))
            uploadFile(file_dir_path + file)
    else:
        print("登陆失败")
