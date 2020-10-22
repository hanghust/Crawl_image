import pandas as pd
import numpy as np
import os
def split_data(path):
    df = pd.read_csv(path)
    df = df.sample(len(df))
    msk = np.random.rand(len(df)) < 0.8
    df_train = df[msk]
    df_test = df[~msk]
    return df_train, df_test
def extract_name(s):
    return (s.split('/')[-1]).split('.')[0]
if __name__ == "__main__":
    path_os = '/home/hangnt/EDA_data_json/'
    # path = ['person_photo/', 'person_drawing/', 'animal_photo/', 'animal_drawing/']
    path = ['object_photo/', 'object_drawing/']
    # path = ['person_photo.csv', 'person_drawing.csv', 'animal_photo.csv', 'animal_drawing.csv']
    # path = ['object_photo.csv', 'object_drawing.csv']
    # for file in path:
    #     df_train, df_test = split_data(file)
    #     file_name = file.split('.')[0]
    #     path_source = path_os + file_name + '/'
    #     path_dirmv = path_os + file_name + '/' + file_name
    #     df_train.to_csv(file_name+'_train.csv', index=False)
    #     df_test.to_csv(file_name + '_test.csv', index=False)
    #     for img in df_train[file_name]:
    #         img = path_source + img.split('/')[-1]
    #         os.system("mv " + img + " " + path_dirmv + "_train/")
    #     for img in df_test[file_name]:
    #         img = path_source + img.split('/')[-1]
    #         os.system("mv " + img + " " + path_dirmv + "_test/")
    for path_file in path:
        path_ = path_os + path_file + path_file.split('/')[0]
        df_train = pd.read_csv(path_+'_train.csv')
        df_test = pd.read_csv(path_+'_test.csv')
        df_test[path_file.split('/')[0]]  =  df_test[path_file.split('/')[0]].apply(extract_name)
        np.savetxt(path_+'_test.txt', df_test[path_file.split('/')[0]], fmt='%s')
        np.savetxt(path_ + '_train.txt', df_train[path_file.split('/')[0]], fmt='%s')