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


# streamlit//data_subway_in_seoul.csv
# encoding='cp949'  읽어오고 확인하기 
df = pd.read_csv('raw_price.csv', encoding='cp949')

# checkbox를 선택하면 원본 데이터프레임이 나타남
if st.checkbox('원본 데이터 보기'):
    st.subheader('2018~2022 data')
    st.dataframe(df)

# button을 누르면 원본데이터 주소가 나타남
if st.button('Data link'):
    st.write('https://data.mafra.go.kr/opendata/data/indexOpenDataDetail.do?data_id=20141216000000000367')

st.subheader('전체 사과의 상·중품 비율')
df = df.astype({'경락일':'str'})
df = df[df['경락일'].str.contains(last_month, na = False)]
df['mass'] = df['농수축산물 거래 단량']*df['거래량']
st.write('농수축산물 거래 단량 x 거래량')
st.write(" 상품 합계 + 중품 합계 / 전체 합계")

# 상중품 비율!!!
ratio = (df[df['grade']=='상품']['mass'].sum() + df[df['grade']=='중품']['mass'].sum()) / df['mass'].sum()
st.write('상중품 비율 ',ratio)


st.subheader('예상 잔존량 구하기')
# 경북 사과 생산량 데이터 가져오기
df_output = pd.read_csv('Gyeongbuk total output.csv', encoding='cp949')
st.write('KOSIS 경북 사과 생산량 Data')
col1, col2, col3 = st.columns(3)

with col1:
    st.text('A cat')
    st.image('https://static.streamlit.io/examples/cat.jpg')
    # 작년 사과 총 생산량
    last_year = int(datetime.today().strftime('%Y'))-1
    output = df_output[df_output['경상북도']== last_year]['생산량 (톤)']
    st.write('작년 사과 총 생산량 ',output)
with col2:
    st.text('A dog')
    st.image('https://static.streamlit.io/examples/dog.jpg')
    # 작년 경북 사과 생산량 
    output = df_output[df_output['경상북도']==last_year]['사과면적 (ha)'] * df_output[df_output['경상북도']==last_year]['10a당 생산량 (kg)'] * 10
    st.write('작년 경북 사과 생산량 (kg)',output)
with col3:
    st.text('An owl')
    st.image('https://static.streamlit.io/examples/owl.jpg')


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
st.write('입력한 숫자입니다', farm_hr)
st.write('농가예상잔존량:', f_remain)

st.subheader('사과 적정가격 범위구하기')

# 상품
tf1 = df[df['grade'] == '상품']
tf1 = tf1[tf1.columns.difference(['datetime', 'price'])]
tf1.rename(columns = {"price": "price_h"}, inplace = True)
st.dataframe(tf1)

# 중품    
tf2 = df[df['grade'] == '중품']
tf2 = tf2[tf2.columns.difference(['datetime', 'price'])]
tf2.rename(columns = {"price": "price_m"}, inplace = True)
tf2 = tf2.groupby(tf2['datetime'].dt.strftime("%Y-%m-%d"))

tf3 = pd.merge(tf1, tf2, how = 'left',on='datetime')
tf3['price'] = (tf3['price_h'] + tf3['price_m'])/2

#도매가 평균
avg = (tf3['price'][-1:] + tf3['price'][-6:].mean())/2
avg

# 적정가격 범위 
st.write(' 떨이가격 :', avg * 8/12)
st.write(' 농가수취가 :', avg* 0.92)

# slider를 사용하여 구간 설정하기
slider_date = st.slider(
    '가격 구간을 선택하세요 ',
    avg * 8/12, avg* 0.92,
    value=(avg * 8/12, avg* 0.92),
    )

# slider 날짜 구간으로 df를 읽어서 새 sel_df 으로 저장하고 확인하기
tf4 = tf3.loc[tf3['price'].between(avg * 8/12, avg* 0.92)]
st.dataframe(tf4)

st.title('Unit 5. Layouts & Containers')
st.caption('참조사이트: https://docs.streamlit.io/library/api-reference/layout')

# sidebar- with 사용하기 📧  📱  ☎︎
with st.sidebar:
    st.header('1. Sidebar')

add_selectbox = st.sidebar.selectbox(
     '어떻게 연락 드릴까요?',
     ('Email', 'Mobile phone', 'Office phone')
)

if add_selectbox == 'Email':
    st.sidebar.title('📧')
elif add_selectbox == 'Mobile phone':
    st.sidebar.title('📱')
else:
    st.sidebar.title('☎︎')



    
# tabs  
st.header('3. Tabs')
tab1, tab2, tab3 = st.tabs(['고양이', '개', '부엉이'])

with tab1:
    st.caption('Cat')
    st.image('https://static.streamlit.io/examples/cat.jpg', width=200)

with tab2:
    st.caption('Dog')
    st.image('https://static.streamlit.io/examples/dog.jpg', width=200)

with tab3:
    st.caption('Owl')
    st.image('https://static.streamlit.io/examples/owl.jpg', width=200)


# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
