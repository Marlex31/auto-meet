from datetime import datetime
from time import sleep
import webbrowser
import pickle
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier


class LogIn:
    """
    Accesses the site by using the selenium webdriver, attemps to log in with
    cookies or promps user to log in and then locally saves the cookies for
    future sessions.
    """

    def __init__(self, headless=True, mail=None, pwd=None):
        """
        :param headless: debug purposes, shows/hides the webdriver window
        :type headless: (bool)
        :param mail: mail used for log in
        :type mail: (str)
        :param pwd: password used for log in
        :type pwd: (str)

        """
        super(LogIn, self).__init__()

        options = webdriver.ChromeOptions()
        if headless is True:
            options.add_argument("--headless")
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)

        self.driver.get('http://adservio.ro')
        self.driver.implicitly_wait(2)

        try:
            cookies = pickle.load(open('cookies.txt', 'rb'))
            self.driver.delete_all_cookies()
            self.driver.implicitly_wait(2)

            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.driver.implicitly_wait(2)

        except FileNotFoundError:

            if mail is not None or pwd is not None:
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

                pickle.dump(self.driver.get_cookies(),
                            open('cookies.txt', 'wb'))

        self.joined = False

    def join(self, delay=0):

        """
        Scrapes the "messages" page for a valid Zoom link, while
        comparing current time and the time the meeting was sent,
        therefore only joining recent meeting. The bool chain returns
        the amount of seconds that the thread has to sleep until becoming
        active again and searching for a meeting.

        :param delay: time in seconds to delay the meeting join
        :type delay: (int)
        """

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
                # print(btn, link)
                break

        tags = self.driver.find_elements_by_tag_name('span')
        pattern = r'^(\d)\s|\s(\d\d)\s'  # \s(\d?\d)\s
        for tag in tags:
            match = re.search(pattern, tag.text)
            if match is not None:
                time_sent = int(match.group())
                break

        if match is None:
            print('> No meeting found, trying again.')
            return 60

        # print(time_sent)
        curr_time = datetime.now().minute

        if curr_time > time_sent and self.joined is False:

            toaster = ToastNotifier()
            toaster.show_toast("Meeting Automation",
                               "Joining a meeting...",
                               duration=3)

            print('> Joined a meeting.')
            webbrowser.open_new_tab(btn)
            self.joined = True
            return 0

        elif curr_time > time_sent and self.joined is True:
            print(f'> Waiting until {datetime.now().hour + 1}:{15 + delay}.')
            self.joined = False
            return 60 * ((75 + delay) - curr_time)

        elif curr_time < 15:
            print('> Waiting until the first quarter.')
            return 60 * (15 - curr_time)

        else:
            print('> No meeting found, trying again...')
            return 30
