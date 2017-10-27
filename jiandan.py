# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 15:00:33 2017

@author: st
"""

from bs4 import BeautifulSoup
import requests
import time

#url = 'http://jandan.net/ooxx/page-1#comments'
def get_link(url):
    
    web_data = requests.get(url)
    Soup = BeautifulSoup(web_data.text, 'lxml')
    #print Soup
    images = Soup.select('div > div > div.text > p > a')
    #a = images[0].get('src')
    #print a[-3:]
    #print 
    image_link = []
    for image in images:
        a = image.get('href')
        #if a[-3:] == 'gif':
        #    a = image.get('org_src')
        image_link.append(a)
    return image_link


def get_more(start, end, restart=0):
    j = 0
    for i in range(start, end):
        url = 'http://jandan.net/ooxx/page-{}#comments'.format(i)
        pic_url = get_link(url)
        for each in pic_url:
            j = j + 1
            if j < restart:
                continue

            each = 'http:' + each
            print each
            try:
                pic = requests.get(each, timeout=10)
            except requests.exceptions.ConnectionError:
                print "[ERROR] Image Cannot be saved."
                continue
            postfix = each[-4:]
            string = 'pictures\\' + str(j) + postfix
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()

    time.sleep(2)


get_more(1, 236)

'''
for each in pic_url:
    print each
    try:
        pic= requests.get(each, timeout=10)
    except requests.exceptions.ConnectionError:
        print '【错误】当前图片无法下载'
        continue
    string = 'pictures\\'+str(i) + '.jpg'
    fp = open(string,'wb')
    fp.write(pic.content)
    fp.close()
    i += 1
'''

'''
#comment-3596839 > div > div > div.text > p > img
#comment-3596837 > div > div > div.text > p > img
#comment-3596837 > div > div > div.text > p > a
'''