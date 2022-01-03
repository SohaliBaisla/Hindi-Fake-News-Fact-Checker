import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get("https://www.aajtak.in/fact-check")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

post_elems = browser.find_elements_by_class_name("post-item-title")

for post in post_elems:
    print post.text