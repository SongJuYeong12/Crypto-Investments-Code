import numpy as np
from pandas import DataFrame as data


def trans_hikinAshi(chart: data) -> data:
  # 거래량과 시간을 제외하고 가격 데이터만 추출한다
  chart = chart[['open', 'close', 'high', 'low']]

  # 가격차트의 행 개수 추출
  count = chart.shape[0]

  # 첫번째 차트 데이터 하이킨 아시 적용
  open = (chart.iloc[0]['open'] + chart.iloc[0]['close']) / 2
  close = (chart.iloc[0]['open'] + chart.iloc[0]['close'] + chart.iloc[0]['high'] + chart.iloc[0]['low']) / 4
  high = chart.iloc[0].max()
  low = chart.iloc[0].min()

  chart.iloc[0] = [open, close, high, low]

  # 첫번째를 제외한 모든 차트 데이터 하이킨 아시 적용
  for num in range(1, count):
    n = num - 1

    open = (chart.iloc[n]['open'] + chart.iloc[n]['close']) / 2
    close = (chart.iloc[num]['open'] + chart.iloc[num]['close'] + chart.iloc[num]['high'] + chart.iloc[num]['low']) / 4
    high = max([open, close, chart['high'].iloc[num]])
    low = min([open, close, chart['low'].iloc[num]])

    chart.iloc[num] = [open, close, high, low]
  
  return chart


def create_color(chart: data) -> data:
  delta = chart['open'] - chart['close']

  # 조건식 정의
  conditions = [(delta > 0), (delta < 0), (delta == 0)]

  # 각 조건에 해당하는 값 정의
  choices = ['red', 'blue', 'white']

  # np.select를 사용하여 조건에 따라 분류
  chart['color'] = np.select(conditions, choices, default='unknown')

  return chart


def create_color_twice(chart: data) -> data:
  delta = chart['open'] - chart['close']

  # 조건식 정의
  conditions = [(delta >= 0), (delta < 0)]

  # 각 조건에 해당하는 값 정의
  choices = ['red', 'blue']

  # np.select를 사용하여 조건에 따라 분류
  chart['color'] = np.select(conditions, choices, default='unknown')

  return chart


def filter_dataframe(chart: data) -> data:
  # 필요한 변수 선언
  result_rows = []

  # 구간별 그룹 번호를 부여
  chart['group'] = (chart['color'] != chart['color'].shift()).cumsum()

  for _, group in chart.groupby('group'):
    if group['color'].iloc[0] == 'red':
      tempList = []
      tempList.append(group.loc[group['high'].idxmax()].name)
      tempList.append(group.loc[group['high'].idxmax()]['high'])

      result_rows.append(tempList)

    elif group['color'].iloc[0] == 'blue':
      tempList = []
      tempList.append(group.loc[group['low'].idxmin()].name)
      tempList.append(group.loc[group['low'].idxmin()]['low'])

      result_rows.append(tempList)

  result_df = data(result_rows, columns=['time', 'price'])

  return result_df


def create_diff(chart: data) -> data:
  # 1열 기준으로 현재 값과 바로 전 행의 값을 빼기
  chart['time_diff'] = chart['time'].diff().fillna(0).astype(int)

  # 2열 기준으로 현재 값과 바로 전 행의 값을 빼고 그 값을 바로 전 행의 값으로 나누기
  chart['price_rate'] = (chart['price'].diff() / chart['price'].shift(1))

  # 변화율을 100을 곱하고 소수점 한자리만 남기기
  chart['price_rate'] = (chart['price_rate'] * 100).fillna(0).round(1)

  return chart



