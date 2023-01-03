import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import json
import os
from PIL import Image
from datetime import datetime
from dateutil.relativedelta import relativedelta

filePath, fileName = os.path.split(__file__)
# 페이지 기본 설정
st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)

#### 페이지 헤더, 서브헤더 제목 설정
# 헤더
st.header("⛔현재 가뭄 주의 상황")

def drought():

    dt_now = datetime.datetime.now()
    date=str(dt_now.date()).replace('-','')
    date=str(date)[:-2]

    now = datetime.now()
    before_one_month = now - relativedelta(months=1)
    before_one_month=str(before_one_month)[:7]
    
    
    url=f'http://223.130.129.189:9191/getInfoList/numOfRows=200&pageNo=1&_type=json&stDt={before_one_month}&edDt={date}'

    response = requests.get(url)
    json_ob = json.loads(response.content)
    body = json_ob['response']['body']['items']['item']
    df = pd.json_normalize(body)
    df=df[['sigunNm', 'frcstFarm', 'frcstFarmMsg', 'frcstLiv','frcstLivMsg']]
    df.rename(columns={'sigunNm':'시군','frcstFarm':'생활 및 공업용수 가뭄 정보','frcstFarmMsg':'생활 및 공업용수 가뭄메시지','frcstLiv':'농업용수 가뭄정보','frcstLivMsg':'농업용수 가뭄메시지'},inplace=True)
    life_df=df[df['생활 및 공업용수 가뭄 정보']!='정상']
    list=life_df['시군'].to_list()
 
    return list

try:
    list_=drought()
    if len(list_)!=0:
        text = ", ".join(list_)
        st.subheader("❗" + text)
except:
    st.subheader('현재 가뭄인 지역이 없습니다.')

st.write("해당 지역 거주자 분들은 단수 상황에 대비해 물을 절약해주시기 바랍니다.")

image = Image.open(os.path.join(filePath,'pages','using_data', '물절약.png'))
st.image(image)
