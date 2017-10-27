# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time

urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(i) for i in range(1, 15)]

def get_fzlink(url):
    
    web_data = requests.get('http://bj.xiaozhu.com/')
    Soup = BeautifulSoup(web_data.text, 'lxml')

#print Soup

    list_link_text = Soup.select('#page_list > ul > li > a')
    #print list_link[0].get('href')
    list_link = []
    for link in list_link_text:
        list_link.append(link.get('href'))
    return list_link
########################################
#test_link = list_link[0]
#print test_link

def get_attr(fz_link):

    fangzi_data = requests.get(fz_link)
    
    fz_soup = BeautifulSoup(fangzi_data.text, 'lxml')
    
    #print fz_soup
    titles = fz_soup.select('div.pho_info > h4')
    title = titles[0].get_text()
    
    addrs = fz_soup.select('div.pho_info > p > span')
    addr = addrs[0].get_text()
    
    prices = fz_soup.select('#pricePart > div.day_l > span')
    price =  prices[0].get_text()
    
    images = fz_soup.select('#detailImageBox > div.pho_show_l > div > div:nth-of-type(2)')
    image = images[0].find_all('img')[0].get('src')
    
    lord_imgs = fz_soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    lord_img = lord_imgs[0].get('src')
    
    lord_genders =fz_soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    gender = 'male'
    if lord_genders[0].get('class')[0] == 'member_ico1' :
        gender = 'female'
    
    lord_names = fz_soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    name = lord_names[0].get_text()
    
    fz_data = {
            'title': title.strip(),
            'address': addr.strip(),
            'price': price,
            'image': image.strip(),
            }
    lord_data = {
            'image': lord_img,
            'gender': gender,
            'name': name
            }
    #print 'fangzi info'
    #print repr(fz_data).decode("unicode–escape")
    #print 'lord info'
    #print repr(lord_data).decode("unicode–escape")
    fz_str = repr(fz_data).decode("unicode–escape")
    lord_str = repr(lord_data).decode("unicode–escape")
    time.sleep(0.5)
    return fz_str, lord_str
    
f = open('xiaozhuduanzu.txt', 'w+')
i = 0
for url in urls:
    list_link = get_fzlink(url)
    for link in list_link:
        fz, lord = get_attr(link)
        string = 'fangzi info:\n' + fz + '\nlord info:\n' + lord + '\n'
        f.write(string.encode('utf-8'))
        f.write('\n')
        print i
        i = i + 1
    time.sleep(4)

f.close()

'''
body > div > div.con_l > div.pho_info > h4
body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span
#pricePart > div.day_l > span
#page_list > ul > li:nth-child(1) > a
#page_list > ul > li:nth-child(2) > a
#page_list > ul > li:nth-child(2) > a > img
#detailImageBox > div.pho_show_l > div > div:nth-child(2)
#floatRightBox > div.js_box.clearfix > div.member_pic > a > img
#floatRightBox > div.js_box.clearfix > div.member_pic > div
#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a
'''
