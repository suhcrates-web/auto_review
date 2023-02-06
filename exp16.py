import re
a = 'http://news.donga.com/BestClick/3/all/20230203/117718407/1'

print(re.findall(r'(?<=/)\d+(?=/)',a))