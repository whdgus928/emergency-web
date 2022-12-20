import pandas as pd
df=pd.read_csv('C:\\Users\\user\\Desktop\\VS code\\disaster-main\\disaster-main\\pages\\using_data\\위도.csv',encoding='utf-8-sig')
df=df.dropna()
df=df.reset_index(drop=True)

from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')

# 위도, 경도 반환하는 함수
def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        return x_y

    except:
        return [0,0]

latitude = []
longitude =[]
j=0
for i in df['ADRES']:
    latitude.append(geocoding(i)[0])
    longitude.append(geocoding(i)[1])
    print(j)
    j+=1

df['위도']=latitude
df['경도']=longitude
df.to_csv('위도경도.csv',encoding='utf-8-sig')