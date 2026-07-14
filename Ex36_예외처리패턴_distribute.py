
import pandas as pd

dirty_data = {
    "id": [101, 102, 103, 104],
    "score": ["8.5", "결측(Error)", "90", 75] 
}


df = pd.DataFrame(dirty_data)
print('df:\n',df)
print()


dead_letter_queue = []
valid_rows = []

print("===== 파이프라인 데이터 처리 시작 1 =====")
for index, row in df.iterrows(): 
    print(index) 
    print(row)
    try:
        clean_score = int(row["score"])
        valid_rows.append({"id": row["id"], "score": clean_score})
    except:
        print('except',index) 
        pass

print('valid_rows 1')
print(valid_rows)
print('------------------------------------------------')
print()

dirty_data = {
    "id": [101, 102, 103, 104],
    "score": ["8.5", "결측(Error)", "90", 75] 
}
df = pd.DataFrame(dirty_data)

dead_letter_queue = []
valid_rows = []

print("===== 파이프라인 데이터 처리 시작 2 =====")
for index, row in df.iterrows(): 
    try:

        clean_score = int(row["score"])
        valid_rows.append({"id": row["id"], "score": clean_score})
        
    except (ValueError, TypeError) as e:
        print('except',index)
        print(f"[WARNING] 인덱스 {index}번 데이터 오류 발견! DLQ로 격리합니다.")
        dead_letter_queue.append({
            "index": index,
            "raw_data": row.to_dict(),
            "error_message": str(e)
        })
    
        print('str(e):',str(e))

# 2. 결과 확인
df_clean = pd.DataFrame(valid_rows)
df_dlq = pd.DataFrame(dead_letter_queue)

print("\n=====  파이프라인 처리 결과 =====")
print("--- [정상 처리된 데이터] ---")
print(df_clean)

print("\n--- [격리된 데드 레터 큐 (DLQ)] ---")
print(df_dlq)

print('---------------------------------------')



print('# 2. 재시도 메커니즘 (Retry Mechanism) 예제')
# 간혹 대용량 데이터를 저장하거나 외부 API를 호출할 때 일시적인 서버 불안정으로 실패할 수 있습니다. 
# 무작정 에러를 내지 않고 시간 간격을 두고 자동으로 재시도하는 패턴입니다.

import time
import random

def save_to_storage(df):
    """일시적인 에러를 시뮬레이션하는 저장 함수"""
    # if random.choice([True, False]): 
    is_server_down = random.choice([True, False]) 
   
    
   
    print(f"[주사위 결과] 서버 다운 여부: {is_server_down}")
    
    if is_server_down:  
        raise ConnectionError("💾 스토리지 서버 연결이 일시적으로 불안정합니다.") 
    print(" 파일이 성공적으로 안전하게 저장되었습니다!")

# 임의의 데이터프레임
df = pd.DataFrame({"id": [1, 2, 3], "score": [100, 200, 300]})

max_retries = 3  # 최대 재시도 횟수
backoff_time = 1  
print("=====  파일 저장 파이프라인 시작 =====")
for attempt in range(1, max_retries + 1): 
    try:
        save_to_storage(df)
        break  
        
    except ConnectionError as e: 
        print(f"[ 에러 발생] {e}")
        if attempt < max_retries: 
            print(f" [{attempt}/{max_retries}] 즉시 종료하지 않고, {backoff_time}초 후 다시 시도합니다...")
            time.sleep(backoff_time)

        else: 

            print(f"\n[ 파이프라인 최종 실패({attempt}/{max_retries})] 지정한 재시도 횟수를 초과했습니다. 담당자에게 알림을 보냅니다.")

