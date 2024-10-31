import time
import requests as req
import datetime as dt
from datetime import datetime as date
from DataDownCode.GetChartData import *


# 서버에서 코인의 마켓 이름과 고유코드를 가져오는 코드
# ---------------------------------------------------------------------------------
def get_marketCode():
  marketCode_lst = []
  url = "https://api.upbit.com/v1/market/all?isDetails=true"
  headers = {"accept": "application/json"}

  request = req.get(url, headers=headers).json()

  for num in request:
    if 'KRW' in num['market']:
      tempList = []
      tempList.append(num['market'])
      tempList.append(num['korean_name'])
      marketCode_lst.append(tempList)

  return marketCode_lst
# ---------------------------------------------------------------------------------


# find_first_time 함수를 보조해주는 함수
# ---------------------------------------------------------------------------------
def sub_find_first_func(candle_min, market_code, mid):
  headers = {"accept": "application/json"}
  time_str = '2000-01-01T00:00:00'

  time_val = date.strptime(time_str, "%Y-%m-%dT%H:%M:%S") - dt.timedelta(hours=9)

  reqest_time = time_val + dt.timedelta(minutes=(candle_min * mid))
  str_dt = reqest_time.strftime("%Y-%m-%dT%H:%M:%S")

  url = create_url(candle_min, market_code, 1, str_dt)
  res1 = req.get(url, headers=headers).json()

  time.sleep(0.1)

  reqest_time = reqest_time + dt.timedelta(minutes=(candle_min))
  str_dt = reqest_time.strftime("%Y-%m-%dT%H:%M:%S")

  url = create_url(candle_min, market_code, 1, str_dt)
  res2 = req.get(url, headers=headers).json()

  time.sleep(0.1)

  return [len(res1), len(res2)]
# ---------------------------------------------------------------------------------


# 차트의 첫번째 값이 시간을 찾는 코드
# ---------------------------------------------------------------------------------
def find_first_time(candle_min, market_code):
  headers = {"accept": "application/json"}

  start_time = '2000-01-01T00:00:00'
  start_time = date.strptime(start_time, "%Y-%m-%dT%H:%M:%S") - dt.timedelta(hours=9)

  end_time = date.now().strftime("%Y-%m-%d %H")
  end_time = date.strptime(end_time, "%Y-%m-%d %H") - dt.timedelta(hours=9)

  dt_delta = (end_time - start_time)

  day = (dt_delta.days * 1440) // 10
  second = dt_delta.seconds // (60 * 10)

  left, right = 0, (day + second)

  while left <= right:
    mid = (left + right) // 2
    lst = sub_find_first_func(candle_min, market_code, mid)

    if (lst[0] == 0) and (lst[1] == 0):
      left = mid + 1

    elif (lst[0] == 1) and (lst[1] == 1):
      right = mid - 1

    elif (lst[0] == 0) and (lst[1] == 1):
      reqest_time = start_time + dt.timedelta(minutes=((candle_min * mid) + candle_min))
      str_dt = reqest_time.strftime("%Y-%m-%dT%H:%M:%S")

      url = create_url(candle_min, market_code, 1, str_dt)
      response = req.get(url, headers=headers).json()

      return response[0]['candle_date_time_kst']
    
    else:
      return print('잘못 입력했어요')
# ---------------------------------------------------------------------------------