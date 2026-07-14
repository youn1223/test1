import pandas as pd

df = pd.read_csv("people.csv")

print(df)

df.to_csv("output.csv", index=False) 

print('------------------------')
import pandas as pd
import json    

# 읽기1
df = pd.read_json("people.json")
print(df) 
print(type(df))

# 읽기2
with open("people.json") as f:
    data = json.load(f)
print(data)
print(type(data)) # <class 'list'> 
print()

people = [
    {"name":"Kim2","age":20},
    {"name":"Lee2","age":30}
]

with open("people2.json","w") as f: 
    json.dump(people, f, indent=4)

print('-------------------------')
# parquet 예제
# pip install pandas pyarrow
import pandas as pd


df = pd.DataFrame({
    "name": ["Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"],
    "age": [20, 30, 40, 25, 35, 45, 28, 32, 50, 22],
    "city": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong", "Gyeonggi", "Jeju"]
})
print(df)

# Parquet 파일 저장
df.to_parquet("people.parquet", index=False) 
print("저장 완료!")

df = pd.read_parquet("people.parquet") 
print("read_parquet df:\n", df)

# 일부만 보기
print('df.head()')
print(df.head()) # 5개만 나온다. 
print()

# 칼럼만 보기
print('df.columns')
print(df.columns)
print()

print('df.dtypes')
print(df.dtypes)
print()


# 나이를 1씩 증가
df["age"] += 1

print(df)
print()

df.to_parquet("people_new.parquet", index=False)
df_new = pd.read_parquet("people_new.parquet") 
print("df_new:\n", df_new)
print()

df = pd.read_parquet(
    "people.parquet",
    columns=["name", "age"]
)

print(df)
print()
df = pd.read_csv("people3.csv") 

df.to_parquet("people_change.parquet", index=False)

print("CSV → Parquet 변환 완료!")

# Parquet → CSV 변환해서 보기 
import pandas as pd

df = pd.read_parquet("people_change.parquet")
print('people_change.parquet df\n', df)
print()

df.to_csv("people_change3.csv", index=False) 
print('people_change3.csv df\n', df)
print()

print("Parquet → CSV 변환 완료!")
print()

print('# 100만 건 데이터 생성')
df = pd.DataFrame({
    "id": range(1_000_000), 
    "score": range(1_000_000) 
})
print(df)
print()

# CSV 저장
df.to_csv("score.csv", index=False)

# Parquet 저장
df.to_parquet("score.parquet", index=False)

csv_df = pd.read_csv("score.csv") #이줄보다 
parquet_df = pd.read_parquet("score.parquet")

import os
import time

csv_size = os.path.getsize("score.csv") / (1024 * 1024)
parquet_size = os.path.getsize("score.parquet") / (1024 * 1024)

print("=====  저장 공간(용량) 비교 =====")
print(f"CSV 파일 크기     : {csv_size:.2f} MB")
print(f"Parquet 파일 크기 : {parquet_size:.2f} MB")
print(f"압축 효율         : Parquet이 약 {csv_size / parquet_size:.1f}배 더 작음")
print()
print("=====  읽기 속도(시간) 비교 =====")

# CSV 읽기 시간 측정
start_time = time.time()
csv_df = pd.read_csv("score.csv")
csv_time = time.time() - start_time
print(f"CSV 읽은 시간     : {csv_time:.4f} 초")

# Parquet 읽기 시간 측정
start_time = time.time()
parquet_df = pd.read_parquet("score.parquet")
parquet_time = time.time() - start_time
print(f"Parquet 읽은 시간 : {parquet_time:.4f} 초")

print(f"속도 차이         : Parquet이 약 {csv_time / parquet_time:.1f}배 더 빠름")
