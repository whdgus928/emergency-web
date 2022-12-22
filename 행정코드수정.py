import pandas as pd

df=pd.read_csv('C:\\Users\\user\\Desktop\\VS code\\행정코드.csv')

list=[]
for i in df.index:
    list=df.loc[i,'cdnm'].split(' ')
    df.loc[i,'도시']=list[0]
    df.loc[i,'시군구']=list[1]
    print(i)

df=df[['cd', '도시',   '시군구']]
df=df.drop_duplicates(['도시','시군구'],keep='first')
print(df)
df.to_csv('행정코드.csv',encoding='utf-8-sig',index=False)