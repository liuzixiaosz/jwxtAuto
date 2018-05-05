#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, sys, os, time
from selenium import webdriver, common
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import traceback

url = "http://pms.sustc.edu.cn/"  # 选课系统
home_val = subprocess.Popen("echo $HOME", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)\
    .stdout\
    .readline()\
    .strip()
gk_path = "%s/PycharmProjects/jwxt_auto/auto_sel_course/geckodriver" % home_val
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


def uploadFile(file_path):
    upload = browser.find_element_by_id("file")
    upload.send_keys(file_path)
    Select(browser.find_element_by_name("double")).select_by_value("duphorizontal")

    # logindlg > p:nth-child(3) > button:nth-child(1)
    browser.find_element_by_css_selector("body > form:nth-child(1) > p:nth-child(4) > button:nth-child(1)").click()

    # temp method, should be changed
    time.sleep(5)

    # temp method, should be changed
    browser.get(url)
    # browser.find_element_by_css_selector("button.close:nth-child(1)").click()



if __name__ == '__main__':
    browser = webdriver.Firefox(executable_path=gk_path)  # geckodriver 路径

    account = sys.argv[1]
    password = sys.argv[2]
    browser.get(url)  # enter website
    browser.find_element_by_id("UploadDoc").click()
    login_success = login(browser, account, password)
    if login_success:
        print("登录成功！")
        # upload_menu = browser.find_element_by_css_selector("#UploadDocDlg > iframe:nth-child(2)")
#       a = ActionChains(browser).move_to_element(browser.find_element_by_id("UploadDocDlg"))
        for file in os.listdir(file_dir_path):
            browser.find_element_by_id("UploadDoc").click()
            browser.switch_to.frame(browser.find_element_by_css_selector("html body div#UploadDocDlg.modal iframe"))
            uploadFile(file_dir_path + file)
    else:
        print("登陆失败")