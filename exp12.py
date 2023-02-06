from database import db, cursor
import datetime
import csv, re
import glob, os
import pandas as pd
import numpy as np
from collections import defaultdict

#### 파일에서 디지털스페셜 가져오기 ####

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
day0 = re.findall(r"\d+일",date0)[0]
week0 = re.findall(r"(?<=\().+?(?=\))",date0)[0]
jonghap0 = f"-{day0} {week0}요일"

######
ds_dics = {}  #디지털스페셜
ex_dics = {}  #그 외
ex_sosok_dics = {}  # ex_dics 의 소속부서 표시

for i in range(last_ind, len(ind_list)):
    line = df.iloc[i].to_list()
    if '디지털스페셜' in str(line[1]):
        ds_dics[line[2]] = []  # 제목을 key로
    else:
        ex_dics[line[2]] = []
        ex_sosok_dics[line[2]] = line[4]



### 네이버, 카카오, 동아 db 가져오기
# dics = defaultdict(list)

for site0 in ['naver','kakao','donga']:
    cursor.execute(
        f"""
        select title0, cv from review_auto.{site0}_one_two
        """
    )

    for title0, cv in cursor.fetchall():
        if title0 in [*ds_dics] and cv>10000:
            ds_dics[title0].append((site0,cv))

text0 = ''
corp_dic = {'naver':'네이버', 'kakao':'카카오', 'donga':'동아'}
for title0, content0 in ds_dics.items():
    text0 += '-' + title0 +'/ '
    for corp0, cv in content0:
        text0 += corp_dic[corp0]+f' {round(cv/10000)}만, '
    text0 = text0[:-2]+'\n'


text00 = ''
#### 디지털콘텐츠 발제 ###
title_list = [*ds_dics]
for title0 in title_list:
    crap = re.findall(r"(?<=\[).+?(?=\])",title0)
    if len(crap)>0:
        text00 += '-'+crap[0] +'\n'




######## 온라인 출고

for site0 in ['naver','kakao','donga']:
    cursor.execute(
        f"""
        select title0, cv from review_auto.{site0}_one_two
        """
    )

    for title0, cv in cursor.fetchall():
        if title0 in [*ex_dics] and cv>30000:
            ex_dics[title0].append((site0,cv))

text000 = ''
corp_dic = {'naver':'네이버', 'kakao':'카카오', 'donga':'동아'}
for title0, content0 in ex_dics.items():
    if content0 !=[]:
        text000 += '-'+ ex_sosok_dics[title0] +'/'+ title0 +'/ '
        for corp0, cv in content0:
            text000 += corp_dic[corp0]+f' {round(cv/10000)}만, '
        text000 = text000[:-2]+'\n'


##### 최종 텍스트 만들기 ####

final0 = \
    f"""
@@종합
{jonghap0}   
@디지털콘텐츠 편성표
{text0}
@디지털콘텐츠 발제
{text00}
@온라인 출고
{text000}
"""

print(final0)