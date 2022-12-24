import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os
import json
import datetime

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'using_data','구호물자정보.csv')

st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide'
)

st.header("지진해일 긴급 대피소 목록")
st.write("사전에 집에서 가까운 지진해일 목록을 확인하시고 비상상황에 대피 하시기 바랍니다!🙏")


url='http://223.130.129.189:9191/getTsunamiShelter1List/numOfRows=1000&pageNo=1&type=json'
response = requests.get(url)
json_ob = json.loads(response.text)

body = json_ob['TsunamiShelter'][1]['row']
df = pd.json_normalize(body)
st.write(df)
