import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

def _donga_newspaper_db_maker():
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
        drop table if exists review_auto.donga_paper
        """
    )

    cursor.execute(
        """
        create table if not exists review_auto.donga_paper(
        title0 varchar(100),
        url varchar(100),
        real_title varchar(100)
        )
        """
    )
    url = 'https://www.donga.com/news'

    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')
    temp = temp.find('div', {'class':'paper_list'})

    cursor.execute(
        """
        select url, title0 from review_auto.donga_today
        """
    )
    compare_dic = {k:v for k,v in cursor.fetchall()}

    for a in temp.findAll('a'):
        title0 = a.text
        url_code = re.findall(r'(?<=/)\d+(?=/)', a['href'])
        xl_url = url_code[-2] + '/'+ url_code[-1]

        real_title0 = compare_dic[xl_url] if xl_url in [*compare_dic] else title0
        cursor.execute(
            f"""
            insert into review_auto.donga_paper values("{title0}", "{xl_url}", "{real_title0}") 
            """
        )
    db.commit()
# _donga_newspaper_db_maker()