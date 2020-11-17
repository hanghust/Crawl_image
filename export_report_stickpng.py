import os 

with open('stickpng_report.csv', 'w') as file:
    file.write('link,home_page,category,child_category,count\n')
    for csv_file in os.listdir('stickpng'):
        with open('stickpng/{}'.format(csv_file), 'r') as csv_file:
            for line in csv_file:
                link = line.split(',')[0].strip()
                link = link[1:link.find('?')]
                if ((link.startswith('https://www.stickpng.com/cat/')) and (len(link.split('/')) == 6)):
                    child_cat = link.split('/')[-1]
                    cat = link.split('/')[-2]
                    file.write('{},stickpng.com,{},{},\n'.format(link, cat, child_cat))
                else:
                    if len(link.split('/')) > 6:
                        print(link)
    file.write('https://www.stickpng.com/cat/bots-and-robots,stickpng.com,bots-and-robots,bots-and-robots,')
