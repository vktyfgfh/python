# streamlit, pandas 라이브러리 불러오기 
import streamlit as st
import pandas as pd

# header, subheader, text, caption 연습하기
st.title('Text elements')
st.caption('text 참고사이트: https://docs.streamlit.io/library/api-reference/text')

st.header('Heager : header')
st.subheader('subheader')
st.text('text text')
st.caption('Caption : streamlit born in 2019')


# markdown 연습하기
st.markdown('#AIVLE')
st.markdown('##AIVLE')
st.markdown('###AIVLE')
st.markdown('**_AIVLE_**')
st.markdown('-**_AIVLE_**')


# Latex & Code 연습하기
st.markdown('## Code & Latex')
st.code('a + ar + a r^2 + a r^3')
st.latex(r''' a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k =
a \left(\frac{1-r^{n}}{1-r}\right) ''') 


# write 연습하기
st.title('write')
st.caption('참고사이트: https://docs.streamlit.io/library/api-reference/write-magic/st.write')
st.text('아래 딕셔너리를 판다스 데이터프레임으로 변경')
st.caption("{'이름': ['홍길동', '김사랑', '일지매', '이루리'],'수준': ['금', '동', '은', '은']}")
df = pd.DataFrame({'first column': [1, 2, 3, 4],'second column': [10, 20, 30, 40]})
st.write('Below is a DataFrame:', df, 'Above is a dataframe.')


# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit \1.text.py