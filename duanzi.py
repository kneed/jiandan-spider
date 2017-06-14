#author:  __keal__
#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

index=0  #全局变量，用来显示爬取段子的序数

def save_joke(res_url):
	global index
	html=BeautifulSoup(requests.get(res_url).text,'html.parser')
	n=[]  #存放oo数
	m=0   #循环变量
	for oo in html.find_all('div',class_='jandan-vote'):
		n.append(int(oo.find('span').string))
	print(n)
	for joke in html.find_all('div',class_='text'):
		if n[m]>50:
			with open('joke.txt','a+',encoding='utf-8') as t:
				for str in joke.find_all('p'):
					if str.string!=None:
						t.write(str.string)
					else:
						t.write(str.find('br').string)
				print('抓取第%s符合要求的段子'%index)
				index+=1
				t.write('\n\n')
		if m<len(n)-1:
			m+=1
#抓取煎蛋段子板块，根据range抓取前n页
if __name__=='__main__':
	url='http://jandan.net/duan'
	for i in range(0,1):
		save_joke(url)
		url = BeautifulSoup(requests.get(url).text,'html.parser').find('a', {'class': 'previous-comment-page'}).get('href')
