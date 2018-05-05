import MonitorCourses as mc
import AS2 as a
from selenium import webdriver
import AutoSelectSinglePro as ass
info1 = a.info_account
info1_1 = a.info_courses

def main(infox, infox_next):
    browser = webdriver.Firefox \
        (executable_path=ass.gk_path)
    browser.get(ass.url)

    while ass.login(browser, infox['account'], infox['password']) == False:
        print 'trying:', infox['account'], infox['password']
        if ass.login(browser, infox['account'], infox['password']):
            break
    while browser.current_url != ass.center:
        browser.get(ass.center)

    course, rank, limit = ass.get_info(browser, infox_next)
    mc.monitor_and_select(browser=browser, course=course,
                          rank=rank, limit=limit)

if __name__ == '__main__':
    m = a.MultiSelect()
    for i in range (0, len(a.info_courses)):
        m.append(main, (a.info_account, a.info_courses[i]))
    m.work()