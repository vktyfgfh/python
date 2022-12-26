import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
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
    st.subheader('원본 데이터')
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
df_output = pd.read_csv('/content/drive/MyDrive/빅프로젝트_1/Gyeongbuk total output.csv', encoding='cp949')

# 작년 사과 총 생산량
last_year = int(datetime.today().strftime('%Y'))-1
output = df_output[df_output['경상북도']== last_year]['생산량 (톤)']
output

# 작년 경북 사과 생산량 ()
output = df_output[df_output['경상북도']==last_year]['사과면적 (ha)'] * df_output[df_output['경상북도']==last_year]['10a당 생산량 (kg)'] * 10
print('경북사과총생산량:', output)


st.subheader('잔존계수 산출')
gs = pd.read_csv('/content/drive/MyDrive/빅프로젝트_1/gyesoo.csv',low_memory=False)
jv = pd.read_csv('/content/drive/MyDrive/빅프로젝트_1/java.csv',low_memory=False) # 출처 : KOSIS '사과 재배면적 규모별 농가 및 면적 2021-10-22'


st.subheader('농가면적 잔존량 INPUT')
st.subheader('사과 적정가격 범위구하기')

# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
