from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
# from . import data
from django.template import loader
from bs4 import BeautifulSoup
from .models import Sido, Goo, Carcharger
from customer.models import Bookmark
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver as wd
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# import pyautogui
from bs4 import BeautifulSoup
from datetime import datetime

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re


def add(request):
    input_address = request.GET.get('input_address')
    marker_address = request.GET.get('marker_address')
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(
                command_executor='http://3.38.105.9:32268/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
   
    # driver.close() #메모리 정리

    start = input_address 
    finish = marker_address
    data = []

    load = "로딩 중..."

    #driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    #driver = webdriver.Chrome('chromedriver.exe')

    driver.get('https://map.naver.com/v5/directions/-/-/-/mode?c=14107103.1786139,4494701.9630842,15,0,0,0,dh')

    delay = 3
    driver.implicitly_wait(delay)
    driver.find_element_by_css_selector('div.search_area > ul > li:nth-child(2) > a').click()  
    driver.implicitly_wait(5)  
    driver.find_element_by_id('directionStart0').send_keys(start)
    time.sleep(0.4)
    driver.find_element_by_id('directionStart0').send_keys(Keys.ENTER)
    time.sleep(0.7)
    driver.find_element_by_id('directionGoal1').send_keys(finish)
    time.sleep(0.4)
    driver.find_element_by_id('directionGoal1').send_keys(Keys.ENTER)
    time.sleep(0.5)
    driver.find_element_by_css_selector('directions-search > div.btn_box > button.btn.btn_direction.active').click()
    time.sleep(0.4)    


    driver.find_element_by_css_selector('shrinkable-layout > div > directions-layout > directions-result > div.main >directions-summary-list > directions-hover-scroll > div > div > directions-summary-item-car.item_summary.selected.ng-star-inserted').click()
    #container > shrinkable-layout > div > directions-layout > directions-result > div.main > directions-summary-list > directions-hover-scroll > div > div > directions-summary-item-car.item_summary.selected.ng-star-inserted
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    score_result = soup.find('div', {'class': 'summary_box'})


    km = score_result.find('readable-distance').text
    duration = score_result.find('readable-duration').text
    time.sleep(0.4)
    driver.close()
    
    return JsonResponse({'km' : km, 'duration': duration}, safe=False)

def add2(request):
    input_address1 = request.GET.get('input_address1')
    input_address2 = request.GET.get('input_address2')
    input_car = request.GET.get('input_car')
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Remote(
                command_executor='http://3.38.105.9:32268/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
    
    #driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

    

    start = input_address1
    finish = input_address2
    data = []

    load = "로딩 중..."

    driver.get('https://map.naver.com/v5/directions/-/-/-/mode?c=14107103.1786139,4494701.9630842,15,0,0,0,dh')

    delay = 3
    driver.implicitly_wait(delay)
    driver.find_element_by_css_selector('div.search_area > ul > li:nth-child(2) > a').click()  
    driver.implicitly_wait(5)  
    driver.find_element_by_id('directionStart0').send_keys(start)
    time.sleep(0.4)
    driver.find_element_by_id('directionStart0').send_keys(Keys.ENTER)
    time.sleep(0.7)
    driver.find_element_by_id('directionGoal1').send_keys(finish)
    time.sleep(0.4)
    driver.find_element_by_id('directionGoal1').send_keys(Keys.ENTER)
    time.sleep(0.7)
    driver.find_element_by_css_selector('directions-search > div.btn_box > button.btn.btn_direction.active').click()
    time.sleep(0.4)    

    driver.find_element_by_css_selector('shrinkable-layout > div > directions-layout > directions-result > div.main >directions-summary-list > directions-hover-scroll > div > div > directions-summary-item-car.item_summary.selected.ng-star-inserted').click()
    #container > shrinkable-layout > div > directions-layout > directions-result > div.main > directions-summary-list > directions-hover-scroll > div > div > directions-summary-item-car.item_summary.selected.ng-star-inserted
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    score_result = soup.find('div', {'class': 'summary_box'})

    km2 = score_result.find('readable-distance').text
    km2 = km2[:-2]
    km2 = float(km2)

    if input_car == "기본연비":
        cal_re = ( 255.7 / 5.5 ) * km2
    elif input_car == "현대 코나":
        cal_re = ( 255.7 / 5.6 ) * km2
    elif input_car == "기아 레이":
        cal_re = ( 255.7 / 5.0 ) * km2
    elif input_car == "기아 쏘울":
        cal_re = ( 255.7 / 5.4 ) * km2
    elif input_car == "현대 아이오닉":
        cal_re = ( 255.7 / 6.3 ) * km2
    elif input_car == "쉐보레 볼트":
        cal_re = ( 255.7 / 5.5 ) * km2
    elif input_car == "기아 니로":
        cal_re = ( 255.7 / 5.3 ) * km2
    elif input_car == "르노삼성 SM3Z.E.":
        cal_re = ( 255.7 / 4.5 ) * km2
    elif input_car == "BMW i3":
        cal_re = ( 255.7 / 5.4 ) * km2
    elif input_car == "쉐보레 스파크":
        cal_re = ( 255.7 / 6.0 ) * km2
    elif input_car == "테슬라 모델X":
        cal_re = ( 255.7 / 3.4 ) * km2
    elif input_car == "테슬라 모델SP":
        cal_re = ( 255.7 / 3.8 ) * km2

    cal_re = int(cal_re)

    driver.close()

    return JsonResponse({'cal_re' : cal_re }, safe=False)

def map(request):
    carcharger_list = Carcharger.objects.order_by('id')
    bookmark_list = Bookmark.objects.order_by('id')
    # sido_list = Sido.objects.order_by('sido_name')
    # seoul = Sido.objects.get(id=1)
    # goo_list = Goo.objects.filter(sido=seoul)

    return render(request, 'map/map.html', {'carcharger_list' : carcharger_list, 'bookmark_list' : bookmark_list})

def map_data(request):
    url ='http://apis.data.go.kr/B552584/EvCharger/getChargerInfo?serviceKey=OyKaWBFSrvDw75CVZ%2BZC7RktH7a2hvKgB3OF6HsZge4vAClsqHM5RHPKEML0BsfwB7BCSFv76je4oqqo3uxnMg%3D%3D'
    res = requests.get(url)
    res.encoding = None
    print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    all = soup.select('item')
    chargespot_list = []

    sido_n = request.GET.get('sido')
    goo_n =  request.GET.get('goo')
    search_str = '서울특별시'

    if sido_n or goo_n:
        search_str = sido_n + ' ' + goo_n

    for tag in all:
        if search_str in str(tag.select_one('addr').text):
            chargespot = {"statNm" : "" , "address" : "","lat" : "" , "lng" : "", "chger_id" : "" ,
                         "chger_type" : "", "use_time" : "", "busi_nm": "", "busi_call" : "",
                         "stat" : "" }
            chargespot["statNm"] = str(tag.select_one('statNm').text)
            chargespot["address"] = str(tag.select_one('addr').text)
            chargespot["lat"] = str(tag.select_one('lat').text)
            chargespot["lng"] = str(tag.select_one('lng').text)
            chargespot["chger_id"] = str(tag.select_one('chgerId').text)
            chargespot["chagertype"] = str(tag.select_one('chgerType').text)
            chargespot["use_time"] = str(tag.select_one('useTime').text)
            chargespot["busi_nm"] = str(tag.select_one('busiNm').text)
            chargespot["busi_call"] = str(tag.select_one('busiCall').text)
            
            #충전기 상태 입력
            if str(tag.select_one('stat').text) == '1':
                chargespot["stat"] = "통신이상"
            elif str(tag.select_one('stat').text) == '2':
                chargespot["stat"] = "충전대기"
            elif str(tag.select_one('stat').text) == '3':
                chargespot["stat"] = "충전중"
            elif str(tag.select_one('stat').text) == '4':
                chargespot["stat"] = "운영중지"
            elif str(tag.select_one('stat').text) == '5':
                chargespot["stat"] = "점검중"
            else:
                chargespot["stat"] = "상태미확인"
            chargespot["power_type"] = str(tag.select_one('output').text)
            chargespot_list.append(chargespot)

    return JsonResponse(chargespot_list, safe=False)

def index(request):
    # data_list = get_html()
    # return render(request,'map/index.html', {'data_list':data_list})
    return render(request,'map/index.html')

def test(request):
    return render(request,'map/test.html')

import requests

def get_html(url):
    html = ''
    res= requests.get(url)
    if res.status_code == 200:
        res.encoding = None
        html = res.text
    return html

def Crawling(request):
    search_keyword = '전기자동차'
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_keyword}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('ul',{'class' : 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]

    count = 0
    data_list = []
    for n in a_list:

        title = n.get('title')
        link = n.get('href')

        if title:
            data = {'text':title, 'link':link}
            data_list.append(data)
        count += 1
        if count >= 8:
               break
    print(data_list)
    return render(request,'map/index.html', {'data_list':data_list})





