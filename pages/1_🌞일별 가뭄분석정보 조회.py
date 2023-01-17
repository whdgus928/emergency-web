import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os
import json
import datetime
from dateutil.relativedelta import relativedelta

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
    
    life_df=df[df['생활 및 공업용수 가뭄 정보']!='정상']
    life_df=life_df[['시군','생활 및 공업용수 가뭄 정보','생활 및 공업용수 가뭄메시지']]
    
    farm_df=df[df['농업용수 가뭄정보']!='정상']
    farm_df=farm_df[['시군','농업용수 가뭄정보','농업용수 가뭄메시지']]
    print(farm_df)
    return life_df,farm_df

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','약수터.csv')

st.set_page_config(
    page_title = "위기 대응 플랫폼",
    layout = 'wide'
)
# 📜

st.header("🌞일별 가뭄분석정보 조회")

# df = pd.read_csv(data_path)

# cd_nm = st.sidebar.selectbox('시도 선택',list(df['시도'].unique()))
# sgg_nm = st.sidebar.selectbox('시군구 선택',list(df[df['시도'] == cd_nm]['시군구'].unique()))
# df = df[(df['시도'] == cd_nm) & (df['시군구'] == sgg_nm)]
# st.write(df.reset_index(drop = True))

try:
    st.subheader("전국에 물 용도별 가뭄정보입니다!🙏")

    life_df,farm_df=drought()
    st.write("생활 및 공업용수 가뭄 정보입니다.")
    st.dataframe(life_df.reset_index(drop = True))

    st.write("농업용수 가뭄정보입니다.")
    st.dataframe(farm_df.reset_index(drop = True))
except:
    st.subheader('현재 가뭄인 지역이 없습니다.')
