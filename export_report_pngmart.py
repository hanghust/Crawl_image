import os 

with open('pngmart_report.csv', 'w') as file:
        file.write('link,home_page,category,child_category,count\n')
        for cat_dir in os.listdir('pngmart'):
            for child_cat_dir in os.listdir('pngmart/{}'.format(cat_dir)):
                lines = [line.strip() for line in open('pngmart/{}/{}/links.txt'.format(cat_dir, child_cat_dir), 'r') if len(line) > 0]
                nbr_img_link = len(lines)
                file.write('http://www.pngmart.com/image/tag/{},pngmart.com,{},{},{}\n'.format(child_cat_dir, cat_dir, child_cat_dir, nbr_img_link))
