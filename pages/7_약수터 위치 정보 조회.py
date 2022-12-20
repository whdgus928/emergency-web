import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','약수터.csv')

st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)
# 📜

st.header("🚑약수터 위치 정보 조회")
st.write("좌측에서 위치 정보를 선택하여 가까운 응급의료기관과 병실현황을 조회하세요!🙏")
df = pd.read_csv(data_path)

cd_nm = st.sidebar.selectbox('시도 선택',list(df['시도'].unique()))
sgg_nm = st.sidebar.selectbox('시군구 선택',list(df[df['시도'] == cd_nm]['시군구'].unique()))
df = df[(df['시도'] == cd_nm) & (df['시군구'] == sgg_nm)]
st.write(df.reset_index(drop = True))