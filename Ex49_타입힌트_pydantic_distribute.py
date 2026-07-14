from typing import Any 
from pydantic import BaseModel, Field 
from pydantic import ValidationError

def add(a: int, b: int) -> int:
    return a+b
print(add(10,20))
print('-------------------------')

names: list[str] = [
    "철수",
    "영희", # "영희"대신 숫자 10을 넣으면 결과는 잘 나오는데 10에 빨간줄이 생긴다. 
    "민수"
]
# names = ["민수", "지수"]   # ✅ 재할당할 때에는 타입 힌트를 빼는 것이 일반적입니다.
print(names)
print()
print('-------------------------')

person: dict[str, Any] = {
    "name": "홍길동",
    "age": 20,
    "height": 175.5
}
# Key : 문자열(str)
# Value : 아무 타입(Any) 아무 자료형이나 올 수 있다는 뜻 

print(person)
print()

print('-------------------------')

def print_name(name: str) -> None:
    print(name)

print(print_name('하하하')) 

print('-------------------------')

def save_user(
    name: str,
    age: int,
    scores: list[int],
    info: dict[str, Any]
) -> bool: # ->bool 없고 return True 대신 pass하면 None 출력된다. 

    print(name)
    print(age)
    print(scores)
    print(info)

    return True

print(save_user(
    "홍길동",
    20,
    [90, 95, 88],
    {"city": "서울", "married": False}
))
print()

print('-------------------------')




class User(BaseModel):
    # name: str
    # age: int
    name: str = Field(
        min_length=2,
        max_length=5 
    )

    age: int = Field( 
        ge=0, 
        le=120
    )

user = User( # 객체생성 
    name="홍길동",
    age="20"
)

print('user:',user) 
print('-------------------------')


user_data = {"name": "윤아", "age": "2.3"} 

try:
    user = User(**user_data) 
    
    result = User.model_validate(user)
    print("성공적으로 검증되었습니다:", result)

except ValidationError as e:
    
    print("데이터 검증 실패!")
    print(e.json())  

print()
print('-------------------------')


data = {
    "name":"철수",
    "age":20
}

print('dict → 객체 : 역직렬화') 
user = User(**data)

print('User 객체:', user)
print()

print('객체 → dict : 직렬화') 
print('user.model_dump():', user.model_dump())

print('객체 → json : 직렬화')
print('user.model_dump_json():',user.model_dump_json())
print()
