# httpx로 API 데이터 비동기 수집 예제

import asyncio
import httpx
import time


async def fetch_api_data(client, url):
    print(f"[요청] {url} 데이터 수집 시작")
    try:
        
        response = await client.get(url, timeout=5.0)
        
        if response.status_code == 200:
            print(f"[완료] {url} 수집 성공")
        
            return response.json()
        else:
            print(f"[실패] {url} 상태 코드: {response.status_code}")
            return None
            
    except httpx.HTTPError as exc:
        print(f"[에러] {url} 요청 중 예외 발생: {exc}")
        return None

# 2. 전체 수집 과정을 컨트롤하는 메인 함수
async def main():
    # 시뮬레이션을 위한 가상 API URL 리스트 (JSONPlaceholder 사용)
    urls = [
        f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)
        # userId	1
        # id	1
        # title	"sunt aut facere repellat…uri optio reprehenderit"
        # body	"quia et suscipit\nsuscip… rem eveniet architecto"
    ]
    
    start_time = time.time()
    

    async with httpx.AsyncClient() as client:
        
        tasks = [fetch_api_data(client, url) for url in urls] 
        print('tasks:', tasks) 
            
        print()

        results = await asyncio.gather(*tasks) 
    
        print('results')
        print(results) 
    
    end_time = time.time()
    
    # 결과 확인
    successful_counts = len([r for r in results if r is not None]) 
    

    print("--------------------------------------------------")
    print(f"총 {len(urls)}개 중 {successful_counts}개 수집 완료")
    print(f"총 소요 시간: {end_time - start_time:.2f}초")

# 3. 비동기 프로그램 실행 시작
asyncio.run(main())
