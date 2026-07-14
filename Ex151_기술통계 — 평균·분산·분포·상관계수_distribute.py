# 기술통계 — 평균·분산·분포·상관계수 
# [필요 라이브러리 설치] pip install pandas numpy matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (데이터 시각화 시 한글 깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우용 (맥은 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

print("1. 분석용 샘플 데이터셋 생성 중...")
# 분석을 위해 인위적으로 연관성이 있는 데이터 500건을 만듭니다.
np.random.seed(42)
n_samples = 500


area = np.random.normal(25, 8, n_samples).round(1) 
area = np.maximum(area, 1.0)

price = (area * 3000 + np.random.normal(0, 15000, n_samples) + 20000).round(-3) 
distance_subway = np.random.exponential(10, n_samples).round(1) 


df = pd.DataFrame({
    '아파트_평수': area,
    '매매가격_원': price,
    '지하철역_거리_분': distance_subway
})

print("\n--- [원본 데이터 상위 5건 확인] ---")
print(df.head())
print("----------------------------------")

print("\n2. 기술통계 정보 추출 (@describe 함수)")
descriptive_stats = df.describe()
print(descriptive_stats)

print(f"\n매매가격 평균: {df['매매가격_원'].mean():,.0f} 원")
print(f"매매가격 분산: {df['매매가격_원'].var():,.0f}")
print(f"매매가격 표준편차: {df['매매가격_원'].std():,.0f} 원")


print("\n3. 변수 간의 상관계수 행렬 계산 (@corr 함수)")
correlation_matrix = df.corr()
print('correlation_matrix')
print(correlation_matrix)

print("\n4. 데이터의 분포와 상관계수 시각화 창 띄우기...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# import seaborn as sns
sns.histplot(data=df, x='매매가격_원', kde=True, ax=axes[0], color='#2b5c8f')

axes[0].set_title('아파트 매매가격 분포 (오른쪽 꼬리가 긴 형태)')
axes[0].set_xlabel('매매 가격 (원)')

sns.heatmap(correlation_matrix, annot=True, cmap='RdBu_r', vmin=-1, vmax=1, ax=axes[1])

axes[1].set_title('변수 간 상관계수 히트맵 (Correlation Heatmap)')

plt.tight_layout()

plt.show()