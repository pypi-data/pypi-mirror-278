region_name = {"강원": ["강원도", "강원"],
               "경기": ["경기도", "경기"],
               "경남": ["경상남도", "경상 남도", "경남"],
               "경북": ["경상북도", "경상 북도", "경북"],
               "충남": ["충청남도", "충청 남도", "충남"],
               "충북": ["충청북도", "충청 북도", "충북"],
               "전남": ["전라남도", "전라 남도", "전남"],
               "전북": ["전라북도", "전라 북도", "전북"],
               "광주": ["광주", "광주광역시", "광주 광역시", "광주시"],
               "대구": ["대구", "대구광역시", "대구 광역시", "대구시"],
               "대전": ["대전", "대전광역시", "대전 광역시", "대전시"],
               "부산": ["부산", "부산광역시", "부산 광역시", "부산시"],
               "서울": ["서울", "서울특별시", "서울 특별시", "서울시"],
               "울산": ["울산", "울산광역시", "울산 광역시", "울산시"],
               "인천": ["인천", "인천광역시", "인천 광역시", "인천시"],
               "제주": ["제주", "제주특별자치도", "제주 특별자치도", "제주 특별 자치도", "제주도"]}

flomon_url = "/api/ts/timeseries/" \
          "multiple?aggregation=NONE&interval=600000&" \
          "keys=sunrise&" \
          "keys=sunset&" \
          "keys=weatherCode&" \
          "keys=weatherCondition&" \
          "keys=temp&" \
          "keys=humidity&" \
          "keys=sensibleTemp&" \
          "keys=visibility&" \
          "keys=clouds&" \
          "keys=pressure&" \
          "keys=windSpeed&" \
          "keys=windDirection&" \
          "keys=windGust&" \
          "keys=precipitationIntensity&" \
          "keys=snowfall&"

api_payload = {}