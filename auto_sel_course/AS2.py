import AutoSelectSinglePro as ass
import multiprocessing
from selenium import webdriver

info_account = {'account': '', 'password': ''}

info_courses = ['', '']

class MultiSelect():
    def __init__(self):
        self.set=[]
    def append(self, target, args):
        this_process = multiprocessing.Process(target=target, args=args)
        self.set.append(this_process)
    def work(self):
        for s in self.set:
            s.start()
        for s in self.set:
            s.join()

def main(infox, infox_next):
    print infox_next
    browser = webdriver.Firefox \
        (executable_path=ass.gk_path)
    browser.get(ass.url)
    while ass.login(browser, infox['account'], infox['password']) == False:
        print 'trying:', infox['account'], infox['password']
        if ass.login(browser, infox['account'], infox['password']):
            break
    while browser.current_url != ass.center:
        browser.get(ass.center)
    for info in infox_next:
        print info
        ass.get_info_and_select(browser, info)
if __name__ == '__main__':

    m = MultiSelect()

    m.append(main, (info_account, info_courses))
    m.work()
