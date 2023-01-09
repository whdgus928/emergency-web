import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os
import datetime

def droughtvalue(code):
    dt_now = datetime.datetime.now()
    date=str(dt_now.date()).replace('-','')
    date=int(date)-1
    
    #SPI 가뭄지수정보
    url=f'http://223.130.129.189:9191/getAnalsInfoList/pageNo=1&numOfRows=10&hjdCd={code}&stDt={date}&edDt={date}'
    response = requests.get(url)
    content = response.text

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')

    row_list = [] # 행값
    name_list = [] # 열이름값
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
    df = pd.DataFrame(row_list, columns=name_list)
    return df

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','행정코드.csv')

st.set_page_config(
    page_title = "위기 대응 플랫폼",
    layout = 'wide'
)
# 📜

st.header("📢가뭄 지수 정보 조회")
st.write("좌측에서 위치 정보를 선택하여 해당 지역의 가뭄 지수 정보를 조회하세요!🙏")
st.write("*어제 기준으로 정보가 제공됩니다.")
df = pd.read_csv(data_path)
do=list(df['도시'].unique())
do.sort()
cd_nm = st.sidebar.selectbox('시도 선택',do)
si=list(df[df['도시'] == cd_nm]['시군구'].unique())
si.sort()
sgg_nm = st.sidebar.selectbox('시군구 선택',si)
df = df[(df['도시'] == cd_nm) & (df['시군구'] == sgg_nm)].reset_index(drop = True)
code=df.loc[0,'cd']

drought_df=droughtvalue(code)
drought_df.rename(columns={'anldt':'날짜','anlrst':'분석결과','anlval':'분석값','dv':'분석구분','hjdcd':'행정코드'},inplace=True)
#drought_df=drought_df[['날짜','분석값','분석결과','분석구분']]
st.write(drought_df.reset_index(drop = True))
