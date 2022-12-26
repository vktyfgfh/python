import streamlit as st
import altair as alt
import pandas as pd

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

# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
