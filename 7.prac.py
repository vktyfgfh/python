import streamlit as st
import altair as alt
import pandas as pd

st.title('빅프로젝트')
st.header('_2021 AIVLE_DX트랙 12조 ')

# streamlit//data_subway_in_seoul.csv
# encoding='cp949'  읽어오고 확인하기 
df = pd.read_csv('streamlit//raw_price.csv', encoding='cp949')

# button을 누르면 원본데이터 주소가 나타남: https://www.data.go.kr/data/15044247/fileData.do
if st.button('data copyright link'):
    st.write('https://www.data.go.kr/data/15044247/fileData.do')

# checkbox를 선택하면 원본 데이터프레임이 나타남
if st.checkbox('원본 데이터 보기'):
    st.subheader('원본 데이터')
    st.dataframe(df)

# '구분' 컬럼이 '하차'인 데이터를 선택
# 새로운 데이터 프레임-에 저장 & 확인
df_off = df.loc[df['구분']=='하차']
# st.write('하차 데이터만 선별 ',df_off)


# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\7.prac_ans.py
