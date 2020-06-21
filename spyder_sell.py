#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib3
import re
import requests
import time
import pandas as pd
from pandas import Series, DataFrame
from file import File
from send_wechat_message import send_message
#URL（ここにURLを入れてください）
url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13101&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1'
main_url='https://suumo.jp/chukoikkodate/tokyo/city/'
domain = 'https://suumo.jp'
names = []
addresses = []
locations = []
land_spaces = []
building_spaces = []
floor_planses = []
biuild_date = []
detail_urls = []
tels = []


def each_page(single_page_url, houses=None):
    if not houses:
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "lxml")
        summary = soup.find("div", {'id': 'js-bukkenList'})
        houses = summary.find_all(
            "div", {'class': 'property_unit-content'})
 

    for house in houses:

        house_title = house.find('h2', class_='property_unit-title').find('a')
        name = house_title.text
        detail_url = house_title['href']
        house_detail = house.find('div', class_='dottable dottable--cassette')
        house_price = house_detail.find('span', class_='dottable-value').text

        house_locate_detail = house_detail.find_all(
            'div', class_='dottable-line')
        address = house_locate_detail[1].find_all('dd')[0].text
        location = house_locate_detail[1].find_all('dd')[1].text

        house_detail_in = house_detail.find_all('table')
        land_space = house_detail_in[0].find_all('dd')[0].text
        building_space = house_detail_in[1].find_all('dd')[0].text
        floor_plans = house_detail_in[0].find_all('dd')[1].text
        biuild_date = house_detail_in[1].find_all('dd')[1].text
        tel = house.find('span', class_='makermore-tel-txt').text

        names.append(name)
        addresses.append(address)
        locations.append(location)
        land_spaces.append(land_space)
        building_spaces.append(building_space)
        floor_planses.append(floor_plans)
        detail_urls.append(domain+detail_url)
        tels.append(tel)


def main(area, url):
    result = requests.get(url)
    c = result.content

    soup = BeautifulSoup(c, "lxml")

    summary = soup.find("div",{'id':'js-bukkenList'})
    body = soup.find("body")
    pages = body.find_all("div",{'class':'pagination pagination_set-nav'})
    
    return pages
    if len(pages)==2:
        each_page('', houses=None)
    else:







    #pages:翻页导航按钮
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    pages_split0 = pages_split[0]
    pages_split1 = pages_split0[-3:]
    pages_split2 = pages_split1.replace('>','')
    pages_split3 = int(pages_split2)

    urls = []

    urls.append(url)

    for i in range(pages_split3-1):
        pg = str(i+2)
        url_page = url + '&page=' + pg
        urls.append(url_page)

    names = [] 
    addresses = [] 
    locations0 = [] 
    locations1 = [] 
    locations2 = [] 
    ages = [] 
    heights = [] 
    floors = []
    rent = [] 
    admin = []
    others = [] 
    floor_plans = [] 
    areas = []
    detail_urls = [] 

    for url in urls:
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "lxml")
        summary = soup.find("div",{'id':'js-bukkenList'})
        houses = summary.find_all(
            "div", {'class': 'property_unit-content'})

        for house in houses:

            #room_number = len(house.find_all('tbody'))

            name = house.find('div', class_='property_unit-title"').text
            address = house.find(
                'li', class_='cassetteitem_detail-col1').text

            #for i in range(room_number):
            #    names.append(name)
            #    addresses.append(address)

            sublocation = house.find(
                'li', class_='cassetteitem_detail-col2')
            cols = sublocation.find_all('div')
            for i in range(len(cols)):
                text = cols[i].find(text=True)
                for j in range(room_number):
                    if i == 0:
                        locations0.append(text)
                    elif i == 1:
                        locations1.append(text)
                    elif i == 2:
                        locations2.append(text)

            age_and_height = house.find(
                'li', class_='cassetteitem_detail-col3')
            age = age_and_height('div')[0].text
            height = age_and_height('div')[1].text

            for i in range(room_number):
                ages.append(age)
                heights.append(height)

            table = house.find('table')
            rows = []
            rows.append(table.find_all('tr'))

            data = []
            for row in rows:
                for tr in row:
                    cols = tr.find_all('td')
                    if len(cols) != 0:
                        _floor = cols[2].text
                        _floor = re.sub('[\r\n\t]', '', _floor)

                        _rent_cell = cols[3].find('ul').find_all('li')
                        _rent = _rent_cell[0].find('span').text
                        _admin = _rent_cell[1].find('span').text

                        _deposit_cell = cols[4].find('ul').find_all('li')
                        _deposit = _deposit_cell[0].find('span').text
                        _reikin = _deposit_cell[1].find('span').text
                        _others = _deposit + '/' + _reikin

                        _floor_cell = cols[5].find('ul').find_all('li')
                        _floor_plan = _floor_cell[0].find('span').text
                        _area = _floor_cell[1].find('span').text

                        _detail_url = cols[8].find('a')['href']
                        _detail_url = 'https://suumo.jp' + _detail_url

                        text = [_floor, _rent, _admin, _others, _floor_plan, _area, _detail_url]
                        data.append(text)

            for row in data:
                floors.append(row[0])
                rent.append(row[1])
                admin.append(row[2])
                others.append(row[3])
                floor_plans.append(row[4])
                areas.append(row[5])
                detail_urls.append(row[6])


            time.sleep(3)

    names = Series(names)
    addresses = Series(addresses)
    locations0 = Series(locations0)
    locations1 = Series(locations1)
    locations2 = Series(locations2)
    ages = Series(ages)
    heights = Series(heights)
    floors = Series(floors)
    rent = Series(rent)
    admin = Series(admin)
    others = Series(others)
    floor_plans = Series(floor_plans)
    areas = Series(areas)
    detail_urls = Series(detail_urls)

    suumo_df = pd.concat([names, addresses, locations0, locations1, locations2, ages, heights, floors, rent, admin, others, floor_plans, areas, detail_urls], axis=1)

    suumo_df.columns = ['マンション名','住所','立地1','立地2','立地3','築年数','建物の高さ','階層','賃料料','管理費', '敷/礼/保証/敷引/償却','間取り','専有面積', '詳細URL']

    suumo_df.to_csv(area + 'suumo.csv', encoding='utf-16', header=True, index=False)
area_url_json=File('area_url.json').load_file()
for (area, url) in area_url_json['rental'].items():
    main(area, url)
    time.sleep(5)
send_message('grep rental finished')
