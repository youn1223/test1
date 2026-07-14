from typing import TypedDict
from dataclasses import dataclass

# 쇼핑몰 API에서 이런 JSON을 받는다고 가정합니다.
# JSON 데이터를 받아서 → 데이터 구조(타입)를 확인하고 → 내부에서 사용하기 좋은 객체로 변환한 뒤 → 필요한 값을 쉽게 사용하기 위한 예제
# =========================
# 외부 데이터 구조
# =========================
# =========================
# =========================
# =========================# =========================
# =====수정===================
# ========================
# ========================
# ========================


class ProductDict(TypedDict):
    id: int
    name: str
    price: int
    stock: int


api_data: ProductDict = {
    "id": 1,
    "name": "맥북", 
    "price": 1500000,
    "stock": 10
}


# =========================
# 내부 데이터 객체
# =========================

@dataclass
class Product:
    id: int
    name: str
    price: int
    stock: int

    def total_price(self):
        return self.price * self.stock


# =========================
# 변환
# =========================
# print('**api_data:', **api_data) # 에러남, **은 함수 호출시 인자로 전달할 때와 같은 특수한 경우에만 쓸수 있다.

product = Product(**api_data) # 딕셔너리 api_data의 키-값을 풀어서(unpacking) 함수(생성자)의 인자처럼 전달하는 문법입니다.
# product는 자동으로 이런 생성자를 만든다.
# def __init__(    self,    id: int,    name: str,    price: int,    stock: int):
#     self.id = id
#     self.name = name
#     self.price = price
#     self.stock = stock

# Product(**api_data)이것은 아래와 같다.
# Product(   id=1,    name="노트북",    price=1500000,    stock=10) # 이것은 위의 생성자를 호출하는 것이다. 

# product = Product(**api_data) 와 아래 코드는 같다.
# dict 값을 직접 꺼내서 객체 생성 (** 사용 안 함)
# product = Product(
#     id=api_data["id"],
#     name=api_data["name"],
#     price=api_data["price"],
#     stock=api_data["stock"]
# )

print(product)
print(product.name)
print(product.total_price())
