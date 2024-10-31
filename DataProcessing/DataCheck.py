import pandas as pd
from pandas import DataFrame as data
from DataDownCode.GetChartData import *


def check_decreas_sort(chart: data) -> bool:
  return chart['time'].is_monotonic_decreasing


def check_last_time(chart: data, stTime: list[str]) -> data:
  # 마지막 행 선택
  start_time = trans_timeval(stTime)
  last_time = chart.iloc[-1]['time']

  # 데이터가 잘 들어 왔는지 확인
  if last_time < start_time:
    chart = chart[chart['time'] >= start_time]

  return chart


def check_timedelta(chart: data, candleMin: int) -> data:
  # 시간 차이 계산
  timedelta = chart['time'].diff(periods=-1)

  # 차이 값 데이터 프레임
  delta = pd.concat([chart['time'], timedelta], axis=1)

  # 이름 변경
  delta.columns = ['time', 'timedelta']

  # 특정 간격이 아닌 행 찾기
  invalid_rows = delta[delta['timedelta'] != pd.Timedelta(minutes=candleMin)]

  # 마지막 행은 삭제(nan 값이여서)
  invalid_rows.drop(invalid_rows.index[-1], axis=0, inplace=True)

  # 특정 간격이 아닌 행의 데이터 추출
  invalid_rows = invalid_rows[['time', 'timedelta']]

  return invalid_rows


def save_Dataframe(Dataframe: data, fileName: str, folderName: str):
  basicPath = 'C:/Users/sailo/OneDrive/문서/chart analysis code/'
  save_path = basicPath + folderName + '/' + fileName + '.csv'

  # 인덱스 기준으로 데이터프레임의 순서를 뒤집음
  Dataframe = Dataframe.sort_index(ascending=False).reset_index(drop=True)

  # 데이터프레임을 CSV 파일로 저장 (인덱스 제외)
  Dataframe.to_csv(save_path, index=False)


def load_Dataframe(fileName: str, folderName: str) -> data:
  # 불러올 파일 이름
  basicPath = 'C:/Users/sailo/OneDrive/문서/chart analysis code/'
  full_path = basicPath + folderName + '/' + fileName +'.csv'

  # 파일 불러오기
  Dataframe = pd.read_csv(full_path)

  return Dataframe