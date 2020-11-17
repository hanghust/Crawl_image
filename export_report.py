import os 

try:
    with open('freepngimg/freepngimg_report.csv', 'w') as file:
        file.write('link,home_page,category,child_category,count\n')
        for cat_dir in os.listdir('freepngimg'):
            for child_cat_dir in os.listdir('freepngimg/{}'.format(cat_dir)):
                lines = [line.strip() for line in open('freepngimg/{}/{}/links.txt'.format(cat_dir, child_cat_dir), 'r') if len(line) > 0]
                nbr_img_link = len(lines)
                file.write('https://www.freepngimg.com/{}/{},freepngimg.com,{},{},{}\n'.format(cat_dir, child_cat_dir, cat_dir, child_cat_dir, nbr_img_link))

except:
    print(cat_dir)
