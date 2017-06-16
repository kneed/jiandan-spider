# __author__:keal
#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import re

headers='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
url='https://movie.douban.com/top250'



#创建list存储信息
name=[]
comment_num=[]
comment_star=[]
info=[]
abstract=[]

def get_movie(res_url):
	html=BeautifulSoup(requests.get(res_url).text,'html.parser')
	ol=html.find('ol',class_='grid_view')
	for list in ol.find_all('li'):
		name.append(list.find('span',class_='title').string)
		comment_num.append(list.find(text=re.compile('评价'))) 
		comment_star.append(float(list.find('span',class_='rating_num').string))
		info.append(list.find('div',class_='bd').find('p').get_text().replace(' ',''))
		x=list.find('p',class_='quote')
		if x:
			abstract.append(x.find('span',class_='inq').string)
		else:
			abstract.append(' ')
	print(name)
		
	

def write_into_excel():
	#建立数据类型
	#创建一个excel表
	workbook=xlsxwriter.Workbook('movie.xlsx')
	worksheet=workbook.add_worksheet()
	
	#调用爬虫函数抓取数据
	url='https://movie.douban.com/top250'
	get_movie(url)
	for x in range(25,250,25):
		print(x)
		url=('https://movie.douban.com/top250'+'?start=%d&amp;filter='%x)
		get_movie(url)
			
	for (n,cn,cs,i,a) in zip(name,comment_num,comment_star,info,abstract):
		col_A= 'A%s' %(name.index(n)+1)
		col_B= 'B%s' %(name.index(n)+1)
		col_C= 'C%s' %(name.index(n)+1)
		col_D= 'D%s' %(name.index(n)+1)
		col_E= 'E%s' %(name.index(n)+1)
		worksheet.write(col_A,n)
		worksheet.write(col_B,cn)
		worksheet.write(col_C,cs)
		worksheet.write(col_D,i)
		worksheet.write(col_E,a)
	workbook.close()

if __name__ == '__main__':
	write_into_excel()