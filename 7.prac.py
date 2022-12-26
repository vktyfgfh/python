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

st.title('빅프로젝트')
st.header('_2021 AIVLE_DX트랙 12조 ')

# streamlit//data_subway_in_seoul.csv
# encoding='cp949'  읽어오고 확인하기 
df = pd.read_csv('raw_price.csv', encoding='cp949')

# button을 누르면 원본데이터 주소가 나타남
if st.button('Data link'):
    st.write('https://data.mafra.go.kr/opendata/data/indexOpenDataDetail.do?data_id=20141216000000000367')

# checkbox를 선택하면 원본 데이터프레임이 나타남
if st.checkbox('원본 데이터 보기'):
    st.subheader('기다려주세요 (_ _)')
    st.dataframe(df)
    
st.subheader('사과 상중품 비율 구하기')
df = df.astype({'경락일':'str'})
df = df[df['경락일'].str.contains(last_month, na = False)]
df['mass'] = df['농수축산물 거래 단량']*df['거래량']

# 상중품 비율!!!
ratio = (df[df['grade']=='상품']['mass'].sum() + df[df['grade']=='중품']['mass'].sum()) / df['mass'].sum()
st.write('상중품 비율 ',ratio)

st.subheader('예상 잔존량 구하기')
# 경북 사과 생산량 데이터 가져오기
df_output = pd.read_csv('Gyeongbuk total output.csv', encoding='cp949')

# 작년 경북 사과 생산량 
output = df_output[df_output['경상북도']==last_year]['사과면적 (ha)'] * df_output[df_output['경상북도']==last_year]['10a당 생산량 (kg)'] * 10
st.write('작년 경북 사과 생산량 ',output)


st.subheader('잔존계수 산출')
gs = pd.read_csv('gyesoo.csv',low_memory=False)
jv = pd.read_csv('java.csv',low_memory=False) # 출처 : KOSIS '사과 재배면적 규모별 농가 및 면적 2021-10-22'

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

st.subheader('농가면적 잔존량 INPUT')
# 특정 농가 예상 잔존량 구하기!!!
# 경상북도 시과 전체 농지
t_hr = df_output[df_output['경상북도']==last_year]['사과면적 (ha)']*100
farm_hr = int(input('농가면적을 입력하시기 바랍니다.(a)'))
f_remain = t_remain * farm_hr/t_hr
st.write('농가예상잔존량:', f_remain)

st.subheader('사과 적정가격 범위구하기')

# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
