#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd

import pandas_profiling as pdp
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder
# from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn import preprocessing
from sklearn import metrics
from utils import *

conf, hostname = readConf()
s3_home = conf.get(hostname, "s3_home")


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
#     print('完毕')

class do_caltulate:
    def __init__(self, max_price=7000, min_price=99):
        # csv_path = s3_home + 'old_house.csv'
        csv_path = 'old_house.csv'
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
    def grouping(self):
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

        #各区楼龄价格分布
        self.age_price_dis = self.df_target.groupby(['区域','築年数'])['販売価格(万円)m2'].mean().reset_index()

        #各区距离价格分布
        self.distance_price = self.df_target.groupby(['区域','距離(分)'])['販売価格(万円)m2'].mean().reset_index()


    def write_csv(self,directory):
        # self.avg_price.to_csv(directory + 'avg_price.csv',encoding='utf-16', header=True, index=False)
        # self.avg_price_per_m2.to_csv(directory + 'avg_price_per_m2.csv',encoding='utf-16', header=True, index=False)
        # self.count_houses.to_csv(directory + 'count_houses.csv',encoding='utf-16', header=True, index=False)
        # self.avg_houses_ages.to_csv(directory + 'avg_houses_ages.csv',encoding='utf-16', header=True, index=False)
        # self.avg_houses_ages_dis.to_csv(directory + 'avg_houses_ages_distribute.csv',encoding='utf-16', header=True, index=False)

        self.age_price_dis.to_csv(directory + 'avg_houses_ages_price_distribute.csv',encoding='utf-16', header=True, index=False)
        self.distance_price.to_csv(directory + 'avg_distance_price_distribute.csv',encoding='utf-16', header=True, index=False)

    def get_location(self):
        df_split1=self.df_target['立地'].str.split('「', expand=True)
        df_split2=df_split1[1].str.split('」', expand=True)
        df_split1=df_split1.loc[:,[0]]
        df_split1.columns=['鉄道']
        df_split2.columns=['駅','距離']
        self.df_target=pd.concat([self.df_target,df_split1,df_split2], axis=1)
        self.df_target['距離(分)']=self.df_target['距離'].apply(lambda x: get_num(x))

        

        
        
    
    def regression(self):
        self.df_regression=self.df_target.loc[:,['建物面積(m2)','土地面積(m2)','築年数','駅','距離(分)','販売価格(万円)']]
        X=self.df_regression.loc[:,['建物面積(m2)','土地面積(m2)','築年数','距離(分)']]
        y=self.df_regression['販売価格(万円)']

        X=preprocessing.scale(X)
        y=preprocessing.scale(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        # model.fit(X_train,y_train)
        print(lr.coef_)
        print('建物面積(m2),土地面積(m2),築年数,距離(分)')
        print(lr.intercept_)
        print('===========================')
        y_pred = lr.predict(X_test)
        print('===========================')
        
        MSE = metrics.mean_squared_error(y_test, y_pred)
        RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))

        print('MSE:',MSE)
        print('RMSE:',RMSE)


this_analyse = do_caltulate()
this_analyse.get_location()
this_analyse.grouping()
this_analyse.write_csv('./')
# this_analyse.regression()

