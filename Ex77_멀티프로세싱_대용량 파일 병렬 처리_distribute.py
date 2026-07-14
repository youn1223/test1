

from multiprocessing import Pool, cpu_count
import os

# 각 프로세스가 처리할 워커(Worker) 함수
def process_chunk(file_positions):
    print('process_chunk=>')
    """
    file_positions: (파일경로, 시작위치, 읽을크기) 튜플
    """
    file_path, start_pos, chunk_size = file_positions
    print('file_positions')
    print(file_positions) # 
    print(file_path , '/', start_pos , "/", chunk_size)
    

    local_count = 0
    
    # 각 프로세스는 자신에게 할당된 위치로 이동(seek) 후 바이트 단위로 읽음
    with open(file_path, 'rb') as f:
        f.seek(start_pos)
        chunk_data = f.read(chunk_size).decode('utf-8', errors='ignore') 
    
        local_count = chunk_data.count("ERROR") # 29949

    return local_count

def get_file_chunks(file_path, chunk_size=1024 * 1024 * 64): 
    file_size = os.path.getsize(file_path)
    print('file_size:', file_size)
    chunks = []
    
    start_pos = 0
    while start_pos < file_size:
        print('start_pos:', start_pos)
        chunks.append((file_path, start_pos, chunk_size)) 
        start_pos += chunk_size

    print()
    print('chunks')
    print(chunks) 

    return chunks

if __name__ == "__main__":
    target_large_file = "huge_system_log.txt"
    
    # 1. 파일을 여러 조각(개념적 위치)으로 나눔
    chunks = get_file_chunks(target_large_file) 
    # chunks : # [('huge_system_log.txt', 0, 67108864), ('huge_system_log.txt', 67108864, 67108864)]
    
    # 2. 프로세스 풀을 CPU 코어 개수만큼 생성하여 병렬 처리
    print(f"작업 시작: {len(chunks)} 조각을 {cpu_count()}개의 코어로 분할 연산합니다.")

    with Pool(processes=cpu_count()) as pool: 
    
        results = pool.map(process_chunk, chunks) # process_chunk함수를 호출하면서 chunks에 있는 요소 하나 하나씩 넘깁니다. 에러가 포함된 문장 갯수를 리턴한다.
        
    print('results:', results)
    total_errors = sum(results)
    print(f"최종 분석 완료! 총 ERROR 발생 횟수: {total_errors}")
