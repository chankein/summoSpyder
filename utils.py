# -*- coding: utf-8 -*-
'''
Created on 2019/07/10

@author: Kein-Chan
'''
import configparser
import os
import datetime
import socket

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
    elif '万' in price_string:
        price_string = (deal_billion(price_string.split(
            '万')[0])+int(price_string.split('万')[1])/10000)
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
