import json
from datetime import datetime
import requests

# 현재 날짜와 시간 가져오기
now = datetime.now()

# YYYYMMDD 형식의 문자열로 변환하기
formatted_date = now.strftime("%Y%m%d")

# JSON 파일에서 데이터 읽기
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# config.json 으로부터 정보 가져오기
Base_Address = data['베이스주소']
API_key = data['api_key']
ATPT_OFCDC_SC_CODE = data['시도교육청코드']
SD_SCHUL_CODE = data['행정표준코드']
MMEAL_SC_CODE = data['식사코드']
MLSV_YMD = f"MLSV_YMD={formatted_date}" # 오늘 날짜

url = f"{Base_Address}&{ATPT_OFCDC_SC_CODE}&{SD_SCHUL_CODE}&{MLSV_YMD}&{MMEAL_SC_CODE}&{API_key}"

try:
    # 요청 보내고 응답 받기
    response = requests.get(url)

    # 응답 확인
    if response.status_code == 200:
        # JSON 데이터 파싱
        json_data = response.json()

        # 각 데이터의 의미를 함께 출력하며 <br> 태그를 제거하고 줄바꿈 추가
        meal_data = json_data['mealServiceDietInfo'][1]['row'][0]  # 급식 정보 데이터
        ddish_nm = meal_data['DDISH_NM'].replace('<br/>', '\n')  # <br/> 태그를 줄바꿈으로 변환

        print("=====급식 정보=====")
        print(ddish_nm)
        print("칼로리 정보:", meal_data['CAL_INFO'])
    else:
        print("요청에 실패했습니다. 상태 코드:", response.status_code)

except Exception as e:
    print("에러 발생:", e)
