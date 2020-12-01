from datetime import datetime
from time import sleep
import webbrowser
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LogIn:

    def __init__(self, headless=True):
        super(LogIn, self).__init__()

        options = webdriver.ChromeOptions()
        if headless is True:
            options.add_argument("--headless")
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            # options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)

        self.driver.get('http://adservio.ro')
        self.driver.implicitly_wait(2)

        try:
            self.driver.delete_all_cookies()
            self.driver.implicitly_wait(2)

            cookies = pickle.load(open('cookies.txt', 'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.driver.implicitly_wait(2)

            print('Enstablished connection to account.')

        except FileNotFoundError:

            print("Your log in credentials have expired or are missing,",
                  "please enter them.")

            mail = 'alexandru.merila@gmail.com'
            pwd = 'vgjdbQ4BaaoFsL%'  # change after GitHub push

            adress = self.driver.find_element_by_css_selector(
                '.label_margin_bottom > input:nth-child(3)')
            adress.send_keys(mail)
            adress.send_keys(Keys.RETURN)
            self.driver.implicitly_wait(2)

            passwd = self.driver.find_element_by_css_selector(
                '.label_margin_bottom > input:nth-child(4)')
            passwd.send_keys(pwd)
            self.driver.implicitly_wait(2)
            passwd.send_keys(Keys.RETURN)
            self.driver.implicitly_wait(2)
            sleep(5)

            pickle.dump(self.driver.get_cookies(), open('cookies.txt', 'wb'))

        self.joined = False
        self.join(5)

    def join(self, delay=0):

        self.driver.get("https://www.adservio.ro/ro/messages")
        self.driver.implicitly_wait(2)
        sleep(1)

        links = []
        for a in self.driver.find_elements_by_xpath('.//a'):
            link = a.get_attribute('href')
            if '/received/' in link:
                links.append(link)

        for link in links:
            btn = None
            self.driver.get(link)
            sleep(1)

            for a in self.driver.find_elements_by_xpath('.//a'):
                if '/zoom.us/' in a.get_attribute('href'):
                    btn = a.get_attribute('href')
            if btn is not None:
                print(btn, link)
                break

        divs = self.driver.find_element_by_tag_name('div')
        time_sent = divs.text.split('\n')[4]

        # test vars
        time_sent = '13:15'
        if len(time_sent) != 5:
            print('Error, no meeting found today.')
            exit()

        time_sent = int(time_sent[-2:].lstrip('0'))
        curr_time = datetime.now().minute

        if curr_time > time_sent and self.joined is False:
            webbrowser.open_new_tab(btn)
            self.joined = True
            print('Joined a meeting')

        elif curr_time > time_sent and self.joined is True:
            print(f'Waiting until {datetime.now().hour + 1}:{15 + delay}.')
            sleep(60 * ((75 + delay) - curr_time))
            self.joined = False

        else:
            print('No meeting found, trying again...')
            sleep(30)
            self.driver.back()

        self.join()


ex = LogIn()
