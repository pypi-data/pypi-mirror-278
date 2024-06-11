from datetime import datetime
import aiohttp
import asyncio
import json
import pandas as pd
from pandas import json_normalize

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


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

class InvalidPeriodError(ThingsAPIError):
    pass

class InvalidDiffError(ThingsAPIError):
    pass


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise InvalidDateFormatError(f"Incorrect data format for date: {date_text}. It should be YYYYMMDD.")


def date_range(start, end):
    calendar_df = pd.DataFrame(columns=['date'])
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    output = [date.strftime("%Y%m%d") for date in pd.date_range(start, end, freq='D')]
    calendar_df['date'] = sorted(output)

    return calendar_df


def date_merge(calendar_pd, holiday_pd):
    calendar_pd['date'] = pd.to_datetime(calendar_pd['date'], format='%Y%m%d')
    holiday_pd['date'] = pd.to_datetime(holiday_pd['date'], format='%Y%m%d')

    out_pd = pd.merge(calendar_pd, holiday_pd, how='outer', on='date')

    return out_pd


async def fetch_holiday_data(api_url, api_key, semaphore):
    url = f"{api_url}/ext/holiday_calendar"
    headers = {'Authorization': api_key}

    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 401:
                    raise InvalidAPIKeyError("The API key provided is invalid.")
                elif response.status == 404:
                    raise InvalidLocationError("The API URL is invalid.")
                elif response.status != 200:
                    raise ThingsAPIError(f"Failed to fetch calendar data: {await response.text()}")

                holidays_data = await response.json()
                dataframe = json_normalize(holidays_data)

    dataframe.rename(columns={"dateName": "description",
                              "isHoliday": "holiday",
                              "locdate": "date"}, inplace=True)
    dataframe.drop(['dateKind', 'seq'], axis=1, inplace=True)

    return dataframe


def weekend_collect(calendar_df):
    calendar_df['day_of_week'] = calendar_df['date'].dt.dayofweek
    calendar_df['weekend'] = calendar_df.day_of_week.apply(lambda x: 1 if x >= 5 else 0)
    calendar_df['holiday'] = (calendar_df['holiday'] == "Y") | (calendar_df['weekend'] == 1)
    calendar_df['holiday'] = calendar_df.holiday.apply(lambda x: 1 if x == True else 0)
    calendar_df.drop(['weekend'], axis=1, inplace=True)

    return calendar_df


def between_collect(calendar_df):
    holiday_list = calendar_df['holiday'].values
    next_day = [0] * len(holiday_list)
    prev_day = [0] * len(holiday_list)

    for i in range(len(holiday_list) - 1):
        if (holiday_list[i] == 1) & (holiday_list[i + 1] == 0):
            next_day[i + 1] = 1

    for i in range(1, len(holiday_list)):
        if (holiday_list[i - 1] == 0) & (holiday_list[i] == 1):
            prev_day[i - 1] = 1

    calendar_df['prev_day'] = prev_day
    calendar_df['next_day'] = next_day

    return calendar_df


def vacation_collect(today_year, start, end):
    vacation_df = pd.DataFrame(columns=['date', "vacation"])

    output = [date.strftime("%Y%m%d")
              for date in pd.date_range(f"{today_year}{start}",
                                        f"{today_year}{end}",
                                        freq='D')]
    vacation_df['date'] = sorted(output)
    vacation_df['vacation'] = "1"

    return vacation_df


async def get_calendar_async(api_key, api_url, start, end=datetime.today().strftime('%Y%m%d')):
    if int(end) - int(start) >= 0:
        validate_date(start)
        validate_date(end)
    else:
        raise InvalidDiffError("The start date is greater than the end date.")

    start_year = start[:4]
    end_year = end[:4]
    calendar_pd = date_range(start, end)

    for i in range(int(end_year) - int(start_year) + 1):
        vacation_list = [vacation_collect(int(start_year) + i, "0715", "0831"),
                         vacation_collect(int(start_year) + i, "0101", "0228"),
                         vacation_collect(int(start_year) + i, "1215", "1231")]
        vacation_ele = pd.concat(vacation_list, ignore_index=True)
        if i == 0:
            vacation_pd = vacation_ele
        else:
            vacation_pd = pd.concat([vacation_pd, vacation_ele], ignore_index=True)

    semaphore = asyncio.Semaphore(10)  # 동시 요청 수 제한
    holiday_pd = await fetch_holiday_data(api_url, api_key, semaphore)
    calendar_df = date_merge(calendar_pd, holiday_pd)
    calendar_df = weekend_collect(calendar_df)
    calendar_df = between_collect(calendar_df)
    calendar_df = date_merge(calendar_df, vacation_pd)
    calendar_df = calendar_df[(calendar_df['date'] >= pd.to_datetime(start)) & (calendar_df['date'] <= pd.to_datetime(end))]
    calendar_df['vacation'] = calendar_df['vacation'].fillna(0)

    calendar_df = calendar_df.astype({"holiday": int,
                                      "day_of_week": int,
                                      "prev_day": int,
                                      "next_day": int})
    calendar_df['year'] = calendar_df['date'].dt.year
    calendar_df['month'] = calendar_df['date'].dt.month
    calendar_df['day'] = calendar_df['date'].dt.day
    calendar_df['date'] = calendar_df['date'].dt.strftime('%Y-%m-%d')

    return calendar_df

def get_calendar(api_key, api_url, start, end=datetime.today().strftime('%Y%m%d')):
    return asyncio.run(get_calendar_async(api_key, api_url, start, end))