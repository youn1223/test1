
# 동기 방식 코드
import time
import asyncio

def worker2(name, delay):
    print(time.strftime('%X'), f"[{name}] 작업 시작")   
    time.sleep(delay) # "컴퓨터야, 지금부터 아무것도 하지 말고 delay초 동안 완전히 얼어붙어라(Block)"라는 명령입니다.  
    print(time.strftime('%X'), f"[{name}] 작업 완료")

def main2():  
    worker2("A", 3)
    worker2("B", 2)

# 프로그램 시작
main2()
print('--------------------------------------------')

# 비동기 방식 코드

async def worker(name, delay): 
    print(time.strftime('%X'), f"[{name}] 작업 시작") 

    await asyncio.sleep(delay) # 대기상태
    
    print(time.strftime('%X'), f"[{name}] 작업 완료")


async def main(): # 메서드 이름 a()도 가능 

    await asyncio.gather(
        worker("A", 3),
        worker("B", 2)      
    )

asyncio.run(main()) 
