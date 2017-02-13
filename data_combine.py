# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 09:53:26 2017

@author: Zhenyi
"""
#%%
import pandas as pd


#%%
directory = './data'

consoleNames = ['3ds','pc-1','pc-2','pc-3','pc-4','pc-5','pc-6','pc-7','pc-8',
                'iphone-1','iphone-2','iphone-3','iphone-4','iphone-5','iphone-6',
                'iphone-7','iphone-8','iphone-9','iphone-10',
                'ps','ps2','ps3','ps4','psp','vita','ds','msx',
                'android','arcade','dreamcast','neo','gameboy','gbc',
                'gba','gamecube','nes','n64','saturn','switch',
                'snes','wii','wii-u','xbox','xbox360','xboxone']

#%%
data = pd.DataFrame()
list_ = []
for name in consoleNames:
    file = directory + '/data_' + name + '.csv'
    print(name)
    df = pd.read_csv(file, encoding="utf-8", index_col=None, header=0)
    del df['Unnamed: 0']
    list_.append(df)
data = pd.concat(list_)

save_file = directory + '/all_data.csv'

data.to_csv(save_file, encoding='utf-8')
    
##%%
#file = './data/data_xboxone.csv'
#df = pd.read_csv(file, encoding='ISO-8859-1')
#del df['Unnamed: 0']
#df.to_csv(file, encoding = 'utf-8')


#%%
directory = './data'
dataFile = './data/all_data.csv'
data = pd.read_csv(dataFile)
data['imgLink'].fillna(data['img-link'], inplace=True)
del data['Unnamed: 0']
del data['img-link']
save_file = directory + '/all_data.csv'
data.to_csv(save_file, encoding='utf-8')





