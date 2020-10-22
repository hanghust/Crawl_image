import imagebot
import os

# list_web = []
web1 = 'http://pngimg.com/imgs/animals/'
# web2 = 'https://freepngimg.com/animals'
# 'http://pngimg.com/imgs/animals/'
# https://www.stickpng.com/cat/animals
# http://www.pngmart.com/image/category/animals/
# https://freepngimg.com/animals
# for i in range(2,10):
#     list_web.append(web+str(i))
# for page in list_web:
#     os.system("imagebot crawl " + page + " -is /home/hangnt/EDA_data_json/crawl_data/")

os.system("imagebot crawl " + web1 + " -is /home/hangnt/EDA_data_json/crawl_data/ -u")

########################################################################################################################
########################################################################################################################
