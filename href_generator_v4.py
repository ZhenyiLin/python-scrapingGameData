# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:06:50 2017

@author: Zhenyi

Generate html links for all games in www.gamefaqs.com
Save links into text file according to each plantform name

"""
#%%
import requests
from bs4 import  BeautifulSoup
import time

def htmlList(consoleName):
    url0 = 'http://www.gamefaqs.com/' + consoleName + '/category/999-all'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    s = requests.session()
    r = s.get(url0, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    pageTag = soup.find_all('ul', {'class':'paginate'})
    try:
        TotalPage = int(pageTag[-1].li.find_all('option')[-1].string)
    except:
        TotalPage = 2
    print("total page= %d" %TotalPage)
    time.sleep(0.1)

    hrefs = []
    for page in range(TotalPage):
        url = url0 + "?page=" + str(page)
        print(url)
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.find('table')
        tags2 = tags.find_all('td',{'class':'rtitle'})
        for t in tags2:
            d = {'href': 'http://www.gamefaqs.com' + t.a['href']}
            #print(d)
            if(not d in hrefs):
                hrefs.append(d)
        time.sleep(0.2)
    print("total game number= %d" %len(hrefs))
    return hrefs

#%%
#consoleNames = ['pc','ps3','ps4','psp','vita','wii-u',
#                'xbox360','xboxone','android','arcade','dreamcast',
#                'gba','gamecube','nes','n64','ps','ps2','saturn',
#                'snes','wii','xbox','neo','gameboy','gbc','msx']
consoleNames = ["switch"]
                
for name in consoleNames:
    hrefs = htmlList(name)
    time.sleep(5)
    fileName = 'html-' + name + '.txt'
    htmlFile = open(fileName, "w")
    for href in hrefs:
        htmlFile.write(" %s \n" %href['href'])
    htmlFile.close()

