
# make_huge_shopping_logs_csv.py 실행해서 data/huge_shopping_logs.csv 먼저 만들고 시작하자
# make_large_sales_data_parquet.py 실행해서 data/make_large_sales_data.parquet 먼저 만들고 시작하자


import polars as pl
import matplotlib.pyplot as plt

# pip install matplotlib
# pip install seaborn
# pip install duckdb

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# 1. 대용량 파일 스캔 (Lazy API)
lazy_df = pl.scan_csv("data/huge_shopping_logs.csv") # 100만건 
# user_id,user_age,category,amount,order_date
# USER_015796,30,도서,73039,2026-04-02 15:56:37
# USER_000861,20,스포츠,93160,2025-09-28 19:37:20
# USER_038159,40,도서,8074,2026-02-03 17:54:45

# 2. Polars 엔진에서 미리 그룹화 및 평균 계산 (가벼운 데이터로 축소)
summary_df = (
    lazy_df
    .group_by("category")
    .agg(pl.col("amount").mean().alias("avg_amount"))
    .sort("avg_amount", descending=True)
    .collect() 
)
print('summary_df')
print(summary_df)
print()


# 3. Matplotlib으로 시각화
plt.figure(figsize=(10, 5))
plt.bar(summary_df["category"], summary_df["avg_amount"], color="skyblue")
plt.title("카테고리별 평균 구매 금액")
plt.xlabel("카테고리")
plt.ylabel("평균 금액 (원)")
plt.xticks(rotation=45)
# plt.show()
print('-----------------------------------------')

# 예: Seaborn으로 카테고리별 분할 그래프를 그릴 때
import seaborn as sns

# Pandas 데이터는 이 코드가 완벽하게 작동합니다.
sns.barplot(data=summary_df, x="category", y="avg_amount", hue="category") 

# 제목 추가
plt.title("Average Amount by Category")
# plt.show()
print('-----------------------------------------')

# 시계열(날짜) 데이터를 다룰 때
monthly_df = (
    lazy_df 
    .with_columns(pl.col("order_date").str.to_datetime())
    .sort("order_date") 
    .group_by_dynamic("order_date", every="1mo") 
    .agg(pl.col("amount").sum())
    .collect()
)

print('monthly_df:')
print(monthly_df)
print()

# Matplotlib 시계열 라인 플롯 시각화
plt.figure(figsize=(10, 5))
plt.plot(monthly_df["order_date"], monthly_df["amount"], marker='o', color='g', linestyle='-')

plt.title("월별 총 구매 금액 추이 (시계열)")
plt.xlabel("주문 월")
plt.ylabel("총 금액 (원)")
plt.grid(True, alpha=0.3)
# plt.show()

print('--------------------------------')
# DuckDB 연계한 데이터 시각화 예제

# make_large_sales_data_parquet.py 실행해서 data/make_large_sales_data.parquet 먼저 만들고 시작하자


import duckdb
import matplotlib.pyplot as plt

import polars as pl
import pandas as pd


print("--- Parquet 원본 데이터 상위 10줄 확인 방법1 ---")
duckdb.sql("SELECT * FROM 'data/large_sales_data.parquet' WHERE revenue >= 300000 LIMIT 10").show()
print("--------------------------------------\n")


con = duckdb.connect()


print("--- Parquet 원본 데이터 상위 10줄 확인 방법2 ---")
df_parquet = con.execute("SELECT * FROM 'data/large_sales_data.parquet' WHERE revenue >= 300000 LIMIT 10").df() 
print(df_parquet)

print("-------------------------------")

import polars as pl
import pandas as pd

df = pd.read_parquet("data/large_sales_data.parquet") 
print("read_parquet df:\n", df)

print('-------------------------')

query_result = con.execute("""
    SELECT 
        strftime(order_date, '%Y-%m') AS order_month, -- order_date 컬럼에 있는 정밀한 날짜 시간 데이터(예: 2025-01-15 14:30:22)를 연도와 월 형태의 문자열(예: 2025-01)로 추출하고, 이 컬럼의 이름을 order_month라고 부르겠다는 뜻입니다.
        SUM(revenue) AS total_revenue -- 각 월에 해당하는 revenue(매출) 값들을 전부 더한다.
    FROM 'data/large_sales_data.parquet'
    GROUP BY order_month -- 위에서 만든 order_month(년-월)를 기준으로 데이터를 그룹화(묶기)합니다.
    ORDER BY order_month
""").df()


print('query_result')
print(query_result)
print()

# 3. 전처리된 데이터를 바로 Matplotlib에 사용
plt.figure(figsize=(12, 5))
plt.plot(query_result["order_month"], query_result["total_revenue"], marker='o', color='red', linestyle='-')
plt.title("월별 총 매출 추이")
plt.xlabel("년-월")
plt.ylabel("총 매출 (억원)")
plt.grid(True, alpha=0.5)
plt.xticks(rotation=45)
# plt.show()
