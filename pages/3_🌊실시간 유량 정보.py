import streamlit as st
import pandas as pd
import requests
import os
import folium
import bs4
from folium.plugins import MarkerCluster
# pip install streamlit-folium 관리자권한 아나콘다
from streamlit_folium import st_folium
import datetime
from pytz import timezone

filePath, fileName = os.path.split(__file__)

def shelter_map(data):
        m = folium.Map(
        location=[data['위도'].mean(), data['경도'].mean()],
        zoom_start= 7
        )
        marker_cluster = MarkerCluster().add_to(m)
        for idx in data.index:
                text = data.loc[idx, '정수장'] + '<br>상세주소 :' + data.loc[idx, '주소']
                folium.Marker([data.loc[idx, '위도'], data.loc[idx, '경도']], icon = folium.Icon(color="red"), tooltip = text).add_to(marker_cluster)
        return m

def flux(df):
    dt_now = datetime.datetime.now(timezone('Asia/Seoul'))
    hour=dt_now.hour
    date=str(dt_now.date()).replace('-','')
    date=int(date)-1
    flux_df = pd.DataFrame()

    for i in df['정수장 코드']:
        url=f'http://223.130.129.189:9191/getWaterFlux/sujCode={i}&stDt={date}&stTm={hour}&edDt={date}&edTm={hour+1}'
        response = requests.get(url)
        content = response.text

        xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
        rows = xml_obj.findAll('item')
        name_list = [] # 열이름값
        row_list = [] # 행값
        value_list = [] #데이터값 
        
        for i in range(0, len(rows)):
            columns = rows[i].find_all()
            #첫째 행 데이터 수집
            for j in range(0,len(columns)):
                if i ==0:
                    # 컬럼 이름 값 저장
                    name_list.append(columns[j].name)
                # 컬럼의 각 데이터 값 저장
                value_list.append(columns[j].text)
            # 각 행의 value값 전체 저장
            row_list.append(value_list)
            # 데이터 리스트 값 초기화
            value_list=[]

        #xml값 DataFrame으로 만들기
        tmp_df = pd.DataFrame(row_list, columns=name_list)
        flux_df = pd.concat([flux_df,tmp_df],ignore_index=True)
        #corona_df.to_csv('정수장.csv',encoding='utf-8-sig')
    return flux_df
    
def main():
    st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide' 
    )

    st.header("🌊실시간 유량 정보")
    st.subheader("선택한 지역에 위치한 정수장 정보입니다.")
    data_path = os.path.join(filePath,'using_data','정수장코드.csv')
    df = pd.read_csv(data_path)
    
    sido_list = list(df['시도'].unique())
    sido_list.append('전국')
    #sido_list.insert(0, '전국')
    cd_nm = st.sidebar.selectbox('시도 선택',sido_list)
    if cd_nm != '전국':
        df = df[df['시도'] == cd_nm]
    df.reset_index(drop=True,inplace=True)
    #df: 지역별 정수장 정보
    st.write(df)
    m = shelter_map(df)
    st_folium(m , width=1400, height=700, returned_objects=[])
    flux_df=flux(df)
    #flux_df=flux_df[['fcltyNm','dataItemDesc','dataItemDiv','dataVal','itemUnit','occrrncDt']]
    #flux_df.rename(columns={'fcltyNm':'시설명','dataItemDesc':'자료 수집 설명','dataItemDiv':'데이터항목구분','dataVal':'유량','itemUnit':'측정단위','occrrncDt':'발생일시'},inplace=True)
    st.subheader(" 선택한 지역 정수장의 실시간 유량 정보입니다.")

    st.write(flux_df)
    
if __name__ == "__main__":
    main()
    
    

