# thingspire-datasets 설치가이드

### - [Docs]()

### - [PyPi](https://pypi.org/project/thingspire-datasets/)

## 시작하기

---

 - 본 문서는 Thingspire MLOps의 데이터 수집/가공을 위한 Thingspire-datasets를 위한 설치 가이드 입니다.
 - 이 문서에는 프로젝트 다운로드, 패키지 설치에 대한 가이드가 포함되어 있습니다.
 - 해당 라이브러리를 사용하기 위해서 암호키 발급을 받아야 합니다.
 - Mail: inho@thingspire.com 에 메일로 암호키 발급을 신청하세요.

## 설치

---

### PIP

   - thingspire-datasets 는 pip를 사용하여 [PyPi]((https://pypi.org/project/thingspire-datasets/))에서 설치할 수 있습니다.

```cmd 
pip install thingspire-datasets
```

### Github install

   - 현재 페이지의 주소를 복사하여 git 명령어로 설치할 수 있습니다

```cmd 
git clone https://github.com/thingspire/thingspire-datasets
cd thingspire-datasets
pip install .
```


## 사용 방법

---

### Calander data

   - [한국천문연구원_특일 정보](https://www.data.go.kr/data/15012690/openapi.do) 사용 <br>
    수집 종료시간을 입력하지 않을 시, 현재 시간까지 데이터를 수집함. <br>
    휴가철 여부는 여행지 숙박업소의 성수기 기준으로 산정 <br>
    (여름: 7/15~8/31, 겨울: 12/15~2/28) <br>

```cmd 
from thingspire.datasets import get_calendar

calendar_data = get_calendar(calendar_key = "암호키",
                             start = "YYYYMMDD", 
                             end = "YYYYMMDD")
```

### Weather data

   - [Openweather](https://openweathermap.org/api) 데이터 사용 <br>
    우리나라의 기초 지자체 (시/군/구 단위)의 특정 지정 간격 날씨 데이터를 출력하는 함수 <br>
    수집 종료 시간을 입력하지 않을 시, 현재 시간까지 데이터를 수집함.

```cmd 
from thingspire.datasets import get_weather

calendar_data = get_weather(weather_key = "암호키", 
                            weather_url = "URL:Port,
                            sido = "시도 명",
                            gungu = "군구 명",
                            start = "YYYYMMDD",
                            end = "YYYYMMDD",
                            )
```

### Region data

   - 우리나라의 기초 지자체 (시/군/구 단위)를 출력하는 함수 <br>
    파라미터로 시/도 를 입력하면 입력한 시/도의 기초 지자체를 받아옴 <br>
    파라미터에 "all"을 입력하면, 모든 시/도의 기초 지자체를 받아옴

```cmd 
from thingspire.datasets import get_city

city_data = get_city(sido = "시도 명")
```

---

