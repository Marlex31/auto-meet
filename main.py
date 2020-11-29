import webbrowser
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


mail = 'alexandru.merila@gmail.com'
pwd = 'vgjdbQ4BaaoFsL%'


class LogIn:

    def __init__(self, mail, pwd, headless=True):
        super(LogIn, self).__init__()

        self.mail = mail
        self.pwd = pwd

        options = webdriver.ChromeOptions()
        if headless is True:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://adservio.ro")

        adress = self.driver.find_element_by_css_selector(
            '.label_margin_bottom > input:nth-child(3)')
        adress.send_keys(self.mail)
        adress.send_keys(Keys.RETURN)
        sleep(2)

        passwd = self.driver.find_element_by_css_selector(
            '.label_margin_bottom > input:nth-child(4)')
        passwd.send_keys(self.pwd)
        passwd.send_keys(Keys.RETURN)
        sleep(2)

        self.driver.get("http://adservio.ro/ro/messages")
        sleep(1)

        self.join()

    def join(self):

        for a in self.driver.find_elements_by_xpath('.//a'):
            link = a.get_attribute('href')
            if '/received/' in link:
                break
        self.driver.get(link)
        sleep(2)

        divs = self.driver.find_element_by_tag_name('div')
        time_sent = divs.text.split('\n')[4]

        # test vars
        time_sent = '13:15'
        if len(time_sent) != 5:
            print('Error, no meeting found today.')
            exit()

        time_sent = int(time_sent[-2:].lstrip('0'))
        curr_time = datetime.now().minute

        if curr_time > time_sent:
            for a in self.driver.find_elements_by_xpath('.//a'):
                if '/zoom.us/' in a.get_attribute('href'):
                    btn = a.get_attribute('href')
                    break

            webbrowser.open_new_tab(btn)
            self.driver.close()

        else:
            print('No meeting found, trying again...')
            self.driver.implicitly_wait(30)
            self.driver.back()
            self.join()


ex = LogIn(mail, pwd)
