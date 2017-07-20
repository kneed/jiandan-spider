#author __keal__
#coding: utf-8
#多进程抓取

import requests
from bs4 import BeautifulSoup
import multiprocessing
import os
import time

headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
url_lists=[]
# 在当前目录下保存图片
def save_jpg(res_url):
    index=1
    oo_num=[] #保存图片得到的赞数
    n=0
    html = BeautifulSoup(requests.get(res_url).text, 'html.parser')
#判断需要oo大于多少的数
    for oo in html.find_all('div',class_='jandan-vote'):
        oo_num.append(int(oo.find('span',{'class':'tucao-like-container'}).find('span').string))
    for link in html.find_all('a', {'class': 'view_img_link'}):
        if oo_num[n]>0:
            with open(link.get('href').split('/')[-1], 'wb')as jpg:
                jpg.write(requests.get("http:" + link.get('href')).content)
                print('pid:'+str(os.getpid())+'  '+ "正在抓取第%s条数据" % index)
                index+=1
        if n<len(oo_num)-1:
           n+=1

def get_url_lists():
    global url_lists
    start_url='http://jandan.net/ooxx'
    url_lists.append(start_url)
    tag=BeautifulSoup(requests.get(start_url).text,'html.parser').find('a', {'class': 'previous-comment-page'})#下一页
    for i in range(7):
        next_url = tag.get('href')
        url_lists.append(next_url)
        tag=BeautifulSoup(requests.get(next_url).text,'html.parser').find('a', {'class': 'previous-comment-page'})
        print(len(url_lists))

#  多进程抓取。
if __name__ == '__main__':
    start=time.time()
    get_url_lists()
    pool=multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(save_jpg,url_lists)
    pool.close()
    pool.join()
    end=time.time()
    print('所用时间：',str(end-start))
    

