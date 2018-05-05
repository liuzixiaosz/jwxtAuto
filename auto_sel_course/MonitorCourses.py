# -*- coding: utf-8 -*-

import AutoSelectSinglePro as ass
from selenium import webdriver
import time
import traceback
import sys
import os

def monitor_and_select(browser, course, rank=1, limit=False):
    isPublic = False
    cur = browser.current_url
    if cur == ass.url_public:
        isPublic = True
    try:
        if limit == False:
            ass.query(browser, course)
        remains = browser.find_elements_by_class_name ('center')
        # for r in remains:
        #     print r.text
        if isPublic == True:
            index_of_remain = rank * 4 + 1
        else:
            index_of_remain = rank * 3 + 1 #rank - 1 + 1 = remains 前三个是其他的字符
        print course, '监测中...'
        while remains[index_of_remain].text == '0':
            #print 'remaining for %s is %s currently' % (course, remains[index_of_remain].text)
            if limit == False:
                query = browser.find_element_by_xpath('/html/body/div[2]/input[5]') #查询按钮
                query.click()
            else:
                browser.refresh()
            while browser.current_url != cur:
                time.sleep(0.1)
            time.sleep(1.5)
            remains = browser.find_elements_by_class_name ('center')
        selections = browser.find_elements_by_link_text('选课')
        selections[rank - 1].click()
        ass.dealAlerts(browser, 0.25)
        ass.dealAlerts(browser, 0.25)
        os.system('say "HEY YO ! WHATSUP!"')
        print '已进行选课尝试'
    except Exception:
        print traceback.format_exc()
        print traceback.print_last()

def main(argv):
    browser = webdriver.Firefox \
        (executable_path=ass.gk_path)
    account = argv[0]
    password = argv[1]
    browser.get(ass.url)
    while ass.login(browser, account, password) == False:
        if ass.login(browser, account, password):
            break
    browser.get(ass.center)
    while browser.current_url != ass.center:
        browser.get(ass.center)  # 选课中心
    print '登录成功！'
    print '请输入抢课信息，结束信息请按回车'
    print '格式：课程号 选课类别 搜索后出现在选课系统第几行(必修选修无法搜索，直接输入行)\n(jh:本学期计划选课, ' \
          'kj:专业内跨年级选课, kz:跨专业选课, gx:公选课选课, bx:必修选课, xx:选修选课. \n 样例: HUM002 gx 1)'

    courseInfo = raw_input()
    course, rank, limit = ass.get_info(browser, courseInfo)
    monitor_and_select(browser, course=course, rank=rank, limit=limit)

if __name__ == '__main__':
    main(sys.argv[1:])

