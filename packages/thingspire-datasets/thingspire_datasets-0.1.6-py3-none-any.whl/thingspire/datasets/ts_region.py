import pandas as pd
import os
from utils import region_name
from io import StringIO

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'resource-id-name.py')


class ThingsAPIError(Exception):
    pass

class InvalidNotFoundError(ThingsAPIError):
    pass


def find_sido(input_name, region_dict):
    for key, names in region_dict.items():
        if input_name in names:
            return key


def filter_by_name(start_str, df=pd.read_json(json_path)):
    result_df = df[df['name'].str.startswith(start_str)]
    return result_df.to_json(force_ascii=False)


def filter_state(specific_sido):
    region_df = pd.read_json(json_path)
    region_list = filter_by_name(specific_sido, region_df)
    region_list = pd.read_json(StringIO(region_list))
    region_list = region_list["name"].tolist()
    city_list = [region[2:] for region in region_list]

    return city_list


def get_city(sido):
    specific_sido = find_sido(sido, region_name)
    if sido == "all":
        specific_sido = ["강원", "경기", "경남", "경북",
                         "충남", "축북", "전남", "전북",
                         "광주", "대구", "대전", "부산",
                         "서울", "울산", "인천", "제주"]

    output = {}
    if isinstance(specific_sido, list) is True :
        for city in specific_sido:
            city_list = filter_state(city)
            output[city] = city_list
    else:
        try:
            city_list = filter_state(specific_sido)
        except:
            raise InvalidNotFoundError("입력한 도시를 찾을 수 없습니다. 전체 도시를 확인하시려면 파라미터에 all을 넣어주세요")

        output[specific_sido] = city_list

    return output