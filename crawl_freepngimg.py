from bs4 import BeautifulSoup
import requests
import urllib
from headers import HEADERS
import random
import os
import time
from multiprocessing import Pool, cpu_count
import subprocess
import time

homepage = 'https://freepngimg.com'
categories_link = 'https://freepngimg.com/categories'
proxies = {'http':  'socks5h://127.0.0.1:9050',
           'https': 'socks5h://127.0.0.1:9050'}

root_dir = 'freepngimg'

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
    categories = soup.find_all('button', {'style': 'margin-bottom:4px;', 'class': 'btn btn-template-main'})
    if categories == None:
        print('Parse all categories failed!')
        return []
    return ['{}/{}'.format(homepage, category.text) for category in categories]

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
    categories = soup.find('ul', {'class': 'ct-nav list-inline'})
    if categories == None:
        print('Parse all categories failed!')
        return []
    return [homepage + category['href'] for category in categories.find_all('a', href=True)]

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
    child_pages = soup.find('ul', {'class': 'pagination'})
    if child_pages == None:
        print('Parse next page failed!')
        return None
    for child_page in child_pages.find_all('a', href=True):
        if child_page.text == 'Next »':
            return homepage + child_page['href']
    return None

def parse_all_image_links(page):
    soup = BeautifulSoup(page.content, "html.parser")
    image_boxes = soup.find('section').find('ul', {'class': 'list-inline'})
    if image_boxes == None:
        print('Parsing all images may failed!')
        return []
    return [homepage + image_box['href'] for image_box in image_boxes.find_all('a', href=True)]

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

def crawl_link(categories):
    for cat in categories:
        category_name = cat.split('/')[-1]
        child_categories = crawl_all_child_categories(cat)

        if child_categories != None:
	        for child_cat in child_categories:
	            child_category_name = child_cat.split('/')[-1]
	            image_links = crawl_all_image_links(child_cat, category_name)

	            print('-----------------------------------------------------')

	            if image_links != None:
	                with open(os.path.join(root_dir, category_name, child_category_name, 'links.txt'), 'w') as file:
	                    for link in image_links:
	                        file.write(link + '\n')
	                print(category_name, child_category_name)
	            else:
	                with open('error_crawl_freepngimg_child_catrgories.txt', 'a') as file_child_cat:
	                	file_child_cat.write('{}\n'.format(child_cat))
        else:
            with open('error_crawl_freepngimg_child_catrgories.txt', 'a') as file_cat:
                file_cat.write('{}\n'.format(cat))
    
if __name__ == '__main__':
    #categories = crawl_categories(categories_link)
    #with open('crawl_freepngimg_categories.txt', 'w') as file:
    #    for cat in categories:
    #        file.write('{}\n'.format(cat))
    categories = [cat.strip() for cat in open('crawl_freepngimg_categories.txt', 'r')]
    crawl_link(categories)
            
            
            
    
