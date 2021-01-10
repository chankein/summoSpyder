# -*- coding: utf-8 -*-
'''
Created on 2019/07/10

@author: Kein-Chan
'''
import configparser
import os
import datetime
import socket
import pandas as pd
import re

def deal_billion(bill_price_string):
    if '億' in bill_price_string:
        price_string = int(bill_price_string.split(
            '億')[0])*10000+int(bill_price_string.split('億')[1])
    else:
        price_string = int(bill_price_string)
    return price_string

def deal_price(price_string):
    price_string = price_string.replace('億円', '0000').replace(
        '万円', '').replace('円', '')
    if '～' in price_string:
        price_avg = (deal_billion(price_string.split('～')[
                     0])+deal_billion(price_string.split('～')[1]))/2
        return price_avg
    elif '・' in price_string:
        price_avg = (deal_billion(price_string.split('・')[
                     0])+deal_billion(price_string.split('・')[1]))/2
        return price_avg
    elif '権利金' in price_string:
        price_string = 0
        return price_string
    elif '万' in price_string:
        price_string = (deal_billion(price_string.split(
            '万')[0])+float(price_string.split('万')[1])/10000)
        return price_string
    else:
        try:
            price_string = deal_billion(price_string)
        except:
            print(price_string)
            price_string = 0
        return price_string


def deal_build_years(date_string):
    now = datetime.datetime.now()
    date_string = date_string.replace(
        '末', '').replace('上旬', '').replace('初旬', '').replace('中旬', '').replace('下旬', '')
    try:
        if '月' in date_string:
            build_date = datetime.datetime.strptime(date_string, '%Y年%m月')
        elif '日' in date_string:
            build_date = datetime.datetime.strptime(date_string, '%Y年%m月%d日')
        else:
            build_date = datetime.datetime.strptime(date_string, '%Y年')
    except:
        print(date_string)
        return None
    return int((now-build_date).days/365)

def readConf():
    hostname=socket.gethostname()
    conf = configparser.ConfigParser()
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(root_path)
    conf.read(root_path + '/summoSpyder/config.ini')
    print(root_path + '/summoSpyder/config.ini')
    return conf, hostname


def deal_size(size_string):
    if 'm2' in size_string:
        size=float(size_string.split('m2')[0])
    elif '㎡' in size_string:
        size = float(size_string.split('㎡')[0])
    else:
        print(size_string)
        size = 0
    return size


def deal_sum_area(df):
    conf, hostname = readConf()
    df_list=[df]
    tokyo23_list=eval(conf.get('common', 'tokyo23'))
    contoury_list=eval(conf.get('common','contoury_area'))
    df_all=df.copy()

    df_all['区域']='全区域'
    df_tokyo=df[df['区域'].isin(tokyo23_list)]
    df_tokyo['区域']='東京23区'
    df_contoury=df[df['区域'].isin(contoury_list)]
    df_contoury['区域']='周辺地区'
    df_list.append(df_all)
    df_list.append(df_tokyo)
    df_list.append(df_contoury)
    return pd.concat(df_list)


def get_target_df(df,filter,max=7000,min=99):
    df_target = df[df['販売価格(万円)'] > min_price]
    df_target = df_target[df_target['販売価格(万円)'] < max_price]
    df_target = df_target[df_target['建物面積(m2)'] > 0]
    return df_target


def get_num(num_string):
    return int(re.findall(r"\d+",num_string)[0])


# def Normalization(pd_data):
#     #对数据进行归一化处理 并存储到eth2.csv
#     sam=[]
#     a=['priceUSD','activeAddresses','adjustedVolume','paymentCount','exchangeVolume','priceBTC']
#     for i in a:
#         y = pd_data.loc[:, i]
#         ys = list(preprocessing.scale(y))  # 归一化
#         sam.append(ys)
 
#     print(len(sam))
#     with open('eth2.csv', 'w') as file:
#         writer = csv.writer(file)
#         for i in range(len(sam[0])):
#             writer.writerow([sam[0][i],sam[1][i],sam[2][i],sam[3][i],sam[4][i],sam[5][i]])
main_area_list=[]
