#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd

import pandas_profiling as pdp
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder
from utils import deal_build_years, deal_price, deal_size, readConf

conf, hostname = readConf()
s3_home = conf.get(hostname, "s3_home")


class do_caltulate:
    def __init__(self, max_price=7000, min_price=99):
        csv_path = s3_home + 'old_house.csv'
        df = pd.read_csv(csv_path, dtype={'マンション名': 'str', '販売価格': 'str', '販売価格(万円)': 'float', '住所': 'str', '立地': 'str', '土地面積': 'str', '建物面積': 'str', '間取り': 'str', '築年月': 'str',
                                          '築年数': 'int', '詳細URL': 'str', '電話': 'str', '区域': 'str', '日付': 'str'}, encoding='utf-16', parse_dates=['日付'])

        df['建物面積(m2)'] = df['建物面積'].apply(
            lambda x: deal_size(x))
        df_target = df[df['販売価格(万円)'] > min_price]
        df_target = df_target[df_target['販売価格(万円)'] < max_price]
        df_target = df_target[df_target['建物面積(m2)'] > 0]
        df_target['販売価格(万円)m2'] = df_target.apply(lambda x: x['販売価格(万円)'] / x['建物面積(m2)'], axis=1)
        #单物件均价
        avg_price = df_target.groupby(['日付', '区域'])['販売価格(万円)'].mean().reset_index()
        avg_price.to_csv(s3_home + 'avg_price.csv',encoding='utf-16', header=True, index=False)
        #各区每平米均价   
        avg_price_per_m2 = df_target.groupby(['日付', '区域'])['販売価格(万円)m2'].mean().reset_index()
        avg_price_per_m2.to_csv(s3_home + 'avg_price_per_m2.csv',encoding='utf-16', header=True, index=False)
this_analyse = do_caltulate()
