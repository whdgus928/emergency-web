import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','약수터.csv')

st.set_page_config(
    page_title = "위기 대응 플랫폼",
    layout = 'wide'
)
# 📜

st.header("🧺우물,약수터 위치 정보 조회")
st.write("좌측에서 위치 정보를 선택하여 가까운 우물과 약수터 위치를 확인하세요!🙏")
df = pd.read_csv(data_path)

do=list(df['시도'].unique())
do.sort()
cd_nm = st.sidebar.selectbox('시도 선택',do)
si=list(df[df['시도'] == cd_nm]['시군구'].unique())
si.sort()
sgg_nm = st.sidebar.selectbox('시군구 선택',si)
df = df[(df['시도'] == cd_nm) & (df['시군구'] == sgg_nm)].reset_index(drop = True)


st.write(df.reset_index(drop = True))


#구글맵에서 위도경도 추출하는 프로그램 개발
