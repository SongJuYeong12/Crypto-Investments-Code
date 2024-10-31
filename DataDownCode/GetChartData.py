import time
import requests as req
import datetime as dt
from pandas import DataFrame as data
from datetime import datetime as date


# 시간변수 리스트를 시간 변수로 바꾸어 주는 코드
# ---------------------------------------------------------------------------------
def trans_timeval(timelst: list[str]) -> date:
  if timelst == 'starting':
    timeStr = '2000-01-01T00:00:00'
    timeValue = date.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
    
    return timeValue
  
  elif timelst == 'present':
    timeStr = date.now().strftime('%Y-%m-%dT%H:%M:%S')
    timeValue = date.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")

    return timeValue
  
  elif len(timelst) == 3:
    zerotime = '00:00:00'
    timeStr = timelst[0] + '-' + timelst[1] + '-' + timelst[2] + 'T' + zerotime
    timeValue = date.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")

    return timeValue
  
  elif len(timelst) == 5:
    zerosec = '00'
    timeStr = timelst[0] + '-' + timelst[1] + '-' + timelst[2] + 'T' \
            + timelst[3] + ':' + timelst[4] + ':' + zerosec
    
    timeValue = date.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
    
    return timeValue
# ---------------------------------------------------------------------------------


# 서버에 요청 형식 문자열을 만들어주는 코드
# ---------------------------------------------------------------------------------
def create_url(candleMin: int, marketCode: str, count: int, timeStr: str) -> str:
  basic_url = 'https://api.upbit.com/v1/candles/minutes/'
  minute = str(candleMin) + '?'
  code = 'market=' + str(marketCode) + '&'
  counts = 'count=' + str(count) + '&'
  times = 'to=' + timeStr

  url = basic_url + minute + code + counts + times

  return url
# ---------------------------------------------------------------------------------


# 서버에서 차트 데이터를 받아오는 코드
# ---------------------------------------------------------------------------------
def get_chart(candleMin: int, marketCode: str, stTime: str, edTime: str) -> data:
  # 변하지 않는 상수
  headers = {"accept": "application/json"}
  dataColumns = ['time', 'open', 'close', 'high', 'low', 'volumn']
  timedelta = dt.timedelta(minutes=0)
  basic_count = 200

  # 변수들을 조합해 만든 합성 변수
  minute = basic_count * candleMin

  # 상황에 따라 변화하는 변수
  count = None
  candle_List = []
  
  # 리스트 형태의 시간을 변환하는 동시에 kst로 변환
  start_dt = trans_timeval(stTime) - dt.timedelta(hours=9)
  end_dt = trans_timeval(edTime) - dt.timedelta(hours=9)

  # 시간의 차이 값
  dt_delta = end_dt - start_dt

  # 반복해서 데이터를 가저오는 코드
  while dt_delta > timedelta:
    # 경우에 따라 카운트 변수를 설정하는 코드
    if dt_delta < dt.timedelta(minutes=minute):
      day = (dt_delta.days * 1440) // candleMin
      second = dt_delta.seconds // (60 * candleMin)
      count = day + second     
    else:
      count = basic_count

    # 서버에서 차트 데이터를 받아오는 코드
    str_dt = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    url = create_url(candleMin, marketCode, count, str_dt)
    response = req.get(url, headers=headers).json()

    # 모든 데이터를 가져와서 가져올 데이터가 없으면 종료
    if len(response) == 0:
      break
    
    # 가져온 데이터를 분류해서 저장하는 코드
    for res in response:
      templist = [
        date.strptime(res['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S"), res['opening_price'], res['trade_price'],
        res['high_price'], res['low_price'], int(res['candle_acc_trade_volume'])
      ]
      candle_List.append(templist)

    # end 시간을 마지막 데이터의 시간으로 변환한다
    end_dt = date.strptime(response[len(response) - 1]['candle_date_time_utc'], "%Y-%m-%dT%H:%M:%S")

    # 시간의 차이 값 갱신
    dt_delta = end_dt - start_dt

    # 요청 지연 시간 맞춤
    time.sleep(0.1)

  return data(candle_List, columns=dataColumns)
# ---------------------------------------------------------------------------------




  

