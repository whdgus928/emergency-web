import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import datetime
import requests
import json
import os
from PIL import Image
from dateutil.relativedelta import relativedelta

filePath, fileName = os.path.split(__file__)
# 페이지 기본 설정
st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)

# st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# st.markdown("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
#   <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)



#### 페이지 헤더, 서브헤더 제목 설정
# 헤더
st.header("⛔현재 가뭄 주의 상황")

def drought():

    dt_now = datetime.datetime.now()
    date=str(dt_now.date()).replace('-','')
    date=str(date)[:-2]
    before_one_month = dt_now - relativedelta(months=1)
    before_one_month=str(before_one_month).replace('-','')[:6]

    url=f'http://223.130.129.189:9191/getInfoList/numOfRows=200&pageNo=1&_type=json&stDt={before_one_month}&edDt={date}'

    response = requests.get(url)
    json_ob = json.loads(response.content)
    body = json_ob['response']['body']['items']['item']
    df = pd.json_normalize(body)
    df=df[['sigunNm', 'frcstFarm', 'frcstFarmMsg', 'frcstLiv','frcstLivMsg']]
    df.rename(columns={'sigunNm':'시군','frcstFarm':'생활 및 공업용수 가뭄 정보','frcstFarmMsg':'생활 및 공업용수 가뭄메시지','frcstLiv':'농업용수 가뭄정보','frcstLivMsg':'농업용수 가뭄메시지'},inplace=True)
    정상=df[df['생활 및 공업용수 가뭄 정보']=='정상']['시군'].to_list()
    관심=df[df['생활 및 공업용수 가뭄 정보']=='관심']['시군'].to_list()
    주의=df[df['생활 및 공업용수 가뭄 정보']=='주의']['시군'].to_list()
    경계=df[df['생활 및 공업용수 가뭄 정보']=='경계']['시군'].to_list()
    
    return 정상, 관심, 주의, 경계

try:
    정상, 관심, 주의, 경계=drought()
    if len(관심)!=0:
        text ="관심 단계: "+ ", ".join(관심)
        st.subheader("❕ " + text)
    if len(주의)!=0:
        text ="주의 단계: "+ ", ".join(주의)
        st.subheader("❗ " + text)
    if len(경계)!=0:
        text ="경계 단계: "+ ", ".join(경계)
        st.subheader("‼ " + text)
except:
    st.subheader('현재 가뭄인 지역이 없습니다.')


st.write("해당 지역 거주자 분들은 단수 상황에 대비해 물을 절약해주시기 바랍니다.")

image = Image.open(os.path.join(filePath,'pages','using_data', '물절약.png'))
st.image(image)
