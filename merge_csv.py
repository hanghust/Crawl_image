import pandas as pd

file1 = 'statistic_freepngimg.csv'
file2 = 'statistic_pngimg.csv'
file3 = 'statistic_pngmart.csv'
file4 = 'statistic_stickpng.csv'

csv1 = pd.read_csv(file1)
csv2 = pd.read_csv(file2)
csv3 = pd.read_csv(file3)
csv4 = pd.read_csv(file4)

total = pd.concat([csv1, csv2, csv3, csv4])
total.to_csv('statistic_4_websites.csv', index=False)
