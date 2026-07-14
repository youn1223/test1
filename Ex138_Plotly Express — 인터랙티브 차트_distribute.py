# pip install plotly 

import duckdb
import plotly.express as px
# pip install plotly

# import plotly.io as pio  # 1. 렌더러 모듈 임포트

# # ★ [해결책] 그래프를 VS Code 내부 탭이나 인터랙티브 창에서 열리도록 강제 설정
# pio.renderers.default = "vscode"

import polars as pl
# 1. 파일 읽기
print(pl.scan_parquet("data/large_sales_data.parquet").head(5).collect())
###################################################
# data/large_sales_data.parquet 파일 생성하는 코드 
import polars as pl
import numpy as np
import datetime
import os

# 2. 랜덤 데이터 생성 (1,000건)
n_rows = 1000
start_date = datetime.datetime(2025, 1, 1)

data = {
    "order_date": [start_date + datetime.timedelta(days=int(i/3), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60)) for i in range(n_rows)],
    "revenue": np.random.randint(10000, 500000, size=n_rows)
}

# 3. Polars 데이터프레임 생성 및 Parquet 저장
df = pl.DataFrame(data)
df.write_parquet("data/large_sales_data_Ex138.parquet")

print("성공적으로 'data/large_sales_data.parquet_Ex138' 파일을 생성했습니다!")
print(df.head(5))
###################################################

print("1. DuckDB를 통해 대용량 Parquet 파일 분석 중...")

query_result = duckdb.execute("""
    SELECT 
        strftime(order_date, '%Y-%m') AS order_month,
        SUM(revenue) AS total_revenue
    FROM 'data/large_sales_data_Ex138.parquet'
    GROUP BY order_month
    ORDER BY order_month
""").df()

print("\n--- [집계 결과 데이터프레임 확인] ---")
print('query_result')
print(query_result)
print("------------------------------------\n")

fig = px.line(
    query_result, 
    x="order_month", 
    y="total_revenue",
    title="월별 총 매출 추이 (Plotly Express)",
    labels={
        "order_month": "주문 월 (Year-Month)", 
        "total_revenue": "총 매출액 (원)"
    },
    markers=True 
)

fig.update_traces(
    line_color="#2b5c8f",     # 차트 선 색상을 세련된 네이비 톤으로 변경
    line_width=3,             # 선 두께 3 두껍게
    marker=dict(size=8) ,      # 마커 점 크기 확대
)

fig.update_layout(
    title_font_size=20,       # 제목 글자 크기
    hovermode="x unified",    # 마커에 마우스를 대면 x축 라인 전체 데이터를 묶어서 팝업 띄우기(팝업창에 해당 월의 1일을 임의로 붙여서 띄운다.)
    template="plotly_white"  # 깔끔한 화이트 테마 적용
)


fig.write_html("data/sales_chart.html")
print("그래프가 data/sales_chart.html 파일로 저장되었습니다!")
