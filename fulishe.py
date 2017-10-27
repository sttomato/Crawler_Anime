# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 00:41:14 2017

@author: st
"""

from bs4 import BeautifulSoup
import requests
import os
import time

url = 'http://www.182fl.com/?cate=6&page=1'
def get_data(url):
    data_list = []
    web_data = requests.get(url)
    Soup = BeautifulSoup(web_data.text, 'lxml')
    infos = Soup.select('#main > ul > li > a')
    titles = Soup.select('#main > ul > li > a > div.info > span.title')
    for info, title in zip(infos, titles):
        
        #print info
        #link = info.get('href')
        #print link
        #print title.get_text()
        data = {
                'title': title.get_text(),
                'link': info.get('href')
                }
        data_list.append(data)
    return data_list

def img_download(links, path):
    i = 0
    for link in links:
        i += 1
        try:
            pic = requests.get(link, timeout = 10)
        except requests.exceptions.ConnectionError:
            print "[ERROR] Image Cannot be saved."
            continue
        string = path + '\\' + str(i) +'.jpg'
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        print '> ' + link + '\t' + str(i)
    
def valid_path(string):
    esc_list = ['*', ':', '?', '\\', '/', '\"', '<', '>', '|']
    for esc in esc_list:
        string = string.replace(esc, '_')  
    return string

def get_img(datas, start = 0):
    #data = datas[0]
    print "Total: ", len(datas)
    print
    i = 0
    for data in datas:
        i += 1
        if (i < start):
            continue
        title = data['title']
        link = data['link']
        link = link + '&page=all'
        print i
        print "link: ", link
        title = valid_path(title)
        path = 'fuli\\' + title
        if not os.path.exists(path):
            os.mkdir(path)
        print "path: ", path
        img_data = requests.get(link)
        img_soup = BeautifulSoup(img_data.text, 'lxml')
        images = img_soup.select('#main > div.article.clearfix > div.art-body > p > img')
        img_links = []
        for image in images:
            img_link = image.get('src')
            #print '> ', img_link
            img_links.append(img_link)
        print "Count: ", len(img_links)
        img_download(img_links, path)
    
start = 4
end = 5
for i in range(start, end):
    url = 'http://www.182fl.com/?cate=10&page={}'.format(i)
    data_list = get_data(url)
    get_img(data_list)
    time.sleep(2)
    

'''
#main > ul > li:nth-child(1) > a
#main > ul > li:nth-child(2) > a
#main > ul > li:nth-child(1) > a > div.info > span.title
#main > div.article.clearfix > div.art-body > p:nth-child(2) > img
#main > div.article.clearfix > div.art-body > p:nth-child(3) > img
'''