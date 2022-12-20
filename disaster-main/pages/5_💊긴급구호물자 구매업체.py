import streamlit as st
import pandas as pd
import numpy as np
import os

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','구호물자정보.csv')

st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)

st.header("💊긴급구호물자 구매업체")
st.write("좌측에서 위치 정보를 선택하여 가까운 구매업체를 찾으세요🙏")
df = pd.read_csv(data_path)

cd_nm = st.sidebar.selectbox('시도 선택',list(df['시도명'].unique()))
sgg_nm = st.sidebar.selectbox('시군구 선택',list(df[df['시도명'] == cd_nm]['시군구명'].unique()))
df = df[(df['시도명'] == cd_nm) & (df['시군구명'] == sgg_nm)]
st.write(df.reset_index(drop = True))