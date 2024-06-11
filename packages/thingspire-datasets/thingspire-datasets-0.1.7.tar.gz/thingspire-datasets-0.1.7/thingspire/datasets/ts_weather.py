import aiohttp
import asyncio
from datetime import datetime
import json
import time
import pandas as pd
import numpy as np
from io import StringIO
import os

from .utils import flomon_url, api_payload, region_name

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'resource-id-name.py')


class ThingsAPIError(Exception):
    pass

class InvalidAPIKeyError(ThingsAPIError):
    pass

class InvalidAPIURLError(ThingsAPIError):
    pass

class InvalidLocationError(ThingsAPIError):
    pass

class InvalidDateFormatError(ThingsAPIError):
    pass

class InvalidDiffError(ThingsAPIError):
    pass

class InvalidDataError(ThingsAPIError):
    pass

class DateDifferenceError(ThingsAPIError):
    pass


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise InvalidDateFormatError(f"Incorrect data format for date: {date_text}. It should be YYYYMMDD.")


def find_sido(input_name, region_dict):
    for key, names in region_dict.items():
        if input_name in names:
            return key


def filter_by_name(start_str, df=pd.read_json(json_path)):
    result_df = df[df['name'].str.startswith(start_str)]
    return result_df.to_json(force_ascii=False)


def load_id_names(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        id_info = json.load(file)
        return {str(ids['id']): ids['name'] for ids in id_info}


def ids_to_names(data, id_name_map):
    named_data = {}
    for region_id, region_data in data.items():
        region_name = id_name_map.get(region_id, "Unknown Region")
        named_data[region_name] = region_data
    return named_data


def date_range(start, end):
    calendar_df = pd.DataFrame(columns=['date'])
    start = datetime.strptime(start, "%Y%m%d")
    end =  datetime.strptime(end, "%Y%m%d")
    output = [date.strftime("%Y%m%d") for date in pd.date_range(start, end, freq='D')]
    calendar_df['date'] = sorted(output)

    return calendar_df


def round_time_and_aggregate(data):
    final_data = {}

    for region_id, categories in data.items():
        final_data[region_id] = {}

        for category, records in categories.items():
            for record in records:
                rounded_time = round(record['time'] / 1000 / 60 / 60) * 60 * 60 * 1000

                if rounded_time not in final_data[region_id]:
                    final_data[region_id][rounded_time] = {}
                if category not in final_data[region_id][rounded_time]:
                    final_data[region_id][rounded_time][category] = record['value']
                else:
                    if not isinstance(final_data[region_id][rounded_time][category], list):
                        final_data[region_id][rounded_time][category] = [final_data[region_id][rounded_time][category]]
                    final_data[region_id][rounded_time][category].append(record['value'])

    return final_data


def kor_time(js):
    rows_list = []
    for district, times in js.items():
        for time, values in times.items():
            row = values.copy()
            row['region'] = district
            row['time'] = time
            rows_list.append(row)

    df = pd.DataFrame(rows_list)
    try:
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')
    except:
        raise InvalidDataError("No data exists for that time. Data exists from March 12, 2024.")
    df['datetime'] = df['datetime'].dt.tz_localize('UTC')
    df['datetime'] = df['datetime'].dt.tz_convert('Asia/Seoul')

    return df


def slice_outter(group, start, end):
    start_date = pd.to_datetime(start, format='%Y%m%d').tz_localize('Asia/Seoul')
    end_date = pd.to_datetime(end, format='%Y%m%d').tz_localize('Asia/Seoul')
    end_date = end_date + pd.DateOffset(days=1, seconds=-1)
    group = group[(group.index >= start_date) & (group.index <= end_date)]

    return group


def region_inter(df, start, end):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            values = df[col].values
            mask = np.array([isinstance(x, list) for x in values])
            df.loc[mask, col] = [x[0] if isinstance(x, list) else x for x in values[mask]]

    df.set_index('datetime', inplace=True)
    results = []
    for name, group in df.groupby('region'):
        full_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='h')
        group = group.reindex(full_index)
        group.interpolate(method='time', inplace=True)
        group['region'] = group['region'].ffill()
        group = slice_outter(group, start, end)
        group = group.reset_index().rename(columns={"index": "datetime"})
        group = group.ffill()
        group = group.bfill()
        results.append(group)

    df = pd.concat(results, ignore_index=True)

    return df


def js_to_dataframe(js, start, end):
    df = kor_time(js)
    df = region_inter(df, start, end)

    required_columns = ['windGust', 'windDirection', 'windSpeed']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
    try:
        df = df[['region', 'datetime', 'time',
             'sunrise', 'sunset', 'temp', 'sensibleTemp',
             'humidity', 'pressure', 'clouds', 'visibility',
             'precipitationIntensity', 'snowfall', 'windGust',
             'windDirection', 'windSpeed', 'weatherCode']]
    except:
        raise InvalidDataError("No data exists for that time. Data exists from March 12, 2024.")
    df['datetime'] = df['datetime'].dt.tz_localize(None)
    df = df.fillna(0)

    return df


def adjust_column_names(cols):
    new_cols = []
    for col in cols:
        if isinstance(col, tuple):
            if col[0] in ['temp', 'sensibleTemp']:
                new_cols.append(f"{col[0]}_{col[1]}")
            else:
                new_cols.append(col[0])
        else:
            new_cols.append(col)
    return new_cols


async def fetch(url, api_key, api_payload, semaphore):
    headers = {'Authorization': api_key}
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=api_payload) as response:
                if response.status == 401:
                    raise InvalidAPIKeyError("The API key provided is invalid.")
                elif response.status == 404:
                    raise InvalidLocationError("The API URL is invalid.")
                elif response.status != 200:
                    raise ThingsAPIError(f"Failed to fetch weather data: {await response.text()}")
                return await response.json()


async def get_weather_async(api_key, api_url,
                            sido, gungu="",
                            start=datetime.today().strftime('%Y%m%d'),
                            end=datetime.today().strftime('%Y%m%d')):
    if int(end) - int(start) >= 0:
        validate_date(start)
        validate_date(end)
    else:
        raise InvalidDiffError("The start date is greater than the end date.")

    start_date = datetime.strptime(start, "%Y%m%d")
    end_date = datetime.strptime(end, "%Y%m%d")
    if (end_date - start_date).days > 32:
        raise DateDifferenceError("Weather data requests can only be made for up to one month.")


    region_df = pd.read_json(json_path)
    id_names = load_id_names(json_path)

    specific_sido = find_sido(sido, region_name)
    if specific_sido is None:
        raise InvalidLocationError("The 'sido' parameter is invalid, please check it.")

    specific_gungu = specific_sido + gungu
    region_list = filter_by_name(specific_gungu, region_df)
    region_list = pd.read_json(StringIO(region_list))
    region_list = region_list["id"].tolist()
    if not region_list:
        raise InvalidLocationError("The 'gungu' parameter is invalid, please check it.")

    region_params = "&".join([f"resourceIds={region_id}" for region_id in region_list])

    start_time = (time.mktime(datetime.strptime(start, "%Y%m%d").timetuple()) - 1800) * 1000
    end_time = (time.mktime(datetime.strptime(end, "%Y%m%d").timetuple()) + 86300 + 1800) * 1000
    limit = (end_time - start_time) // (3600 * 1000) * 3
    if limit == 0:
        limit = 24 * 3

    url = f"{api_url}{flomon_url}limit={int(limit)}&{region_params}&startTime={int(start_time)}&endTime={int(end_time)}"

    semaphore = asyncio.Semaphore(10)  # 동시 요청 수 제한

    try:
        response = await fetch(url, api_key, api_payload, semaphore)
    except aiohttp.ClientError as e:
        raise InvalidAPIURLError("The API URL is invalid.") from e

    processed_data = round_time_and_aggregate(response)
    named_data = ids_to_names(processed_data, id_names)
    output = js_to_dataframe(named_data, start, end)

    return output


def get_weather(api_key, api_url, sido, gungu="", start=datetime.today().strftime('%Y%m%d'), end=datetime.today().strftime('%Y%m%d')):
    return asyncio.run(get_weather_async(api_key, api_url, sido, gungu, start, end))