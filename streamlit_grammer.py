# 사이드바
with st.sidebar:
    selected=option_menu(
        menu_title=None,
        options=['home','가뭄 상세 메시지','정수장 위치 및 실시간 유량','생수 구매 가능 업체','우물,약수터 위치 정보','응급의료기관 실시간 정보 조회','전국 역대 단수 사례'],
        icons=[]
    )

if selected=='home':
    home()
if selected=='가뭄 상세 메시지':
    가뭄상세메시지()
if selected=='정수장 위치 및 실시간 유량':
    정수장위치및실시간유량()
if selected=='생수 구매 가능 업체':
    생수구매가능업체()
if selected=='우물,약수터 위치 정보':
    우물약수터()
if selected=='응급의료기관 실시간 정보 조회':
    응급의료기관()
if selected=='전국 역대 단수 사례':
    전국단수()
