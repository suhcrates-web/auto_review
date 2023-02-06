from database import db, cursor
import datetime
from collections import defaultdict

### 편성표 가져오기
week0 = ['mon','tue','wed','thu','fri','sat','sun']
week_day = week0[datetime.date.today().weekday()-1]
week_day2 = week0[datetime.date.today().weekday()-2]

cursor.execute(
    f"""
    select title_real from review_auto.편성표 where day0="{week_day}" or day0="{week_day2}"
    """
)

d_special = [x[0].replace(' ','') for x in cursor.fetchall()]

def check_dsp(title0):
    title0 = title0.replace(' ','')
    for i in d_special:
        if i in title0:
            return True
    return False



### 네이버, 카카오, 동아 db 가져오기
dics = defaultdict(list)

for site0 in ['naver','kakao','donga']:
    cursor.execute(
        f"""
        select title0, cv from review_auto.{site0}_one_two
        """
    )

    for title0, cv in cursor.fetchall():
        if check_dsp(title0):
            dics[title0].append((site0,cv))
        # dics[title0] = {'naver':cv}
    # print(dics)
print(dics)