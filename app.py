from flask import Flask, render_template, url_for, request, redirect, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from database import cursor, db
import binascii, codecs
import mysql.connector
import os, glob
from make_review import make_review
import random
import time

app = Flask(__name__)

#
# @app.route(f'/donga/df_review/', methods=['GET'])
# def index():
#     return render_template('index.html')


@app.route(f'/donga/df_review/', methods=['GET'])
def index_brod():
    now = datetime.today()
    try:

        config = {
            'user': 'root',
            'password': 'Seoseoseo7!',
            'host': 'localhost',
            'port': '3306'
        }

        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        article = "<br><br>최근 10분내 작성 보고 없음<br><br><br>"
        date0 = '123'
        return render_template('sihwang.html', article=article, now=date0, id_0='asdf', state='asdf', state_m='asdf')

    except:
        article = "<br><br>새로고침 하세요<br><br><br>"
        # date0 = now.strftime("%Y년 %m월 %d일 // %H시 %M분")
        date0 = now.strftime(
            "%Y년 %m월 %d일 // %H시 %M분".encode('unicode-escape').decode()
        ).encode().decode('unicode-escape')
        return render_template('sihwang.html', article=article, now=date0, id_0='asdf', state='asdf', state_m='asdf')

@app.route('/file_upload', methods=('POST',))
def upload():
    if request.method == 'POST':
        list_0 = glob.glob(f'data/*')
        for i in list_0:
            file_name = os.path.basename(i)
            os.remove(f"data/{file_name}")

        f = request.files['file']
        # f.save("./data/"+ secure_filename(f.filename))
        file_name = str(round(random.random()*100000))
        print(f"file_name: {file_name}")
        f.save(f"./data/{file_name}")
        loop = True
        while loop:
            time.sleep(1)
            list_0 = glob.glob(f'data/*')
            print(list_0)
            for i in list_0:
                print(os.path.basename(i))
                if file_name == os.path.basename(i):
                    loop = False

    return redirect(f'/donga/df_review/')

@app.route('/make_review', methods=['POST'])
def si_post():
    if request.method == 'POST':

        print('fuck')
        cmd = request.form['cmd']
        print(cmd)
        state = request.form['state']
        version = request.form['version']

        text00 = make_review()
        text00 = text00.replace('\n','<br>')
        print(text00)

        # if cmd == 'giveme':
        #     if version == '1':
        #         jong_time = 'jonghap_time'
        #     elif version == '2':
        #         jong_time = 'jonghap_time2'
        #
        #     now = datetime.today()
            # ago = time_checker(brod) or (now- timedelta(minutes=3))
            # ago = datetime.strptime(ago, '%Y-%m-%d %H:%M:%S')
            # if (now - ago) < timedelta(minutes=2):  # 2분미만
            #     message = "다른 사람이 작성중이거나 최근 작성 2분 미만입니다…좀만 기다려보세요"
            #     cmd = 'not_yet'
            #     time = ''
            # else:
            #     config = {
            #         'user': 'root',
            #         'password': 'Seoseoseo7!',
            #         'host': 'localhost',
            #         # 'database':'shit',
            #         'port': '3306'
            #     }
            #
            #     db = mysql.connector.connect(**config)
            #     cursor = db.cursor()
            #
            #     message = checkers_dic[brod]()
            #     cursor.execute(
            #         f"""update dangbun_stuffs.brods set date0 = "{now}" where brod="{brod}" """
            #     )
            #     cursor.execute(
            #         f"""update dangbun_stuffs.brods set content = b'{bin(int(binascii.hexlify(message.encode('utf-8')), 16))[2:]}' where brod="{brod}" """
            #     )
            #     db.commit()
            #     cmd = 'ok'

        return {"message": text00, "cmd": 'ok'}



#잘못들어갈때
@app.route(f'/donga/dangbun/naver/', methods=['GET'])
def mistake1():
    return redirect('http://testbot.ddns.net:5235/donga/dangbun/naver/only')



if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    # host = '0.0.0.0'
    if port == '5232':
        host = '172.30.1.58'
        host = '0.0.0.0'

    elif port == '5231':
        port = '5234'
        host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
