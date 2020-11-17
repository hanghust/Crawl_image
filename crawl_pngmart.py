from bs4 import BeautifulSoup
import requests
import urllib
from headers import HEADERS
import random
import os
import time
from multiprocessing import Pool, cpu_count
import subprocess

homepage = 'http://www.pngmart.com/'
categories_link = 'http://www.pngmart.com/categories'
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

def parse_all_categories(page):
    soup = BeautifulSoup(page.content, "html.parser")
    categories = soup.find('ul', {'class': 've-cat-widget-listing'})
    if categories == None:
        print('Parse all categories failed!')
        return []
    return [category['href'] for category in categories.find_all('a', href=True)]

def crawl_categories(url):
    categories_page = get_page(url)
    if categories_page != None:
        categories = parse_all_categories(categories_page)
    else:
        return None
    if categories != None:
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
    return categories

def parse_all_child_categories(page):
    soup = BeautifulSoup(page.content, "html.parser")
    categories = soup.find('div', {'class': 'category_tags'})
    if categories == None:
        print('Parse all categories failed!')
        return []
    return [category['href'] for category in categories.find_all('a', href=True)]

def crawl_all_child_categories(url):
    category_name = url.split('/')[-1]
    child_categories_page = get_page(url)
    if child_categories_page != None:
        child_categories = parse_all_child_categories(child_categories_page)
    else:
        return None
    if child_categories != None:
        path = os.path.join(root_dir, category_name)
        if not os.path.exists(path):
            os.makedirs(path)
    return child_categories

def parse_next_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    child_page = soup.find('a', {'class': 'nextpostslink'})
    if child_page == None:
        return None
    return child_page['href']

def parse_all_image_links(page):
    soup = BeautifulSoup(page.content, "html.parser")
    image_boxes = soup.find_all('div', {'class': 'featuredimage'})
    if image_boxes == None:
        print('Parsing all images may failed!')
        return []
    return [image.find('a', href=True)['href'] for image in image_boxes]

def crawl_all_image_links(url, category_name):
    image_links = []
    child_category_name = url.split('/')[-1]
    image_links_page = get_page(url)
    if image_links_page != None:
        image_links += parse_all_image_links(image_links_page)
    else:
        return None
    if image_links != None:
        path = os.path.join(root_dir, category_name, child_category_name)
        if not os.path.exists(path):
            os.makedirs(path)
    
    while parse_next_page(image_links_page) != None:
        next_page = parse_next_page(image_links_page)
        image_links_page = get_page(next_page)
        if image_links_page != None:
            next_image_links = parse_all_image_links(image_links_page)
            image_links += next_image_links
        else:
            return None
    return image_links

def crawl_link(categories):
    for cat in categories:
        category_name = cat.split('/')[-1]
        child_categories = crawl_all_child_categories(cat)

        if child_categories != None:
            for child_cat in child_categories:
                try:
                    crawled = [line.strip() for line in open('pngmart/{}/{}/links.txt'.format(cat.split('/')[-1], child_cat.split('/')[-1]), 'r') if len(line.strip()) > 0]
                    if len(crawled) > 0:
                        print('--------- skip {} --- {}'.format(cat, child_cat))
                        continue
                except Exception as e:
                    print(e)
                child_category_name = child_cat.split('/')[-1]
                image_links = crawl_all_image_links(child_cat, category_name)

                print('-----------------------------------------------------')

                if image_links != None:
                    with open(os.path.join(root_dir, category_name, child_category_name, 'links.txt'), 'w') as file:
                        for link in image_links:
                            file.write(link + '\n')
                    print(category_name, child_category_name)
                else:
                    with open('error_crawl_pngmart_child_catrgories.txt', 'a') as file_child_cat:
                        file_child_cat.write('{}\n'.format(child_cat))
        else:
            with open('error_crawl_pngmart_child_catrgories.txt', 'a') as file_cat:
                file_cat.write('{}\n'.format(cat))
    
if __name__ == '__main__':
    categories = crawl_categories(categories_link)
    with open('crawl_pngmart_categories.txt', 'w') as file:
       for cat in categories:
           file.write('{}\n'.format(cat))
    # categories = [cat.strip() for cat in open('crawl_pngmart_categories.txt', 'r')]
    print(categories)
    crawl_link(categories)
    
