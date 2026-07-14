import streamlit as st # pip install streamlit 
import duckdb
import plotly.express as px

# 실행방법 : streamlit run 파일명

# 1. 스트림릿 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="매출 대시보드", layout="wide") # layout="wide" 화면 넓게 나온다.
st.title("실시간 월별 매출 분석 대시보드")
st.write("DuckDB와 Plotly를 활용한 100만 건 대용량 데이터 시각화 결과입니다.")

# 2. 데이터 가져오기 (캐싱 처리로 속도 최적화)
@st.cache_data 
def load_data():
    return duckdb.execute("""
        SELECT 
            strftime(order_date, '%Y-%m') AS order_month,
            SUM(revenue) AS total_revenue
        FROM 'data/large_sales_data.parquet'
        GROUP BY order_month
        ORDER BY order_month
    """).df()

query_result = load_data()
print('query_result')
print(query_result)

# 3. 화면을 반으로 쪼개서 (왼쪽: 표, 오른쪽: 그래프) 배치
col1, col2 = st.columns(2)

with col1:
    st.subheader("월별 데이터 요약")
    st.dataframe(query_result, use_container_width=True)

with col2:
    st.subheader("매출 추이 시각화")
    fig = px.line(query_result, x="order_month", y="total_revenue", markers=True)
    st.plotly_chart(fig, use_container_width=True)
