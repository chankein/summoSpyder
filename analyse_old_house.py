#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd

import pandas_profiling as pdp
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder
from utils import deal_build_years, deal_price, deal_size, readConf, deal_sum_area

conf, hostname = readConf()
s3_home = conf.get(hostname, "s3_home")


class do_caltulate:
    def __init__(self, max_price=7000, min_price=99):
        csv_path = s3_home + 'old_house.csv'
        df = pd.read_csv(csv_path, dtype={'マンション名': 'str', '販売価格': 'str', '販売価格(万円)': 'float', '住所': 'str', '立地': 'str', '土地面積': 'str', '建物面積': 'str', '間取り': 'str', '築年月': 'str',
                                          '築年数': 'int', '詳細URL': 'str', '電話': 'str', '区域': 'str', '日付': 'str'}, encoding='utf-16', parse_dates=['日付'])
        df = deal_sum_area(df)
        df['建物面積(m2)'] = df['建物面積'].apply(
            lambda x: deal_size(x))
        df['土地面積(m2)'] = df['土地面積'].apply(
            lambda x: deal_size(x))       
        self.df_target = df[df['販売価格(万円)'] > min_price]
        self.df_target = self.df_target[self.df_target['販売価格(万円)'] < max_price]
        self.df_target = self.df_target[self.df_target['建物面積(m2)'] > 0]
        self.df_target['販売価格(万円)m2'] = self.df_target.apply(lambda x: x['販売価格(万円)'] / x['建物面積(m2)'], axis=1)
        #单物件均价
        self.avg_price = self.df_target.groupby(['日付', '区域'])['販売価格(万円)'].mean().reset_index()
        
        #各区每平米均价   
        self.avg_price_per_m2 = self.df_target.groupby(['日付', '区域'])['販売価格(万円)m2'].mean().reset_index()
        
        #各区房源数量
        self.count_houses = self.df_target.groupby(['日付', '区域']).size().reset_index()
        self.count_houses.columns=['日付', '区域','物件数']
        
        #各区平均楼龄
        self.avg_houses_ages = self.df_target.groupby(['日付', '区域'])['築年数'].mean().reset_index()
        self.avg_houses_ages.columns=['日付', '区域','平均築年数']
        
        #各区楼龄分布
        self.avg_houses_ages_dis = self.df_target.groupby(['日付', '区域','築年数']).size().reset_index()
        self.avg_houses_ages_dis.columns=['日付', '区域', '築年数', '楼龄分布']
        
    def write_csv(self):
        self.avg_price.to_csv(s3_home + 'avg_price.csv',encoding='utf-16', header=True, index=False)
        self.avg_price_per_m2.to_csv(s3_home + 'avg_price_per_m2.csv',encoding='utf-16', header=True, index=False)
        self.count_houses.to_csv(s3_home + 'count_houses.csv',encoding='utf-16', header=True, index=False)
        self.avg_houses_ages.to_csv(s3_home + 'avg_houses_ages.csv',encoding='utf-16', header=True, index=False)
        self.avg_houses_ages_dis.to_csv(s3_home + 'avg_houses_ages_distribute.csv',encoding='utf-16', header=True, index=False)

this_analyse = do_caltulate()
this_analyse.write_csv()
