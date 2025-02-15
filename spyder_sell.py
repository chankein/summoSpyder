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
from utils import deal_price, deal_build_years, readConf
import time
import datetime
#URL（ここにURLを入れてください）
#url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13101&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1'
#nerima_url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=021&ta=13&jspIdFlg=patternShikugun&sc=13101&sc=13120&kb=1&kt=9999999&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1'
#main_url='https://suumo.jp/chukoikkodate/tokyo/city/'
domain = 'https://suumo.jp'

area_url_json = File('/home/ubuntu/summoSpyder/area_url.json').load_file()

prifix_file = '_old_house.csv'
debug = 0
conf,hostname = readConf()
s3_home = conf.get(hostname, "s3_home")
csv_path = s3_home + 'old_house.csv'
#print(csv_path)

class HouseArea:
    def __init__(self, area):
        self.main_url = domain + area_url_json['secondHandHouse'][area]
        self.file_name = area + prifix_file
        self.suumo_df_list = []

    def each_page(self, single_page_url):
        result = requests.get(single_page_url)
        c = result.content
        soup = BeautifulSoup(c, "lxml")
        self.summary = soup.find("div", {'id': 'js-bukkenList'})
        houses = self.summary.find_all(
            "div", {'class': 'property_unit-content'})
        if len(self.suumo_df_list) == 0:
            body = soup.find("body")
            pages = body.find_all(
                "div", {'class': 'pagination pagination_set-nav'})
            self.next_pages = pages[0].find_all('a')
        else:
            pass
        names = []
        house_prices = []
        house_prices_nums = []
        addresses = []
        locations = []
        land_spaces = []
        building_spaces = []
        floor_planses = []
        biuild_dates = []
        biuild_ages = []
        detail_urls = []
        tels = []

        for house in houses:
            name = ''
            house_price = ''
            house_prices_num = 0
            address = ''
            location = ''
            land_space = ''
            building_space = ''
            floor_plans = ''
            biuild_date = ''
            biuild_age = ''
            detail_url = ''
            tel = ''

            house_title = house.find(
                'h2', class_='property_unit-title').find('a')
            name = house_title.text.replace('\n', '')
            detail_url = house_title['href']
            house_detail = house.find(
                'div', class_='dottable dottable--cassette')
            tables = house_detail.find_all('dl')
            for table in tables:
                this_title = table.find('dt').text
                this_value = table.find('dd').text
                if '販売価格' in this_title:
                    house_price = this_value.replace('\n', '')
                    try:
                        house_prices_num = deal_price(house_price)
                    except:
                        pass
                elif '所在地' in this_title:
                    address = this_value.replace('\n', '')
                elif '沿線・駅' in this_title:
                    location = this_value.replace('\n', '')
                elif '土地面積' in this_title:
                    land_space = this_value.replace('\n', '')
                elif '間取り' in this_title:
                    floor_plans = this_value.replace('\n', '')
                elif '建物面積' in this_title:
                    building_space = this_value.replace('\n', '')
                elif '築年月' in this_title:
                    biuild_date = this_value.replace('\n', '')
                    biuild_age = deal_build_years(biuild_date)
                else:
                    pass
            if house.find('span', class_='makermore-tel-txt'):
                tel = house.find('span', class_='makermore-tel-txt').text
            else:
                tel = ''
            names.append(name)
            house_prices.append(house_price)
            house_prices_nums.append(house_prices_num)
            addresses.append(address)
            locations.append(location)
            land_spaces.append(land_space)
            building_spaces.append(building_space)
            floor_planses.append(floor_plans)
            biuild_dates.append(biuild_date)
            biuild_ages.append(biuild_age)
            detail_urls.append(domain+detail_url)
            tels.append(tel)
            if debug == 1:
                print('name= '+name)
                print('house_prices= '+house_price)
                print('addresses= '+address)
                print('locations= '+location)
                print('land_spaces= '+land_space)
                print('building_spaces= '+building_space)
                print('floor_planses= '+floor_plans)
                print('biuild_date= '+biuild_date)
                print('tels= '+tel)

        names = Series(names)
        house_prices = Series(house_prices)
        house_prices_nums = Series(house_prices_nums)
        addresses = Series(addresses)
        locations = Series(locations)
        land_spaces = Series(land_spaces)
        building_spaces = Series(building_spaces)
        floor_planses = Series(floor_planses)
        biuild_dates = Series(biuild_dates)
        biuild_ages = Series(biuild_ages)
        detail_urls = Series(detail_urls)
        tels = Series(tels)
        suumo_df_pages = pd.concat([names, house_prices, house_prices_nums, addresses, locations, land_spaces, building_spaces, floor_planses,
                                    biuild_dates, biuild_ages, detail_urls, tels], axis=1)
        suumo_df_pages.columns = ['マンション名', '販売価格', '販売価格(万円)', '住所', '立地', '土地面積',
                                  '建物面積',  '間取り', '築年月', '築年数', '詳細URL', '電話']
        self.suumo_df_list.append(suumo_df_pages)


if __name__ == '__main__':
    if debug == 0:
        pass
    else:
        area_url_json['secondHandHouse'] = {"横浜市鶴見区": "/chukoikkodate/kanagawa/sc_yokohamashitsurumi/",
                                            "横浜市神奈川区": "/chukoikkodate/kanagawa/sc_yokohamashikanagawa/",
                                            "横浜市西区": "/chukoikkodate/kanagawa/sc_yokohamashinishi/",
                                            "横浜市中区": "/chukoikkodate/kanagawa/sc_yokohamashinaka/",
                                            "横浜市南区": "/chukoikkodate/kanagawa/sc_yokohamashiminami/",
                                            "横浜市保土ケ谷区": "/chukoikkodate/kanagawa/sc_yokohamashihodogaya/",
                                            "横浜市磯子区": "/chukoikkodate/kanagawa/sc_yokohamashiisogo/",
                                            "横浜市金沢区": "/chukoikkodate/kanagawa/sc_yokohamashikanazawa/",
                                            "横浜市港北区": "/chukoikkodate/kanagawa/sc_yokohamashikohoku/",
                                            "横浜市戸塚区": "/chukoikkodate/kanagawa/sc_yokohamashitotsuka/",
                                            "横浜市港南区": "/chukoikkodate/kanagawa/sc_yokohamashikonan/",
                                            "横浜市旭区": "/chukoikkodate/kanagawa/sc_yokohamashiasahi/",
                                            "横浜市緑区": "/chukoikkodate/kanagawa/sc_yokohamashimidori/",
                                            "横浜市瀬谷区": "/chukoikkodate/kanagawa/sc_yokohamashiseya/",
                                            "横浜市栄区": "/chukoikkodate/kanagawa/sc_yokohamashisakae/",
                                            "横浜市泉区": "/chukoikkodate/kanagawa/sc_yokohamashiizumi/",
                                            "横浜市青葉区": "/chukoikkodate/kanagawa/sc_yokohamashiaoba/",
                                            "横浜市都筑区": "/chukoikkodate/kanagawa/sc_yokohamashitsuzuki/"}
    all_area_list = []
    df0 = pd.read_csv(csv_path, dtype='str', encoding='utf-16')
    # df0 = pd.read_csv('/home/ubuntu/s3data/ec_s3/old_house.csv',
    #                   dtype='str', encoding='utf-16')
    all_area_list.append(df0)
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
                    AREACLASS.each_page(pages_url)
                    time.sleep(3)
        suumo_df = pd.concat(AREACLASS.suumo_df_list)
        suumo_df['区域'] = area
        suumo_df['日付'] = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        all_area_list.append(suumo_df)
        time.sleep(5)
    result_df = pd.concat(all_area_list)
    result_df.to_csv(csv_path,encoding='utf-16', header=True, index=False)
    #os.system('mv -f tmp_old_house.csv ' + csv_path)
    # result_df.to_csv('/home/ubuntu/s3data/ec_s3/old_house.csv',
    #                  encoding='utf-16', header=True, index=False)

#main('千代田区', 'https://suumo.jp/chukoikkodate/tokyo/sc_chiyoda/')
#for (area, url) in area_url_json['secondHandHouse'].items():
    #try:
#    main(area, (domain+url))
#    time.sleep(5)
    #except Exception:
    #    pass
    #    send_message(area+' failed')

#send_message('grep sell old houses finished')
