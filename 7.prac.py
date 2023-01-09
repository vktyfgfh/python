import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.relativedelta import *

now = datetime.now().date()
last_month = now+relativedelta(months=-1)
last_month = last_month.isoformat()
last_month = last_month[0:4]+last_month[5:7]

st.title('빅프로젝트_2022_DX_12조 🍎')
st.write('커넥트팜_')
st.text('팀_닿음')
st.image('https://img.freepik.com/premium-vector/farm-panorama_273525-19.jpg?w=1380')
st.write(' ')
st.write(' ')

# streamlit//data_subway_in_seoul.csv
# encoding='cp949'  읽어오고 확인하기 
df = pd.read_csv('raw_price.csv', encoding='cp949')

col1, col2 = st.columns(2)

with col1:
    # checkbox를 선택하면 원본 데이터프레임이 나타남
    if st.checkbox('원본 데이터 보기'):
        st.subheader('2018~2022 data')
        st.dataframe(df)
with col2:
    # button을 누르면 원본데이터 주소가 나타남
    if st.button('데이터 링크'):
        st.write('https://data.mafra.go.kr/opendata/data/indexOpenDataDetail.do?data_id=20141216000000000367')

st.subheader('전체 사과의 상·중품 비율')
df = df.astype({'경락일':'str'})
df = df[df['경락일'].str.contains(last_month, na = False)]
df['mass'] = df['농수축산물 거래 단량']*df['거래량']
st.text('((거래단량 x 거래량)상품 합계 + (거래단량 x 거래량)중품 합계 )/ 전체합계')

# 상중품 비율!!!
ratio = (df[df['grade']=='상품']['mass'].sum() + df[df['grade']=='중품']['mass'].sum()) / df['mass'].sum()
st.write('상중품 비율 ',ratio)

st.write(' ')
st.write(' ')
st.subheader('사과 생산량 데이터 ')
# 경북 사과 생산량 데이터 가져오기
df_output = pd.read_csv('Gyeongbuk total output.csv', encoding='cp949')
st.write('출처 : KOSIS 경북 사과 생산량')

# last_year = int(datetime.today().strftime('%Y'))-1
last_year = 2021

col1, col2 = st.columns(2)

with col1:
    st.text('작년 사과 총 생산량')
    output = df_output[df_output['경상북도']== last_year]['생산량 (톤)']  
    st.write(output)
with col2:
    st.text('작년 경북 사과 생산량 (kg)')
    output = df_output[df_output['경상북도']==last_year]['사과면적 (ha)'] * df_output[df_output['경상북도']==last_year]['10a당 생산량 (kg)'] * 10
    st.write(output)
    
st.write(' ')
st.subheader('잔존계수 산출')
gs = pd.read_csv('gyesoo.csv')
jv = pd.read_csv('java.csv')
st.write('KOSIS 사과 재배면적 규모별 농가 및 면적 Data')
jv.T
# 재배면적에 따른 분포 시각화
# altair mark_line 차트 그리기
chart = alt.Chart(jv).mark_bar().encode(
         x='재배면적', y='가구수').properties(width=650, height=350)
st.altair_chart(chart, use_container_width=True)
gs.T
st.write('시각화를 통해 대형, 중형, 소형농가 확인 (L = 2ha 이상, M = 1~2ha, S = 1ha 미만 * 통계청 기준)')
st.write('S 농가의 경우 잔존량이 거의 없고 소규모 거래가 주를 이루므로 가중치에서 제외 (L : M = 1 : 3) ')
st.write(' ')
k = (gs['잔존율'][0] + gs['잔존율'][1] + gs['잔존율'][2] + 
     (gs['잔존율'][3]*3/4 + gs['잔존율'][4]*1/4) + 
     (gs['잔존율'][5]*3/4 + gs['잔존율'][6]*1/4))/5
st.write(' ')
st.write('잔존계수 ',k) # 잔존계수  = k

# 작년 전체 농가 사과 예상 잔존량
# ratio : 상중품 비율
remain = float(k)
t_remain = int(output * remain * ratio)
st.write('경북예상잔존량:', t_remain)

st.write(' ')
st.write(' ')
st.subheader('농가면적 대비 잔존량')
st.text('경북사과잔존량 ')
# 특정 농가 예상 잔존량 구하기!!!
# 경상북도 시과 전체 농지
t_hr = df_output[df_output['경상북도']==last_year]['사과면적 (ha)']*100
farm_hr = st.number_input('농가면적을 입력하시기 바랍니다.(a)', step = 1)
f_remain = int(t_remain * farm_hr/t_hr)
st.write('농가예상잔존량 (kg) :', f_remain)

st.write(' ')
st.write(' ')
st.subheader('사과 적정가격 범위')

# # 상품
# tf1 = df[df['grade'] == '상품']
# tf1 = tf1[tf1.columns.difference(['품목명', '품종명', '등급 코드', '농수축산물 거래 단량',
#                                             '포장단위 규격명', '포장단위 규격', '거래량', '경락일',
#                                             'year', 'month', '경매건수(건)', '최소가(원)',
#                                             '평균가(원)', '최대가(원)', 'mass'])]
# tf1.rename(columns = {"price": "price_h"}, inplace = True)
# tf1 = tf1.groupby(tf1['datetime'].dt.strftime("%Y-%m-%d")).mean()


# # 중품    
# tf2 = df[df['grade'] == '중품']
# tf2 = tf2[tf2.columns.difference(['품목명', '품종명', '등급 코드', '농수축산물 거래 단량',
#                                             '포장단위 규격명', '포장단위 규격', '거래량', '경락일',
#                                             'year', 'month', '경매건수(건)', '최소가(원)',
#                                             '평균가(원)', '최대가(원)', 'mass'])]
# tf2.rename(columns = {"price": "price_m"}, inplace = True)
# tf2 = tf2.groupby(tf2['datetime'].dt.strftime("%Y-%m-%d")).mean()

# tf3 = pd.merge(tf1, tf2, how = 'left',on='datetime')
# tf3['price'] = (tf3['price_h'] + tf3['price_m'])/2

# # csv 파일로 저장
# tf3.to_csv("tf3.csv",encoding='cp949', mode='w', index = False )
tf3 = pd.read_csv('tf3.csv', encoding='cp949')

#도매가 평균
avg = (tf3['price'][-1:] + tf3['price'][-6:].mean())/2

# 적정가격 범위 
col1, col2, col3 = st.columns(3)

with col1:
    st.text('떨이가격')
    st.write(int(avg * 8/12))
with col2:
    st.text('도매가 평균')
    st.write(int(avg))
with col3:
    st.text('농가수취가')
    st.write(int(avg* 0.92))
    
#slider를 사용하여 구간 설정하기
s = st.slider('제안하는 사과 적정가격 범위 ', 11000, 18000, (12369, 17069))
s1 = st.slider("희망 판매 가격을 선택하세요", min_value=12369, max_value=17069, value=14719)


st.write(' ')
st.write(' ')
st.subheader('최대 판매 가능량')
st.write('최대 판매 가능량은 :', f_remain, '(kg) 입니다')
s_vol = st.number_input('희망판매량을 입력하시기 바랍니다.(kg)', step = 1, max_value = f_remain)

st.write(' ')
st.write(' ')
st.subheader('농가 예상수익')
st.text('범위 내 설정가격 x 농가예상잔존량')
s2 = int(s1 * s_vol)
st.write('예상수익 =',s2, '￦')


# df['price'] = round(df['평균가(원)']/df['농수축산물 거래 단량']*10)
# df['datetime'] = df['경락일'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
# tf5 = df[df.columns.difference(['품목명', '품종명', '등급 코드', '농수축산물 거래 단량',
#                                             '포장단위 규격명', '포장단위 규격', '거래량', '경락일',
#                                             '경매건수(건)', '최소가(원)',
#                                             '평균가(원)', '최대가(원)', 'grade', 'mass'])]
# tf5 = tf5.groupby(tf5['datetime'].dt.strftime("%Y-%m-%d")).mean()
tf5 = pd.read_csv('tf5.csv', encoding='cp949')
tf5 = tf5[-6:]
st.write(' ')
st.write(' ')
st.subheader('평균도매가격 일주일 데이터')
tf5.T

# altair mark_line 차트 그리기
chart = alt.Chart(tf5).mark_line().encode(
         x='datetime', y='price').properties(width=650, height=350)
st.altair_chart(chart, use_container_width=True)

# sidebar- with 사용하기
with st.sidebar:
    st.header('[AIVLE_]')

add_selectbox = st.sidebar.selectbox(
     '조원 소개',
     ('강하라', '서경원', '심민수', '조광현', '김정민')
)

if add_selectbox == '강하라':
    st.sidebar.title('🧸')
    st.sidebar.write('엑셀 여신')
    st.sidebar.write('그룹내최고미녀')
    st.sidebar.write('정민담당일진')
    st.sidebar.write('12조왕언니')
elif add_selectbox == '서경원':
    st.sidebar.title('🍀')
    st.sidebar.write('소통의神')
    st.sidebar.write('먹잘알척척박사님')
    st.sidebar.write('개인기 본좌')
    st.sidebar.write('먹선생')
    st.sidebar.write('한입사냥꾼')
    st.sidebar.write('쩝쩝..아니척척박사')
    st.sidebar.write('떴다먹선생')
elif add_selectbox == '심민수':
    st.sidebar.title('📝')
    st.sidebar.write('ENTJ그잡채')
    st.sidebar.write('케이시가 좋아..')
    st.sidebar.write('위스키믈리에(비전문가)')
    st.sidebar.write('쌍화탕이피료해..☆')
elif add_selectbox == '조광현':
    st.sidebar.title('📱')
    st.sidebar.write('인심좋은배곧주인장')
    st.sidebar.write('덩킨도넛터줏대감')
    st.sidebar.write('대한민국수도배곧으로기억할사람')
    st.sidebar.write('언어의마술사람')
    st.sidebar.write('배곧홍보대사S2')
else:
    st.sidebar.title('🎶')
    st.sidebar.write('올라운더갓정민')
    st.sidebar.write('ㄴㅇㄱ')
    st.sidebar.write('밈(Meme)잘알')
    st.sidebar.write('버스정류장절대강자')
    st.sidebar.write('뉴진스가너무좋은ditto좌♥')
