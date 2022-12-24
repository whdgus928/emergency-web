import streamlit as st
import pandas as pd
import requests
import pandas as pd
import bs4
import os
import json
import datetime

url='http://223.130.129.189:9191/getTsunamiShelter1List/numOfRows=1000&pageNo=1&type=json'
response = requests.get(url)
json_ob = json.loads(response.text)

body = json_ob['TsunamiShelter'][1]['row']
df = pd.json_normalize(body)
st.write(df)