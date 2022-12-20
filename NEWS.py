import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import os
from PIL import Image
filePath, fileName = os.path.split(__file__)
# 페이지 기본 설정
st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)

#### 페이지 헤더, 서브헤더 제목 설정
# 헤더
st.header("⛔단수 특보 발령사항(최근 24시간 내)")


def flood_news(serviceKey, HydroType, DataType,Edt, DocumentType):
        url = f'https://api.hrfco.go.kr/{serviceKey}/{HydroType}/{DataType}/{Edt}{DocumentType}'
        response = requests.get(url)
        contents = response.text
        json_ob = json.loads(contents)
        body = json_ob['content']
        body = pd.json_normalize(body)
        return body

try :
    serviceKey = 'A3A7BEB0-361E-4134-878C-BD8004204558'
    HydroType = 'fldfct'
    DataType = 'list'
    # Edt = '20220810'
    DocumentType = '.json'
    Edt = datetime.today().strftime(("%Y%m%d"))
    df = flood_news(serviceKey, HydroType, DataType, Edt, DocumentType).drop(columns = 'links')
    df.columns = ['발표일시','발표자','수위도달 예상일시', '예상 수위표수위', '예상 해발수위', '홍수예보 종류', '홍수예보 번호', '지점', '기존발령일시', 
                '비고','강명','변동상황', '현재 일시', '현재 수위표수위', '현재 해발수위', '예상 일시(변동)', '예상 수위표수위(변동)', '예상 해발수위(변동)', '관측소 코드', '주의 지역', 
                '주의 강명']

    list_ = []
    for idx in df.index:
        if df.loc[idx,'홍수예보 종류'][-2:] == '발령':
            list_.append(df.loc[idx, '주의 지역'])
    warning_message = ",".join(list_)
    st.subheader("❗" + warning_message)
    st.write("해당 지역 거주자 분들은 혹시 모를 사태에 대비해주시기 바랍니다.")
    st.write(df)
    
    image = Image.open(os.path.join(filePath,'pages','using_data', '홍수발생시 요령.png'))
    st.image(image)
except :
    st.subheader("최근 24시간 내 발효된 홍수 특보 발령사항이 없습니다😊")
    image = Image.open(os.path.join(filePath,'pages','using_data', '홍수발생시 요령.png'))
    st.image(image)
    pass