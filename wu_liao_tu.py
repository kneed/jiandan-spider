# -*- coding:utf-8 -*-
# author: 禾斗
import requests
from bs4 import BeautifulSoup
import base64
import os
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import time, random

start_url = 'http://jandan.net/pic/page-232#comments'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
num = 0
Flag = True

def download_data(url):
    global num
    dir_path = os.path.abspath('..')
    file_name = url.split('.')[2][-8:-1]
    postfix = url.split('.')[-1].replace('\'', '')
    with open(dir_path + f'\\jan_dan\\wu_liao_tu\\{file_name}.{postfix}', 'wb') as f:
        f.write(requests.get(url, headers=header).content)
    print(f'{num} task done')
    num += 1


def get_wuliaotu(url):
    global start_url, Flag
    try:
        resp = requests.get(url, headers=header)
        bs = BeautifulSoup(resp.text, 'html.parser')
        next_url = 'http:'+ bs.find('a', class_='previous-comment-page').get('href')
    except Exception as err:
        print(f'Error:{err}')
        Flag = False
        return Flag

    url_ls = set()

    for item in bs.find_all('span', class_='img-hash'):
        url = ('http:' + str(base64.b64decode(item.string.encode('utf-8')))[2:]).replace('\'', '')
        url_ls.add(url)

    pool = ProcessPoolExecutor(max_workers=8)
    pool.map(download_data, url_ls)
    url_ls.clear()
    start_url = next_url
    time.sleep(random.randint(3,6))

if __name__ == '__main__':
    while True:
        get_wuliaotu(start_url)