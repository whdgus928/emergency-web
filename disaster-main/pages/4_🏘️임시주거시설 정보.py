import streamlit as st
import pandas as pd
import numpy as np
import os
import folium
from folium.plugins import MarkerCluster
# pip install streamlit-folium 관리자권한 아나콘다
from streamlit_folium import st_folium

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','이재민 임시주거시설 정보.csv')

st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)


st.header("🏘️임시주거시설 정보")
st.write("좌측에서 위치 정보를 선택하고 지도를 확대하면서, 가까운 임시주거시설 정보를 찾으세요🙏")
df = pd.read_csv(data_path)


cd_nm = st.sidebar.selectbox('시도 선택',list(df['시도명'].unique()))
sgg_nm = st.sidebar.selectbox('시군구 선택',list(df[df['시도명'] == cd_nm]['시군구명'].unique()))
df = df[(df['시도명'] == cd_nm) & (df['시군구명'] == sgg_nm)]



col1, col2 = st.columns(2)
with col1:
    # 지도 시각화
    mapping_data = df[['위도','경도','시설명', '상세주소', '시설면적', '주거능력']]

    m = folium.Map(
    location=[mapping_data['위도'].mean(), mapping_data['경도'].mean()],
    zoom_start= 10
    )
    coords = mapping_data[['위도', '경도','시설명', '상세주소','시설면적', '주거능력']] 
    marker_cluster = MarkerCluster().add_to(m)
    for idx in coords.index:
        # popup 크기 설정
        text = coords.loc[idx,'시설명'] + '<br>상세주소 : ' + str(coords.loc[idx,'상세주소']) +'<br>시설면적 : ' + str(coords.loc[idx,'시설면적']) + '<br>주거능력 : ' + str(coords.loc[idx,'주거능력'])
        folium.Marker([coords.loc[idx,'위도'], coords.loc[idx,'경도']], icon = folium.Icon(color="purple"), tooltip = text).add_to(marker_cluster)
        
    st_map = st_folium(m , width=700, height=450, returned_objects=[])

    
with col2 :
    st.write(df.drop(columns = ['시도명', '시군구명', '경도','위도']).reset_index(drop = True))




    
