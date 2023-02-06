import csv, re
import glob, os
import pandas as pd
import numpy as np
list_0 = glob.glob(f'data/*')
file_list = []
year_list = []
file_dic = {}
for i in list_0:
    file_name = os.path.basename(i).replace('.csv', '')
    file_list.append(file_name)

df = pd.read_excel(f'data/{file_list[0]}', engine='openpyxl')
# list0 = df.iloc[:,0].to_list()
# for i in list0:
#     print(type(i))
ind_list =  df.iloc[:,0].to_list()
last_ind = [n for n, sch in enumerate(df.iloc[:,0].to_list()) if type(sch) !=float][-1]

total_num = len(ind_list) - last_ind
date0 = df.iloc[last_ind,0]

for i in range(last_ind, len(ind_list)):
    line = df.iloc[i].to_list()
    if '디지털스페셜' in line[1]:
        print(line)

