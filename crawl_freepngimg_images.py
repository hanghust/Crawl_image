import os
import numpy as np
import pandas as pd
import imagebot
def get_names_folder_category(folder_path):
    images = os.listdir(folder_path)
    category = ['artistic', 'fantasy', 'games', 'holidays', 'learning', 'lifestyle', 'love', 'miscellaneous', 'movies', 'music', 'tableware', 'people', 'religion', 'fruits', 'food', 'vehicles', 'electronics', 'sport']
    path = []
    for img in images:
        if img in category:
            path = [folder_path+img+'/' for img in images]
    return path
def get_name_folder_sub_category(folder_path, path):
    list_ctg = []
    for pt in path:
        path_level2 = get_names_folder_category(pt)
        list_ctg.append(path_level2)
    with open(folder_path+'list_ctg.txt', 'w') as f:
        for my_list in list_ctg:
            for item in my_list:
                f.write("%s\n" % item)

def crawl_image(file_name):
    with open(file_name) as f:
        path_file = f.readlines()
    f.closed
    for path in path_file:
        path = path.replace('\n', '')
        path1 = path + 'links.txt'
        print(path)
        with open(path1) as f:
            links = f.readlines()
        for link in links:
            link = link.replace('\n', '')
            os.system("imagebot crawl " + link + " -is " + path + ' -u')
if __name__ == "__main__":
    # folder_path = '/home/hangnt/hangnt/crawl_images/freepngimg/'
    # path = get_names_folder_category(folder_path)
    # get_name_folder_sub_category(folder_path, path)
    file_name = '/home/hangnt/hangnt/crawl_images/freepngimg/list_ctg.txt'
    crawl_image(file_name)



