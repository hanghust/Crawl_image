from bs4 import BeautifulSoup
import requests
import urllib
from headers import HEADERS
import random
import os
import time
from multiprocessing import Pool, cpu_count
import subprocess

homepage = 'https://pngmart.com'
categories_link = 'https://freepngimg.com/categories'
proxies = {'http':  'socks5h://127.0.0.1:9050',
           'https': 'socks5h://127.0.0.1:9050'}

root_dir = 'pngmart'

def get_sub_file_iterator(_dir, endswith=''):
    for entry in os.scandir(_dir):
        if entry.is_file() and entry.path.endswith(endswith):
            yield entry
        elif entry.is_dir():
            yield from get_sub_file_iterator(entry.path, endswith)
            
def get_page(url):
    header = random.choice(HEADERS)
    try:
        page = requests.get(url, proxies=proxies, headers=header, timeout=120)
    except Exception as e:
        print('get {} failed!'.format(url))
        print(e)
    return page
    
def parse_big_image_link(page):
    soup = BeautifulSoup(page.content, "html.parser")
    big_image_link = soup.find('div', {'class': 'png-big'}).find('img')['src']
    if big_image_link == None:
        print('Parsing big images may failed!')
        return None
    return homepage + big_image_link

def crawl_big_image(url):
    big_image_page = get_page(url)
    if big_image_page != None:
        big_image_link = parse_big_image_link(big_image_page)
    else:
        return None
    return big_image_link.replace(' ', '%20')

def download_big_image(url, folder):
    filename = url.split('/')[-1]
    try:
        urllib.request.urlretrieve(url, os.path.join(folder, filename))
    except Exception as e:
        print('Parse all images failed!')
        print(e)
        return -1
    return 1

def download_in_parallel(links):
    big_image_link = crawl_big_image(links[0])
    download_big_image(big_image_link, os.path.join(root_dir, links[1], links[2]))
    
if __name__ == '__main__':
    for link_files in get_sub_file_iterator(root_dir, endswith='txt'):
        print(link_files.path)
        child_category = link_files.path.split('/')[-2]
        category = link_files.path.split('/')[-3]
        links = [(link.strip(), category, child_category) for link in open(link_files, 'r')]
        downloaded = [file for file in get_sub_file_iterator(os.path.join(root_dir, category, child_category), endswith='png')] 
        if len(links) == len(downloaded):
            continue
        rss = []
        tic = time.time()
        with Pool(3) as pool:
            rss = pool.map(download_in_parallel, links)
            pool.close()
            pool.join()
        
        toc = time.time()
        print((toc - tic) / max(len(links), 1))
        
            
            
            
    
