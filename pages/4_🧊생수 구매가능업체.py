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

st.header("🧊생수 구매가능업체")
st.write("좌측에서 위치 정보를 선택하여 가까운 생수를 구매 가능한 마트를 찾으세요🙏")
df = pd.read_csv(data_path)


do=list(df['시도명'].unique())
do.sort()
cd_nm = st.sidebar.selectbox('시도 선택',do)
si=list(df[df['시도명'] == cd_nm]['시군구명'].unique())
si.sort()
sgg_nm = st.sidebar.selectbox('시군구 선택',si)
df = df[(df['시도명'] == cd_nm) & (df['시군구명'] == sgg_nm)].reset_index(drop = True)

st.write(df.reset_index(drop = True))