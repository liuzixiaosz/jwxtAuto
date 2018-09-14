#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium import common
import time, subprocess, sys, os

url = 'http://jwxt.sustc.edu.cn/jsxsd/'  # 选课系统
abs_path = os.path.abspath('.')
driver_path = abs_path + os.sep + "geckodriver"
info_path = abs_path + os.sep + "courseInfo.txt"

url_multimajor = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInFawxk'  # 跨专业选课
url_multigrade = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInKnjxk'  # 专业内跨年级选课
url_public = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk'  # 公选课选课
url_optional = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInXxxk' #选修选课
url_repulsory = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInBxxk' #必修选课
url_plan = 'http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk' #计划选课
url_map = {'bx': url_repulsory,'xx': url_optional,'kj': url_multigrade,
           'kz': url_multimajor, 'gx': url_public, 'jh': url_plan}
center = 'http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=D102885918754CD79C2E3F167A288A11'

def dealAlerts(browser, sleeptime, loop=5):
    if loop == 0:
        return
    time.sleep(sleeptime)
    try:
        browser.switch_to.alert.accept()  # 确认选课
    except common.exceptions.NoAlertPresentException:
        dealAlerts(browser, sleeptime, loop=loop - 1)

def query(browser, course):
    course_box = browser.find_element(value='kcxx')  # 课程查询box
    course_box.clear()
    course_box.send_keys(course)
    query = browser.find_element_by_xpath('/html/body/div[2]/input[5]')  # 查询按钮
    query.click()

def select(browser, course, rank=1, loop=5, limit=False):

    if loop == 0:
        return
    try:
        if limit == False:
            query(browser, course)
        selections = browser.find_elements_by_link_text('选课')
        selections[rank - 1].click()
        dealAlerts(browser, 0.25)
        dealAlerts(browser, 0.25)

    except Exception:
        time.sleep(0.2)
        select(browser, course, rank=rank, loop=loop - 1, limit=limit)


def login(browser, username, password):
    try:
        username_box = browser.find_element_by_id('username')
        username_box.send_keys(username)
        password_box = browser.find_element_by_id('password')
        password_box.send_keys(password)
        submit_btn = browser.find_element_by_name('submit')
        submit_btn.click()
        return True
    except common.exceptions.NoSuchElementException:
        print common.exceptions.NoSuchElementException
        return False

def get_info(browser, courseInfo):
    c = courseInfo.strip().split(' ')
    browser.get(url_map[c[1]])
    if c[1] == 'xx' or c[1] == 'bx':
        limit = True
    else:
        limit = False
    return c[0], int(c[2]), limit

def get_info_and_select(browser, courseInfo):
    course, rank, limit = get_info(browser, courseInfo)
    select(browser, course=course, rank=rank,limit=limit)

def main(argv):
    browser = webdriver.Firefox(executable_path=driver_path)  #driver 路径
    browser.get(url)  # enter website
    account = argv[0]
    password = argv[1]
    courseArr = []
    while login(browser, account, password) == False:
        if login(browser, account, password):
            break
    while browser.current_url != center:
        browser.get(center)  # 选课中心
    print '登录成功！'
    print '读取成功'
    #print '格式：课程号 选课类别 搜索后出现在选课系统第几行\n(bx:必修选课, xx:选修选课, jh:本学期计划选课, ' \
          #'kj:专业内跨年级选课, kz:跨专业选课, gx:公选课选课. \n 样例: HUM002 gx 1)'

    courseArr = open(info_path, "r").readlines()
    
    while time.localtime().tm_min == 59:
        if time.localtime().tm_sec == 0:  # waiting when now is 12:59:xx, when now comes to 13:00, break waiting
            break

    browser.get(center)
    for ca in courseArr:
        get_info_and_select(browser, ca)

if __name__ == '__main__':
    main(sys.argv[1:])


