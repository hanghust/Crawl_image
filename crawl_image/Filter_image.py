import os
import pandas as pd
from extract_information_image import extract_all_path
path = []
path_file = extract_all_path('crawl_data/pngimg.com1/', 'png')
list_str = ['_', '.']
# list_str = ['_PNG_', '_Transparent', '_Background', '_Download']
# for pt in path_file:
#     path.append((pt.split('/'))[-1].split('_')[0])
for pt in path_file:
    for x in list_str:
        if x in pt:
            pa = (pt.split('/')[-1]).split(x)[0]
            pt = pa
    path.append(pa)

df = pd.DataFrame()
df['Path'] = path_file
df['Category'] = path
df.to_csv('crawl_data/path_file_pngimg.csv', index=False)
