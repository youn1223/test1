
import polars as pl 
# pip install polars  
# pip install "polars[rtcompat]" 윗줄 에러나면 설치하자


q = pl.scan_csv("data/large_data.csv") # 10,000 명의 데이터

lazy_df = pl.DataFrame({
    'Region': ['Seoul', 'Seoul', 'Busan', 'Busan', 'Seoul', 'Busan'],
    'Gender': ['F', 'M', 'F', 'M', 'M', 'F'],
    'Score': [85, 92, 88, 95, 70, 60]
}).lazy() 


# 연산 계획 세우기 (필터링 후 그룹화하여 평균 내기)
query = (
    lazy_df 
    .filter(pl.col("Score") >= 70)                 # 70점 이상인 사람만 필터링 계획
    .group_by("Region")                            # 지역별 그룹화 계획
    .agg(pl.col("Score").mean().alias("Avg_Score")) # 점수 평균 계산 계획, 집계 및 이름 변경
)


print("--- 연산 계획 (Query Plan) ---")
print(query) 

print("\n" + "="*40 + "\n")

# collect()로 한 번에 연산 실행 및 메모리 로드
result = query.collect()

print("--- 최종 결과1 (DataFrame) ---")
print(result)
print()

print('-------------------------------------------')

# 1. 연산 계획 작성
query_2 = (
    q
    .filter(pl.col("Score") >= 70)
    .with_columns(
        ((pl.col("Age") // 10) * 10).alias("Age_Group")
    )
    .sort("Score", descending=True) # 점수 내림차순 정렬
)

# 2. 계획서 출력해보기
print("=== 1. 일반 계획서 (내가 쓴 코드 순서) ===")
print(query_2) 
print("\n" + "="*50 + "\n")


result = query_2.collect()

print("--- 최종 결과2 (DataFrame) ---")
print(result)
print()
