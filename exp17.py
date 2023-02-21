import mysql.connector
import requests
from giveme_gija_name import giveme_gija_name
import time

def make_paper_review():

    config = {
            'user': 'root',
            'password': 'Seoseoseo7!',
            'host': 'localhost',
            # 'database':'shit',
            'port': '3306'
        }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    cursor.execute(
        """
        select real_title, url from review_auto.donga_paper
        """
    )

    paper_dics = {k: {'corps': [], 'tot_cv': 0, 'url':v, 'sosok':''} for k,v in cursor.fetchall()}


    for site0 in ['naver', 'kakao', 'donga']:
        cursor.execute(
            f"""
            select title0, cv from review_auto.{site0}_today
            """
        )

        for title0, cv in cursor.fetchall():
            if title0 in [*paper_dics] and cv > 30000:
                paper_dics[title0]['corps'].append((site0, cv))
                paper_dics[title0]['tot_cv'] += cv

    ex_dics = {k: v for k, v in sorted(paper_dics.items(), key=lambda item: item[1]['tot_cv'], reverse=True) if v['corps']!=[]}

    ## 소속 채우기
    cursor.execute(
        f"""
        select name0, sosok0 from review_auto.name_db
        """
    )
    name_to_sosok = {k:v for k,v in cursor.fetchall()}
    # print(name_to_sosok)
    for key0 in ex_dics:
        name0 = giveme_gija_name(ex_dics[key0]['url'])
        # print(name0)
        if name0 in [*name_to_sosok]:
            ex_dics[key0]['sosok'] = name_to_sosok[name0]
        else:
            ex_dics[key0]['sosok'] = "(소속 미확인)"
        time.sleep(1)

    text000 = ''
    corp_dic = {'naver': '네이버', 'kakao': '다음', 'donga': '동아'}

    for title0, content0 in ex_dics.items():
        if content0['corps'] != []:
            text000 += '-' + content0['sosok'] + '/' + title0 + '/ '
            for corp0, cv in content0['corps']:
                text000 += corp_dic[corp0] + f' {str(round(cv / 10000, 1)).replace(".0", "")}만, '
            text000 = text000[:-2] + '\n'
    return text000



# print(make_paper_review())