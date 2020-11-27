import webbrowser
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


mail = 'alexandru.merila@gmail.com'
pwd = 'vgjdbQ4BaaoFsL%'

# options = webdriver.ChromeOptions()
# options.add_argument("--headless")

driver = webdriver.Chrome()
driver.get("http://adservio.ro")
sleep(2)
driver.refresh()
sleep(2)

# adress = driver.find_element_by_css_selector(
#     '.label_margin_bottom > input:nth-child(3)')
# adress.send_keys(mail)
# adress.send_keys(Keys.RETURN)
# sleep(2)

# passwd = driver.find_element_by_css_selector(
#     '.label_margin_bottom > input:nth-child(4)')
# passwd.send_keys(pwd)
# passwd.send_keys(Keys.RETURN)
# sleep(2)

# driver.get("http://adservio.ro/ro/messages")
# sleep(1)

# for a in driver.find_elements_by_xpath('.//a'):
#     if '/received/' in a.get_attribute('href'):
#         link = a.get_attribute('href')
#         break

# driver.get(link)
# sleep(2)

# divs = driver.find_element_by_tag_name('div')
# time_sent = divs[4]


# for a in driver.find_elements_by_xpath('.//a'):
#     if '/zoom.us/' in a.get_attribute('href'):
#         btn = a.get_attribute('href')
#         break

driver.close()

# webbrowser.open_new_tab(btn)
