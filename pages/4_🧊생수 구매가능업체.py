import streamlit as st
import pandas as pd
import os
import folium
from folium.plugins import MarkerCluster
# pip install streamlit-folium 관리자권한 아나콘다
from streamlit_folium import st_folium


filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','구호물자정보.csv')

def shelter_map(data):
        m = folium.Map(
        location=[data['위도'].mean(), data['경도'].mean()],
        zoom_start= 7
        )
        marker_cluster = MarkerCluster().add_to(m)
        for idx in data.index:
                text = data.loc[idx, '업체명'] + '<br>상세주소 :' + data.loc[idx, '주소']
                folium.Marker([data.loc[idx, '위도'], data.loc[idx, '경도']], icon = folium.Icon(color="red"), tooltip = text).add_to(marker_cluster)
        return m

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

st.write(df.loc[:,['업체명',	'품목명',	'주소',	'대표전화번호']].reset_index(drop = True))
m = shelter_map(df)
st_folium(m , width=1400, height=700, returned_objects=[])
