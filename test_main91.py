import pytest
import httpx
from Ex91main_distribute import WeatherResult # main_distribute.py
from Ex91main_distribute import fetch_city_data
import pandas
import numpy

# pip install pytest-asyncio


@pytest.mark.asyncio 
async def test_weather_schema():
    city = {"name": "서울", "lat": 37.5665, "lon": 126.9780, "tz": "Asia/Seoul"}

    async with httpx.AsyncClient() as client:
        weather = await fetch_city_data(client, city)
        print("###############:", weather["degrees"])


    if weather["city_name"] == "서울":
        assert weather["degrees"] > 30, ( 
            f"서울의 기온이 {weather['degrees']}℃ 입니다. 30℃ 이하입니다."
        )

