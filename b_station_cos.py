# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 21:35:37 2017

@author: st
"""

#from bs4 import BeautifulSoup
import requests
import json
import os
import time

url = 'https://api.vc.bilibili.com/link_draw/v1/doc/list?category=cos&type=2&page_size=20&page_num=0&tag=&source=normal'

def get_imgs_link(url):
    res_link = []
    web_data = requests.get(url)
    #print web_data.text
    jsonData = web_data.text
    #Soup = BeautifulSoup(web_data.text, 'lxml')
    #print Soup
    #jsonData = Soup.get_text()
    #print jsonData
    text = json.loads(jsonData)
    #print text.keys()
    #print text
    data = text['data']
    #print data.keys()
    items = data['items']
    #print len(items) # 20
    for its in items:
        user = its['user']
        name = user['name']
        item = its['item']
        #print name
        title = item['title']
        pictures = item['pictures']
        #print pictures   #
        imgs_link = []
        for pic in pictures:
            imgs_link.append(pic['img_src'])
        data = {
                'name': name,
                'title': title,
                'imgs_link':imgs_link
                }
        
        res_link.append(data)
    return res_link

def valid_path(string):
    esc_list = ['*', ':', '?', '\\', '/', '\"', '<', '>', '|']
    for esc in esc_list:
        string = string.replace(esc, '_')
    return string
def get_imgs(infos):
    
    for info in infos:
        name = info['name']
        title = info['title']
        links = info['imgs_link']
        numbers = 0
        title = valid_path(title)
        name = valid_path(name)
        path = 'bstation\\cos\\' + name
        #path = path.replace('*', '_')
        print path
        if not os.path.exists(path):
            os.mkdir(path)
        for link in links:
            numbers += 1
            try:
                pic = requests.get(link, timeout = 10)
            except requests.exceptions.ConnectionError:
                print "[ERROR] Image Cannot be saved."
                continue
            string = path + '\\' + title + '_' + str(numbers) +'.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            print '> ' + string
        
def get_more(start, end):
    for i in range(start, end):
        print i
        url = 'https://api.vc.bilibili.com/link_draw/v1/doc/list?category=cos&type=2&page_size=20&page_num={}&tag=&source=normal'.format(i)        
        infos = get_imgs_link(url)
        #print infos
        get_imgs(infos)
        time.sleep(2)

get_more(0, 40)
#for img in imgs:
#    image = img.get('img_src')
    
#    print image
