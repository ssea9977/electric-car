from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import time
from datetime import datetime
 
start = "송천고"
finish = "소래포구역"
data = []

driver = webdriver.Chrome(executable_path='chromedriver.exe')


# driver.close() #메모리 정리
    
start = "송천고"
finish = "소래포구역"
data = []


driver.get('https://map.naver.com/v5/directions/-/-/-/mode?c=14107103.1786139,4494701.9630842,15,0,0,0,dh')

delay = 3
driver.implicitly_wait(delay)
driver.find_element_by_css_selector('div.search_area > ul > li:nth-child(2) > a').click()  
driver.implicitly_wait(5)  
pyautogui.press('enter')
driver.find_element_by_id('directionStart0').send_keys(start)
time.sleep(0.3)
pyautogui.press('enter')
time.sleep(0.3)
driver.find_element_by_id('directionGoal1').send_keys(finish)
time.sleep(0.02)
pyautogui.press('enter')
time.sleep(0.3)
driver.find_element_by_css_selector('directions-result > div > directions-search > div.btn_box > button.btn.btn_direction.active').click() 
time.sleep(0.4)    

driver.find_element_by_css_selector('shrinkable-layout > div > directions-layout > directions-result > directions-summary-list > directions-hover-scroll > div > div > directions-summary-item-car.item_summary.selected.ng-star-inserted').click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
score_result = soup.find('div', {'class': 'summary_box'})

km2 = score_result.find('readable-distance').text

km2 = km2[:-2]
km2 = float(km2)

print(km2)
