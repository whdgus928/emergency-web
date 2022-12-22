#시설물코드
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import json
import pandas as pd
from datetime import datetime,timedelta
import warnings
import bs4
import xmltodict # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
warnings.filterwarnings('ignore')

url = 'http://apis.data.go.kr/B500001/drghtFcltyCode/fcltyList'
#for j in range():
    
params ={'serviceKey' : 'z5tZeY7iv8p2Ib1ApuO7q//wKERNpofeMjmWiun9zefOVRmdNnZkj9DCIiZoMTf3fhj6CEToyLj94bjSGZ4q4A==', 'pageNo' : '8', 'numOfRows' : '500', 'fcltyDivCode' : '1008' }

response = requests.get(url, params=params)
content = response.text

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')

row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

#xml값 DataFrame으로 만들기
df1 = pd.DataFrame(row_list, columns=name_list)

#print(df)
#corona_df.to_csv('정수장.csv',encoding='utf-8-sig')

df = pd.concat([df,df1], ignore_index=True)
df.to_csv('행정코드.csv',encoding='utf-8-sig')

print(df)