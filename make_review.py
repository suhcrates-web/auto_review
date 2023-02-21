from database import db, cursor
import datetime
import csv, re
import glob, os
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import date, timedelta
import mysql.connector
from make_paper_review import make_paper_review


#### 파일에서 디지털스페셜 가져오기 ####
def make_review():
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    list_0 = glob.glob(f'data/*')
    file_list = []
    year_list = []
    file_dic = {}
    for i in list_0:
        file_name = os.path.basename(i).replace('.csv', '')
        file_list.append(file_name)

    df = pd.read_excel(f'data/{file_list[0]}', engine='openpyxl')
    df = df.dropna(subset=df.columns[[2]])  ## nan 을 제거

    # list0 = df.iloc[:,0].to_list()
    # for i in list0:
    #     print(type(i))

    ## 오늘 날짜인거 빼기 ##
    temp_list = df.iloc[:, 0].to_list()
    last_ind = [n for n, sch in enumerate(df.iloc[:, 0].to_list()) if type(sch) != float][-1]
    date0 = df.iloc[last_ind, 0]
    day0 = re.findall(r'\d+(?=일)', date0)[0]
    if str(date.today().day) == day0:  # 오늘날짜인게 있으면 잘라서 없앰.
        df = df.iloc[:last_ind, :]

    # 다시시작
    ind_list = df.iloc[:, 0].to_list()
    title_list = df.iloc[:, 2].to_list()
    total_num = len(df.iloc[:, 2].to_list())

    day_ind_list = [n for n, sch in enumerate(df.iloc[:, 0].to_list()) if type(sch) != float]
    last_ind = day_ind_list[-1]  # 마지막 날짜 (해당 날짜)  의 인덱스
    s_last_ind = day_ind_list[-2]  # 목록을 긁어와야 하는 날짜 (31일 기준 리뷰면 30일, 31일) 의 인덱스

    # total_num = len(ind_list) - last_ind
    # date0 = df.iloc[last_ind,0]
    # day0 = re.findall(r"\d+일",date0)[0]
    # week0 = re.findall(r"(?<=\().+?(?=\))",date0)[0]
    today0 = date.today() - timedelta(days=1)
    jonghap0 = f"-{today0.day}일 {['월', '화', '수', '목', '금', '토', '일'][today0.weekday()]}요일 총 {len(ind_list) - last_ind}건"

    ######
    ds_dics = {}  # 디지털스페셜.  # 이따가  포탈 해당일자에 나온거만 추려야 함
    ex_dics = {}  # 그 외
    ex_sosok_dics = {}  # ex_dics 의 소속부서 표시

    # 진짜제목 찾기
    cursor.execute(
        """
        select url, title0 from review_auto.donga_one_two
        """
    )
    title_finder = {re.findall(r'(?<=/)\d+(?=/)', k)[-1]: v for k, v in cursor.fetchall()}  # url:title0

    # print(title_finder)
    for i in range(s_last_ind, total_num):  #
        line = df.iloc[i].to_list()
        # print(line)
        if ('디지털스페셜' in str(line[1]) or '디지털콘텐츠' in str(line[1])) and '정치인&아웃' not in str(line[2]).replace(' ',''):
            # print(line[2])
            ds_dics[line[2]] = []  # 제목을 key로
        elif i >= last_ind:  # 디지털 스페셜 외의 기사는 s_last 가 아닌 last_ind 부터 적용돼야함. 이건 이후 수정
            # print(line[2])
            xl_url = re.findall(r'(?<=/)\d+(?=/)', line[3])[-1]
            if xl_url in [*title_finder]:  # 엑셀의 기사가 동아닷컴 조회수 순위에 있을 경우.
                title0 = title_finder[xl_url]
            else:  # 동아닷컴 조회수 순위에 없으면 그냥 엑셀 기사 제목을 붙임.
                title0 = line[2]
            ex_dics[title0] = {'corps': [], 'tot_cv': 0}
            ex_sosok_dics[title0] = line[4]

    ######## 네이버, 카카오, 동아 db 가져오기
    #####  디지털 콘텐츠 발제 중 네이버 혹은 카카오 해당일 출고된 거만 남겨놓기.
    #####  디지털 콘텐츠 중  편성표에 있는 거만 남겨놓기

    # 편성표 목록 가져오기
    cursor.execute(
        """
        select title_real from review_auto.편성표
        """
    )
    title_list = [x[0].replace(' ', '') for x in cursor.fetchall()]

    def title_checker(title0):
        title0 = title0.replace(' ', '')
        title0 = re.sub(r'\(.+\)', '', title0)
        for check in title_list:
            if check in title0:
                return True
        return False

    #### 포탈에서 '해당일'인거 가져오기
    portal_dic = {}
    ds_dics_temp = ds_dics
    ds_dics = {}
    print(today0)
    for site0 in ['naver', 'kakao']:
        cursor.execute(
            f"""
            select title0 from review_auto.{site0}_one_two where date0="{today0}"
            """
        )

        for title0 in cursor.fetchall():
            portal_dic[title0[0]] = 0
    # for title0 in ds_dics_temp:
    for title0 in portal_dic:
        # if title0 in [*portal_dic] and title_checker(title0):
        if title_checker(title0):
            ds_dics[title0] = {'corps': [], 'tot_cv': 0}

    ### 디지털 컨텐츠 조회수 짝짓기

    for site0 in ['naver', 'kakao', 'donga']:
        cursor.execute(
            f"""
            select title0, cv from review_auto.{site0}_one_two 
            """
        )

        for title0, cv in cursor.fetchall():
            if title0 in [*ds_dics] and cv > 10000:
                ds_dics[title0]['corps'].append((site0, cv))
                ds_dics[title0]['tot_cv'] += cv

    ds_dics = {k: v for k, v in sorted(ds_dics.items(), key=lambda item: item[1]['tot_cv'], reverse=True)}

    text0 = ''
    corp_dic = {'naver': '네이버', 'kakao': '다음', 'donga': '동아'}
    for title0, content0 in ds_dics.items():
        text0 += '-' + title0 + '/ '
        for corp0, cv in content0['corps']:
            text0 += corp_dic[corp0] + f' {str(round(cv / 10000, 1)).replace(".0", "")}만, '
        text0 = text0[:-2] + '\n'

    #####  디지털콘텐츠 발제 ###
    text00 = ''
    cursor.execute(
        f"""
        select title from review_auto.편성표 where day0 = "{['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'][(today0 + timedelta(days=1)).weekday()]}"
        """
    )
    for title0 in cursor.fetchall():
        text00 += '-' + title0[0] + '\n'

    ######## 온라인 출고

    for site0 in ['naver', 'kakao', 'donga']:
        cursor.execute(
            f"""
            select title0, cv from review_auto.{site0}_one_two
            """
        )

        for title0, cv in cursor.fetchall():
            if title0 in [*ex_dics] and cv > 30000:
                ex_dics[title0]['corps'].append((site0, cv))
                ex_dics[title0]['tot_cv'] += cv

    ex_dics = {k: v for k, v in sorted(ex_dics.items(), key=lambda item: item[1]['tot_cv'], reverse=True)}

    text000 = ''
    corp_dic = {'naver': '네이버', 'kakao': '다음', 'donga': '동아'}

    for title0, content0 in ex_dics.items():
        if content0['corps'] != []:
            text000 += '-' + ex_sosok_dics[title0] + '/' + title0 + '/ '
            for corp0, cv in content0['corps']:
                text000 += corp_dic[corp0] + f' {str(round(cv / 10000, 1)).replace(".0", "")}만, '
            text000 = text000[:-2] + '\n'

    #### 조간
    text0000 = make_paper_review()

    ##### 최종 텍스트 만들기 ####

    final0 = \
        f"""
    <{date.today().day}일 디프런티어센터>

    @@종합
    {jonghap0}   

    @디지털콘텐츠 편성표
    {text0}
    @디지털콘텐츠 발제
    {text00}
    @온라인 출고
    {text000}
    @{date.today().day}일 조간(오전 9시 반)
    {text0000}
    """
    return final0


