#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn import preprocessing
import pandas_profiling as pdp

df = pd.read_csv('suumo.csv', sep='\t', encoding='utf-16')

splitted1 = df['立地1'].str.split(' 歩', expand=True)
splitted1.columns = ['立地11', '立地12']
splitted2 = df['立地2'].str.split(' 歩', expand=True)
splitted2.columns = ['立地21', '立地22']
splitted3 = df['立地3'].str.split(' 歩', expand=True)
splitted3.columns = ['立地31', '立地32']

splitted4 = df['敷/礼/保証/敷引,償却'].str.split('/', expand=True)
splitted4.columns = ['敷金', '礼金']

df = pd.concat([df, splitted1, splitted2, splitted3, splitted4], axis=1)

df.drop(['立地1', '立地2', '立地3', '敷/礼/保証/敷引,償却'], axis=1, inplace=True)

df = df.dropna(subset=['賃料料'])

df['賃料料'] = df['賃料料'].str.replace(u'万円', u'')
df['敷金'] = df['敷金'].str.replace(u'万円', u'')
df['礼金'] = df['礼金'].str.replace(u'万円', u'')
df['管理費'] = df['管理費'].str.replace(u'円', u'')
df['築年数'] = df['築年数'].str.replace(u'新築', u'0')
df['築年数'] = df['築年数'].str.replace(u'99年以上', u'0')
df['築年数'] = df['築年数'].str.replace(u'築', u'')
df['築年数'] = df['築年数'].str.replace(u'年', u'')
df['専有面積'] = df['専有面積'].str.replace(u'm', u'')
df['立地12'] = df['立地12'].str.replace(u'分', u'')
df['立地22'] = df['立地22'].str.replace(u'分', u'')
df['立地32'] = df['立地32'].str.replace(u'分', u'')

df['管理費'] = df['管理費'].replace('-', 0)
df['敷金'] = df['敷金'].replace('-', 0)
df['礼金'] = df['礼金'].replace('-', 0)

splitted5 = df['立地11'].str.split('/', expand=True)
splitted5.columns = ['路線1', '駅1']
splitted5['徒歩1'] = df['立地12']
splitted6 = df['立地21'].str.split('/', expand=True)
splitted6.columns = ['路線2', '駅2']
splitted6['徒歩2'] = df['立地22']
splitted7 = df['立地31'].str.split('/', expand=True)
splitted7.columns = ['路線3', '駅3']
splitted7['徒歩3'] = df['立地32']

df = pd.concat([df, splitted5, splitted6, splitted7], axis=1)

df.drop(['立地11', '立地12', '立地21', '立地22', '立地31', '立地32'], axis=1, inplace=True)

df['賃料料'] = pd.to_numeric(df['賃料料'])
df['管理費'] = pd.to_numeric(df['管理費'])
df['敷金'] = pd.to_numeric(df['敷金'])
df['礼金'] = pd.to_numeric(df['礼金'])
df['築年数'] = pd.to_numeric(df['築年数'])
df['専有面積'] = pd.to_numeric(df['専有面積'])

df['賃料料'] = df['賃料料'] * 10000
df['敷金'] = df['敷金'] * 10000
df['礼金'] = df['礼金'] * 10000

df['徒歩1'] = pd.to_numeric(df['徒歩1'])
df['徒歩2'] = pd.to_numeric(df['徒歩2'])
df['徒歩3'] = pd.to_numeric(df['徒歩3'])

splitted8 = df['階層'].str.split('-', expand=True)
splitted8.columns = ['階1', '階2']
splitted8['階1'].str.encode('cp932')
splitted8['階1'] = splitted8['階1'].str.replace(u'階', u'')
splitted8['階1'] = splitted8['階1'].str.replace(u'B', u'-')
splitted8['階1'] = splitted8['階1'].str.replace(u'M', u'')
splitted8['階1'] = pd.to_numeric(splitted8['階1'])
df = pd.concat([df, splitted8], axis=1)

df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下1地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下2地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下3地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下4地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下5地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下6地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下7地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下8地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下9地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'平屋', u'1')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'階建', u'')
df['建物の高さ'] = pd.to_numeric(df['建物の高さ'])

df = df.reset_index(drop=True)
df['間取りDK'] = 0
df['間取りK'] = 0
df['間取りL'] = 0
df['間取りS'] = 0
df['間取り'] = df['間取り'].str.replace(u'ワンルーム', u'1')

for x in range(len(df)):
    if 'DK' in df['間取り'][x]:
        df.loc[x, '間取りDK'] = 1
df['間取り'] = df['間取り'].str.replace(u'DK', u'')

for x in range(len(df)):
    if 'K' in df['間取り'][x]:
        df.loc[x, '間取りK'] = 1
df['間取り'] = df['間取り'].str.replace(u'K', u'')

for x in range(len(df)):
    if 'L' in df['間取り'][x]:
        df.loc[x, '間取りL'] = 1
df['間取り'] = df['間取り'].str.replace(u'L', u'')

for x in range(len(df)):
    if 'S' in df['間取り'][x]:
        df.loc[x, '間取りS'] = 1
df['間取り'] = df['間取り'].str.replace(u'S', u'')

df['間取り'] = pd.to_numeric(df['間取り'])

splitted9 = df['住所'].str.split('区', expand=True)
splitted9.columns = ['区', '市町村']
splitted9['区'] = splitted9['区'] + '区'
splitted9['区'] = splitted9['区'].str.replace('東京都', '')
df = pd.concat([df, splitted9], axis=1)

df_for_search = df.copy()

df[['路線1', '路線2', '路線3', '駅1', '駅2', '駅3', '市町村']] = df[[
    '路線1', '路線2', '路線3', '駅1', '駅2', '駅3', '市町村']].fillna("NAN")

oe = preprocessing.OrdinalEncoder()
df[['路線1', '路線2', '路線3', '駅1', '駅2', '駅3', '市町村']] = oe.fit_transform(
    df[['路線1', '路線2', '路線3', '駅1', '駅2', '駅3', '市町村']].values)

df['賃料料+管理費'] = df['賃料料'] + df['管理費']

#上限価格を設定
df = df[df['賃料料+管理費'] < 300000]

df = df[["マンション名", '賃料料+管理費', '築年数', '建物の高さ', '階1',
         '専有面積', '路線1', '路線2', '路線3', '駅1', '駅2', '駅3', '徒歩1', '徒歩2', '徒歩3', '間取り', '間取りDK', '間取りK', '間取りL', '間取りS',
         '市町村']]

df.columns = ['name', 'real_rent', 'age', 'hight', 'level', 'area', 'route_1', 'route_2', 'route_3', 'station_1',
              'station_2', 'station_3', 'distance_1', 'distance_2', 'distance_3', 'room_number', 'DK', 'K', 'L', 'S', 'adress']


pdp.ProfileReport(df)
