import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','단수사례.csv')

st.set_page_config(
    page_title = "위기 대응 플랫폼",
    layout = 'wide'
)
# 📜

st.header("❌전국 역대 단수 사례")
st.write("역대 단수 사례입니다.")
df = pd.read_csv(data_path)
st.write(df)

# do=list(df['시도명'].unique())
# do.sort()
# cd_nm = st.sidebar.selectbox('시도 선택',do)
# si=list(df[df['시도명'] == cd_nm]['시군구명'].unique())
# si.sort()
# sgg_nm = st.sidebar.selectbox('시군구 선택',si)
# df = df[(df['시도명'] == cd_nm) & (df['시군구명'] == sgg_nm)].reset_index(drop = True)

