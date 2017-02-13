# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:41:17 2017

@author: Zhenyi
version 6:
    fix bugs

version 5:
    1) add check request status code
    2) improve delay
    3) fix bugs output file

"""

import requests
from bs4 import  BeautifulSoup
import time
import pandas as pd
import random


#%%
def parse(url):
    header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
    header2 = {'User_Agent': 'AppleWebKit/537.36 (KHTML, like Gecko)'}
    header3 = {'User_Agent': 'Chrome/55.0.2883.87 Safari/537.36'}
    headerList = [header1, header2, header3]    
    for i in range(3):
        try:
            headers = random.choice(headerList)
            s = requests.session()
            r = s.get(url, headers=headers)
            break
        except:
            continue
    if( r.status_code != requests.codes.ok):
        print("Can not be connected, ignore this one")
        dic = {}
        return dic
        
    soup = BeautifulSoup(r.text, 'html.parser')
    for e in soup.find_all('br'):
        e.extract()

    try:
        # extract game title
        title = soup.find('h1', {'class':'page-title'}).string
                      
        # extract game description                  
        description = soup.find('div', {'class': 'body game_desc'}).div.contents
        descriptionText = ''                        
        for text in description:
            descriptionText += text

        # extract game category    
        tags = soup.find_all("li",{"itemprop":"applicationCategory"})    
        category=[]
        for t in tags:
            category.append(t.string)
    
        dic = {'title':title, 'description':descriptionText, 
               'category':category, 'html':url}    
    except:
        return {}

    # extract game details
    try:
        tag = soup.find_all("div",{"class":"pod pod_gameinfo"})[0]
        tags = tag.find_all("li")                    
    except:
        return dic
    


    imgLink = ''
    platform = ''
    releaseDate = ''
    creator = ''
    for t in tags:
        try:
            if(t.find("img")):
                imgLink = t.find("img")["src"]
        except:
            imgLink = ''
            
        try:
            if(t.has_attr("itemprop")) and (t["itemprop"]=="gamePlatform"):
                platform =  t.b.string
        except:
            platform = ''
            
        try:
            if (t.find('b')) and (t.b.string == "Release:"):
                releaseDate = t.a.string[:-2]
        except:
            releaseDate = 'ERROR'
         
    if(not tags[2].find("b")) and (not tags[2].has_attr("itemprop")):        
        contents = tags[2].contents
        for c in contents:
            creator += c.string
    

    if(releaseDate == "TBA") or( releaseDate == "Canceled") or (releaseDate =="ERROR"):
        gameDetails = {"img-link":imgLink, "platform":platform,"creator":creator,
                   "releaseDate":releaseDate, "franchise":''}
        dic.update(gameDetails)    
        dic2= {'faq':'', 'cheats':'','reviews':'', 'rate_reviews':'', 
               'critic':'', 'rate_critic':'','questions':'', 'answers':''} 
        dic.update(dic2)
        statistics = {"star":[], "ownership":[], "play":[],
                      "difficulty":[], "playTime":[],
                      "star_a": '', "play_beaten_percent": '',
                      "difficulty_a": '', "playTime_a":'',
                      "star_userNo":'',"owner_userNo":'',
                      "play_userNo":'',"difficulty_userNo":'',
                      "playTime_userNo":''}
        dic.update(statistics)
        return dic
    
        
    franchise = ''    
    try:
        for t in tags:
            if (t.find('b')) and (t.b.string == "Franchise:"):
                franchise = t.a.string
                break
    except:
        franchise = ''

    gameDetails = {"imgLink":imgLink, "platform":platform,"creator":creator,
                   "releaseDate":releaseDate, "franchise":franchise}

    dic.update(gameDetails)
    
    
    # extract the number of game faq
    href_faq = url[23:] + '/faqs'
    try:
        faq = soup.find_all('a', {'href': href_faq})[-1].contents[0]
        faq = int(faq.split()[0])
    except:
        faq = ''     

    # extract the number of game cheats
    href_cheats = url[23:] + '/cheats'
    try:
        cheats = soup.find_all('a', {'href': href_cheats})[-1].contents[0]
        cheats = int(cheats.split()[0])
    except:
        cheats = ''    
    
    # extract the number of reviews 
    href_reviews = url[23:] + '/reviews'
    try:
        reviews = soup.find_all('a', {'href': href_reviews})[-1].contents[0]
        rate_reviews = 100*float(reviews.split()[-1][0:-1].split('/')[0])/float(reviews.split()[-1][0:-1].split('/')[1])
        reviews = int(reviews.split()[0])
    except:
        rate_reviews = ''
        reviews = ''
    
    # extract the number of critical reviews    
    href_critic = url[23:] + '/critic'
    try:
        critic = soup.find_all('a', {'href': href_critic})[-1].contents[0]
        rate_critic = 100*float(critic.split()[-1][0:-1].split('/')[0])/float(critic.split()[-1][0:-1].split('/')[1])
        critic = int(critic.split()[0])
    except:
        rate_critic = ''
        critic = ''

    # extract the number of questions and answers
    href_answers = url[23:] + '/answers'
    try:
        answers = soup.find_all('a', {'href': href_answers})[-1].contents[0]
        questions = int(answers.split()[0])
        answers = questions - int(answers.split()[-2][1:])
    except:
        questions = ''
        answers = ''     

    dic2= {'faq':faq, 'cheats':cheats,
           'reviews':reviews, 'rate_reviews':rate_reviews, 
           'critic':critic, 'rate_critic':rate_critic,
           'questions':questions, 'answers':answers}    
    
    dic.update(dic2)
    
    


    # extract the game statitics in www.gameFaqs.com    
    url_statistics = url + '/stats'
    r = requests.get(url_statistics, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    figTags = soup.find_all("figcaption")
    idxFig = 0
    try:
        tag = soup.find_all("table", {"class":"bar_chart hbars_chart mygames_stats_rate"})[0]
        tags = tag.find_all("tr")
        star = [0.0]*10
        for i in range(1,len(tags)):
            idx = int(tags[i]['class'][1][-1])-1
            if(idx==-1):
                idx=9
            star[idx] = float(tags[i]['title'].split()[0][:-1])
        star_userNo = int(figTags[idxFig].string.split()[6])
        star_a = float(figTags[idxFig].string.split()[10])*20   #normalized to 100
        idxFig += 2
    except:
        star = []*10
        star_userNo = ''
        star_a = ''
    
    try:
        tag = soup.find_all("table", {"class":"bar_chart hbars_chart mygames_stats_own"})[0]
        tags = tag.find_all("tr")                    
        owner = [0.0]*4
        for i in range(1,len(tags)):
            idx = int(tags[i]['class'][1][-1])-1
            owner[idx]=float(tags[i]['title'].split()[0][:-1])
        owner_userNo = int(figTags[idxFig].string.split()[5])
        idxFig += 2
    except:
        owner = []*4
        owner_userNo = ''
     
    try:   
        tag = soup.find_all("table", {"class":"bar_chart hbars_chart mygames_stats_play"})[0]
        tags = tag.find_all("tr")                    
        play = [0.0]*5
        for i in range(1,len(tags)):
            idx = int(tags[i]['class'][1][-1])-1
            play[idx] = float(tags[i]['title'].split()[0][:-1])
        play_userNo = int(figTags[idxFig].string.split()[6])
        play_beaten = float(figTags[idxFig].string.split()[14][:-1])
        idxFig += 2
    except:
        play = []*5
        play_userNo = ''
        play_beaten = ''
         

    try:  
        tag = soup.find_all("table", {"class":"bar_chart hbars_chart mygames_stats_diff"})[0]
        tags = tag.find_all("tr")                    
        difficulty = [0.0]*5
        for i in range(1,len(tags)):
            idx = int(tags[i]['class'][1][-1])-1
            difficulty[idx]=float(tags[i]['title'].split()[0][:-1])
        difficulty_userNo = int(figTags[idxFig].string.split()[6])
        difficulty_a = figTags[idxFig].string.split(':')[2]
        idxFig += 2
    except:
        difficulty = []*5
        difficulty_a = ''
        difficulty_userNo = ''
        
            
    try:
        tag = soup.find_all("table", {"class":"bar_chart hbars_chart mygames_stats_time"})[0]
        tags = tag.find_all("tr")                    
        playTime = [0.0]*10
        for i in range(1,len(tags)):
            idx = int(tags[i]['class'][1][-1])-1
            if(idx==-1):
                idx=9
            playTime[idx] = float(tags[i]['title'].split()[0][:-1])
        playTime_userNo = int(figTags[idxFig].string.split()[6])
        playTime_a = float(figTags[idxFig].string.split()[11])
    except:
        playTime = []*10
        playTime_a = ''
        playTime_userNo = ''
    
#    print(star)
#    print(star_userNo, star_a)
#    print(owner)
#    print(owner_userNo)
#    print(play)
#    print(play_userNo, play_beaten)
#    print(difficulty)
#    print(difficulty_userNo, difficulty_a)
#    print(playTime)
#    print(playTime_userNo, playTime_a)
  
    statistics = {"star":star, "ownership":owner, "play":play,
                  "difficulty":difficulty, "playTime":playTime,
                  "star_a": star_a, "play_beaten_percent": play_beaten,
                  "difficulty_a": difficulty_a, "playTime_a":playTime_a,
                  "star_userNo":star_userNo,"owner_userNo":owner_userNo,
                  "play_userNo":play_userNo,"difficulty_userNo":difficulty_userNo,
                  "playTime_userNo":playTime_userNo}

    dic.update(statistics)
    
    return dic
#%%

urls=['http://www.gamefaqs.com/pc/200777-7d-game','http://www.gamefaqs.com/iphone/157964-daily-crosswords']
#urls=['http://www.gamefaqs.com/pc/954437-league-of-legends']

data = []        
for url in urls:
    dic = parse(url)
    data.append(dic)
    print(dic)
 
df = pd.DataFrame(data)
#df.to_csv('C:\Dropbox\codes\codes_python\python_dataIncubator2\dataScraping01\data\data_temp.csv')
print(df.imgLink)
print(df.platform)
print(df.releaseDate)
print(df.creator)


#%%

#consoleNames = ['3ds','iphone','pc','ps3','ps4','psp','vita','wii-u',
#                'xbox360','xboxone','android','arcade','dreamcast',
#                'gba','gamecube','nes','n64','ps','ps2','saturn',
#                'snes','wii','xbox','neo','gameboy','gbc']
consoleNames = ['ps2','saturn']
delayList = [0.8]*3 + [1]*5 + [1.5]*2
delay = random.choice(delayList)
time1 = time.time()
for name in consoleNames:
    dir_ubuntu = 'C:/Dropbox/codes/codes_python/python_dataIncubator2/dataScraping01'
    file = dir_ubuntu + '/htmls/html-' + name +'.txt'
    urls=[]
    f = open(file, 'r')
    for line in f:
        urls.append(line.strip())

    data=[]
    i = 0    
    for url in urls:
        i +=1
        if (i%10 ==0) or (i==1):
            print(url)
        data.append(parse(url))
        time.sleep(delay)
        time2 = time.time()
        if (time2 - time1) >= 54.5*60.0:
            print("5 mins sleep for every 55 mins scrapying")  
            time.sleep(320)
            time1 = time.time()

    df = pd.DataFrame(data)
    df.to_csv(dir_ubuntu + '/data/data_' + name +'.csv')

##%%
#urls=['http://www.gamefaqs.com/iphone/647573-the-case-of-the-missing-billionaire-uncle']
#header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
#s = requests.session()
#r = s.get(urls[0], headers=header1)
#
#
##%%
#soup = BeautifulSoup(r.text, 'lxml.html')
#print(soup.prettify())
#tags = soup.find_all("div",{"class":"pod pod_gameinfo"})


