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
last_month

st.title('빅프로젝트_2022_AIVLE_DX_12조')
st.header('🍎🍏 🍎🍎🍏🍏 🍎🍎🍎🍏🍏🍏 🍎🍎')
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
    if st.button('Data link'):
        st.write('https://data.mafra.go.kr/opendata/data/indexOpenDataDetail.do?data_id=20141216000000000367')

st.subheader('전체 사과의 상·중품 비율')
df = df.astype({'경락일':'str'})
df = df[df['경락일'].str.contains(last_month, na = False)]
df['mass'] = df['농수축산물 거래 단량']*df['거래량']
st.write('농수축산물 거래 단량 x 거래량 > 상품 합계 + 중품 합계 / 전체 합계')

# 상중품 비율!!!
ratio = (df[df['grade']=='상품']['mass'].sum() + df[df['grade']=='중품']['mass'].sum()) / df['mass'].sum()
st.write('상중품 비율 ',ratio)

st.write(' ')
st.write(' ')
st.subheader('예상 잔존량 구하기')
# 경북 사과 생산량 데이터 가져오기
df_output = pd.read_csv('Gyeongbuk total output.csv', encoding='cp949')
st.write('KOSIS 경북 사과 생산량 Data')

col1, col2 = st.columns(2)

with col1:
    st.text('작년 사과 총 생산량')
    last_year = int(datetime.today().strftime('%Y'))-1
    output = df_output[df_output['경상북도']== last_year]['생산량 (톤)']
    st.write(output)
with col2:
    st.text('작년 경북 사과 생산량 (kg)')
    output = df_output[df_output['경상북도']==last_year]['사과면적 (ha)'] * df_output[df_output['경상북도']==last_year]['10a당 생산량 (kg)'] * 10
    st.write(output)
    
st.write(' ')
st.write(' ')
st.subheader('잔존계수 산출')
gs = pd.read_csv('gyesoo.csv')
jv = pd.read_csv('java.csv')
st.write('KOSIS 사과 재배면적 규모별 농가 및 면적 Data')

# 재배면적에 따른 분포 시각화
# altair mark_line 차트 그리기
chart = alt.Chart(jv).mark_line().encode(
         x='재배면적', y='가구수').properties(width=650, height=350)
st.altair_chart(chart, use_container_width=True)

# altair mark_area 차트 그리기
chart = alt.Chart(jv).mark_area().encode(
         x='재배면적', y='가구수').properties(width=650, height=350)
st.altair_chart(chart, use_container_width=True)

# 시각화를 통해 대형, 중형, 소형 구분
# L = 2ha이상의 농가, M = 1~2ha 농가, S = 1ha 미만
# S 농가의 경우 잔존량이 거의 없고 소규모 거래이므로 가중치에서 제외
# M, L은 농가별 계수의 평균치

# L : M = 1 : 3이므로 가중치를 1/4, 3/4로 두어 평균치 계산.
k = (gs['잔존율'][0] + gs['잔존율'][1] + gs['잔존율'][2] + 
     (gs['잔존율'][3]*3/4 + gs['잔존율'][4]*1/4) + 
     (gs['잔존율'][5]*3/4 + gs['잔존율'][6]*1/4))/5
st.write('잔존계수 ',k) # 잔존계수  = k

# 작년 전체 농가 사과 예상 잔존량
# ratio : 상중품 비율
remain = float(k)
t_remain = output * remain * ratio
st.write('경북예상잔존량:', t_remain)

st.subheader('농가면적 대비 잔존량')
# 특정 농가 예상 잔존량 구하기!!!
# 경상북도 시과 전체 농지
t_hr = df_output[df_output['경상북도']==last_year]['사과면적 (ha)']*100
farm_hr = st.number_input('농가면적을 입력하시기 바랍니다.(a)')
st.write(farm_hr)
f_remain = t_remain * farm_hr/t_hr
st.write('농가예상잔존량 (kg) :', f_remain)

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
    st.write(avg * 8/12)
with col2:
    st.text('도매가 평균')
    avg
with col3:
    st.text('농가수취가')
    st.write(avg* 0.92)
    
#slider를 사용하여 구간 설정하기
values = st.slider(
    '범위로 나타낸 사과 적정가격 (빨간부분) ',
    11000, 18000, (12369, 17069))

s1 = st.slider("slider 1", min_value=12369, max_value=17069, value=14719)
st.write(f'예상수익 = {s1 * f_remain}')


# df['price'] = round(df['평균가(원)']/df['농수축산물 거래 단량']*10)
# df['datetime'] = df['경락일'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
# tf5 = df[df.columns.difference(['품목명', '품종명', '등급 코드', '농수축산물 거래 단량',
#                                             '포장단위 규격명', '포장단위 규격', '거래량', '경락일',
#                                             '경매건수(건)', '최소가(원)',
#                                             '평균가(원)', '최대가(원)', 'grade', 'mass'])]
# tf5 = tf5.groupby(tf5['datetime'].dt.strftime("%Y-%m-%d")).mean()
tf5 = pd.read_csv('tf5.csv', encoding='cp949')
tf5 = tf5['price'][-6:]
chart = alt.Chart(tf5).mark_line().encode(
         x='최근 일주일', y='가격').properties(width=650, height=350)
st.altair_chart(chart, use_container_width=True)

st.line_chart(tf5)
st.bar_chart(tf5)
st.area_chart(tf5)

# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
