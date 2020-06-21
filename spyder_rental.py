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
#url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC031/?ar=030&ta=13&bs=040&smk=n01&cinsc=134&tm=035&tmkbn=1'
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&pc=50'

result_dict={}

def main(area, url):
    result = requests.get(url)
    c = result.content

    soup = BeautifulSoup(c, "lxml")

    summary = soup.find("div",{'id':'js-bukkenList'})
    body = soup.find("body")
    pages = body.find_all("div",{'class':'pagination pagination_set-nav'})
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
        apartments = summary.find_all("div",{'class':'cassetteitem'})

        for apartment in apartments:

            room_number = len(apartment.find_all('tbody'))

            name = apartment.find('div', class_='cassetteitem_content-title').text
            address = apartment.find('li', class_='cassetteitem_detail-col1').text

            for i in range(room_number):
                names.append(name)
                addresses.append(address)

            sublocation = apartment.find('li', class_='cassetteitem_detail-col2')
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

            age_and_height = apartment.find('li', class_='cassetteitem_detail-col3')
            age = age_and_height('div')[0].text
            height = age_and_height('div')[1].text

            for i in range(room_number):
                ages.append(age)
                heights.append(height)

            table = apartment.find('table')
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
    try:
        main(area, url)
        result_dict['area'] = 'done'
        time.sleep(5)
    except:
        result_dict['area'] = 'fail'

send_message('grep rental finished' + str(result_dict))
