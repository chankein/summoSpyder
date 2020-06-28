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
#url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13101&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1'
#nerima_url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13101&sc=13120&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1'
#main_url='https://suumo.jp/chukoikkodate/tokyo/city/'
domain = 'https://suumo.jp'

area_url_json = File('area_url.json').load_file()

prifix_file = '_old_house.csv'


class HouseArea:
    def __init__(self, area):
        self.main_url = domain + area_url_json['secondHandHouse'][area]
        self.file_name = area + prifix_file
        self.suumo_df_list = []

    def each_page(self, single_page_url):
        result = requests.get(single_page_url)
        c = result.content
        self.soup = BeautifulSoup(c, "lxml")
        self.summary = self.soup.find("div", {'id': 'js-bukkenList'})
        self.houses = self.summary.find_all(
            "div", {'class': 'property_unit-content'})
        if len(self.suumo_df_list)==0:
            body = self.soup.find("body")
            pages = body.find_all(
                "div", {'class': 'pagination pagination_set-nav'})
            self.next_pages = pages[0].find_all('a')
        else:
            pass
        names = []
        house_prices = []
        addresses = []
        locations = []
        land_spaces = []
        building_spaces = []
        floor_planses = []
        biuild_date = []
        detail_urls = []
        tels = []

        for house in self.houses:

            house_title = house.find('h2', class_='property_unit-title').find('a')
            name = house_title.text
            detail_url = house_title['href']
            house_detail = house.find('div', class_='dottable dottable--cassette')
            house_price = house_detail.find('span', class_='dottable-value').text

            house_locate_detail = house_detail.find_all(
                'div', class_='dottable-line')[1].find_all('dd')

            address = house_locate_detail[0].text
            if len(house_locate_detail) == 1:
                print(house_locate_detail[0].text)
                location = ''
            else:
                location = house_locate_detail[1].text

            house_detail_in = house_detail.find_all('table')
            land_space = house_detail_in[0].find_all('dd')[0].text
            building_space = house_detail_in[1].find_all('dd')[0].text
            floor_plans = house_detail_in[0].find_all('dd')[1].text
            biuild_date = house_detail_in[1].find_all('dd')[1].text
            if house.find('span', class_='makermore-tel-txt'):
                tel = house.find('span', class_='makermore-tel-txt').text
            else:
                tel=''
            names.append(name)
            addresses.append(address)
            locations.append(location)
            land_spaces.append(land_space)
            building_spaces.append(building_space)
            floor_planses.append(floor_plans)
            detail_urls.append(domain+detail_url)
            tels.append(tel)
        
        names = Series(names)
        house_prices = Series(house_prices)
        addresses = Series(addresses)
        locations = Series(locations)
        land_spaces = Series(land_spaces)
        building_spaces = Series(building_spaces)
        floor_planses = Series(floor_planses)
        biuild_date = Series(biuild_date)
        detail_urls = Series(detail_urls)
        tels = Series(tels)
        suumo_df_pages = pd.concat([names, house_prices, addresses, locations, land_spaces, building_spaces, floor_planses,
                            biuild_date, detail_urls, tels], axis=1)
        suumo_df_pages.columns = ['マンション名', '販売価格', '住所', '立地', '土地面積',
                                '建物面積',  '間取り', '築年月', '詳細URL', '電話']
        self.suumo_df_list.append(suumo_df_pages)
        #return suumo_df_pages



    # def main(area):
    #     url = domain + area_url_json['secondHandHouse'][area]
    #     suumo_df_list = []
    #     result = requests.get(url)
    #     c = result.content

    #     soup = BeautifulSoup(c, "lxml")

    #     summary = soup.find("div",{'id':'js-bukkenList'})
    #     houses = summary.find_all(
    #         "div", {'class': 'property_unit-content'})

    #     suumo_df_list.append(each_page('', houses))

    #     body = soup.find("body")
    #     pages = body.find_all("div",{'class':'pagination pagination_set-nav'})

    #     next_pages=pages[0].find_all('a')

    #     if len(next_pages) == 0:
    #         pass
    #     else:
    #         max_pages = int(next_pages[-2].text)
    #         for x in range(2, max_pages+1):
    #             pages_url = url + 'pnz1{}.html'.format(str(x))
    #             suumo_df_list.append(each_page(pages_url, houses=None))
    #             time.sleep(3)
    #     suumo_df = pd.concat(suumo_df_list)

    #     suumo_df.to_csv(area + '_old_house.csv', encoding='utf-16', header=True, index=False)


if __name__=='__main__':
    for (area, url) in area_url_json['secondHandHouse'].items():
        AREACLASS = HouseArea(area)
        AREACLASS.each_page(AREACLASS.main_url)
        if AREACLASS.next_pages:
            if len(AREACLASS.next_pages) == 0:
                pass
            else:
                max_pages = int(AREACLASS.next_pages[-2].text)
                for x in range(2, max_pages+1):
                    pages_url = AREACLASS.main_url + \
                        'pnz1{}.html'.format(str(x))
                    
                    time.sleep(3)
        suumo_df = pd.concat(AREACLASS.suumo_df_list)

        suumo_df.to_csv(area + '_old_house.csv', encoding='utf-16', header=True, index=False)


#main('千代田区', 'https://suumo.jp/chukoikkodate/tokyo/sc_chiyoda/')
#for (area, url) in area_url_json['secondHandHouse'].items():
    #try:
#    main(area, (domain+url))
#    time.sleep(5)
    #except Exception:
    #    pass
    #    send_message(area+' failed')

#send_message('grep sell old houses finished')
