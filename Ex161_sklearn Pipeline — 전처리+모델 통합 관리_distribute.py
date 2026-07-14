# sklearn Pipeline — 전처리+모델 통합 관리

# pip install scikit-learn

# type: ignore

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# 1. 예제 데이터 생성
data = pd.DataFrame({
    'age': [25, 30, None, 45],       # 수치형
    'city': ['Seoul', 'Busan', 'Seoul', 'Incheon'], # 범주형 
    'target': [0, 1, 0, 1] # 이진분류(제품구매/구매안함, 질병있음/질병없음, ...)
})
# Seoul에 사는 25세는 제품을 구매하지 않음(0)
# Busan에 사는 30세는 제품을 구매함(1)

# 2. 전처리 단계 분리
# 데이터가 통과할 처리 과정의 데이터 처리 절차의 설계도를 만드는 작업

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline : 어떤 단계(step)를 거쳐 처리가 되는지를 담는다. 리스트에 처리 단계를 담는다.

print('--------------------------------------------------------------------')

# 3. 전처리 적용 및 DataFrame 변환
processed_data = numeric_transformer.fit_transform(data[['age']]) 
print('processed_data')
print(processed_data)
print('--------------------------------------------------------------------')

# 4. 결과 출력
df_processed = pd.DataFrame(processed_data, columns=['age_scaled'])
print("--- 전처리 완료된 데이터 (DataFrame) ---")
print(df_processed)



# 범주형: 결측치 채우기 -> 원핫인코딩(OneHotEncoding)
categorical_features = ['city']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')), 
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
print('categorical_transformer')
print(categorical_transformer)
print('--------------------------------------------------------------------')

processed_data = categorical_transformer.fit_transform(data[['city']])


# 희소 행렬을 일반 numpy 배열로 변환
dense_data = processed_data.toarray() 

print("--- 0과 1이 다 보이는 행렬 ---")
print(dense_data)
# [[0. 0. 1.]
#  [1. 0. 0.]
#  [0. 0. 1.]
#  [0. 1. 0.]]

print('categorical_transformer processed_data')
print(processed_data)
# 'city': ['Seoul', 'Busan', 'Seoul', 'Incheon'],
# Coords        Values
#   (0, 2)        1.0
#   (1, 0)        1.0
#   (2, 2)        1.0
#   (3, 1)        1.0

print('--------------------------------------------------------------------')


# 3. ColumnTransformer로 통합
numeric_features = ['age']
categorical_features = ['city']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

print('ColumnTransformer preprocessor')
print(preprocessor)
print('--------------------------------------------------------------------')


# 4. 최종 Pipeline 구축 (전처리 + 모델)
from sklearn.linear_model import LogisticRegression
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier()) 
])


print('model_pipeline')
print(model_pipeline)
print('-----------------------------------------------------------')


# 5. 학습 (한 번의 fit으로 모든 과정 처리)
X = data.drop('target', axis=1)
y = data['target']
print('X:', X)
print('y:', y)
model_pipeline.fit(X, y)


predictions = model_pipeline.predict(X)
print("예측값:", predictions)

from sklearn.metrics import accuracy_score
score = accuracy_score(y, predictions)
print(f"모델 정확도: {score * 100:.2f}%")
print()
print("모델 파이프라인이 성공적으로 생성되고 학습되었습니다.")
print('-------------------------------')

# 새로운 데이터 
new_data = pd.DataFrame({
    'age': [22, 50, None, 35, 60, None], 
    'city': ['Busan', 'Incheon', 'Seoul', 'Daegu', 'Busan', 'Gwangju']
})

# 예측 수행
new_predictions = model_pipeline.predict(new_data)

print("새로운 데이터에 대한 예측값:", new_predictions)


new_probs = model_pipeline.predict_proba(new_data)
print("예측 확률 (0일 확률, 1일 확률):\n", new_probs)


# joblib으로 모델 저장·로딩
# joblib은 scikit-learn 모델(특히 대용량 배열을 포함하는 경우)을 파일로 저장하고 불러오는 데 최적화된 라이브러리
# 모델 학습을 완료한 후, 매번 다시 학습할 필요 없이 '학습된 모델을 파일로 보관'했다가 필요할 때 꺼내 쓸 수 있게 해준다.

import joblib


filename = 'data/model_v1.joblib'


# 모델 저장
joblib.dump(model_pipeline, filename) # model_pipeline : 최종 Pipeline
print(f"모델이 {filename}으로 저장되었습니다.")

import joblib

# 저장된 파일 불러오기
loaded_model = joblib.load('data/model_v1.joblib')


predictions = loaded_model.predict(new_data)
print("불러온 모델로 예측한 결과:", predictions)

