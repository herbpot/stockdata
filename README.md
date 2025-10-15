# stockdata

한국 주식 시장 데이터 조회 및 분석 도구입니다.

## 개요

stockdata는 pandas_datareader와 KRX(한국거래소) API를 활용하여 코스피(KOSPI)와 코스닥(KOSDAQ)의 주식 데이터를 조회하는 Python 프로젝트입니다. 회사명으로 종목 코드를 검색하고 Yahoo Finance에서 과거 주가 데이터를 가져옵니다.

## 주요 기능

- **종목 코드 조회**: 회사명으로 종목 코드 검색
- **KOSPI/KOSDAQ 지원**: 한국 주식 시장 전체 종목
- **과거 주가 데이터**: 시작일~종료일 주가 조회
- **Yahoo Finance 연동**: 실시간 주가 데이터
- **데이터 분석**: pandas DataFrame으로 데이터 처리

## 기술 스택

- **Python 3.x**
- **pandas** - 데이터 분석
- **pandas_datareader** - Yahoo Finance API
- **BeautifulSoup4** - HTML 파싱
- **requests** - HTTP 요청

## 프로젝트 구조

```
stockdata/
├── 주식정보 불러오기.py     # 간단한 주가 조회
├── 주식test.py            # 테스트 스크립트
├── 주식test_2.py          # 기간 지정 주가 조회
├── import requests.py     # requests 모듈 테스트
└── py code test.py        # 코드 테스트
```

## 설치 및 실행

### 의존성 설치

```bash
pip install pandas pandas_datareader requests beautifulsoup4 lxml
```

### 실행

#### 1. 간단한 주가 조회

```bash
python 주식정보\ 불러오기.py
회사이름을 입력하세요
삼성전자
```

#### 2. 기간 지정 주가 조회

```bash
python 주식test_2.py
시작년도
2020
시작월
1
시작일
1
끝년도
2020
끝월
12
끝일
31
회사이름을 입력하세요
삼성전자
```

## 사용 방법

### 1. 회사명으로 주가 조회

```python
# 주식정보 불러오기.py 실행
회사이름을 입력하세요
삼성전자
```

**출력:**
```
              Open    High     Low   Close    Volume  Adj Close
Date
2020-01-02   57000   57400   56600   57000  15234567   57000
2020-01-03   57200   57800   57000   57600  18234567   57600
...
```

### 2. 특정 기간 주가 조회

```python
# 주식test_2.py 실행
시작년도 >>> 2020
시작월 >>> 1
시작일 >>> 1
끝년도 >>> 2020
끝월 >>> 12
끝일 >>> 31
회사이름을 입력하세요 >>> LG전자
```

## 핵심 코드 구현

### 1. 종목 코드 목록 다운로드

```python
stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}

def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type
    df = pd.read_html(download_link, header=0)[0]
    return df
```

### 2. KOSPI 종목 코드

```python
def get_download_kospi():
    df = get_download_stock('kospi')
    # 종목코드에 .KS 추가 (Yahoo Finance 형식)
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    return df
```

### 3. KOSDAQ 종목 코드

```python
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    # 종목코드에 .KQ 추가
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df
```

### 4. 회사명으로 종목 코드 검색

```python
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
    code = code.strip()  # 공백 제거
    return code

# 사용
code = get_code(code_df, "삼성전자")
# 결과: "005930.KS"
```

### 5. 주가 데이터 가져오기

```python
import pandas_datareader.data as wb
from datetime import datetime

# 기간 설정
start = datetime(2020, 1, 1)
end = datetime(2020, 12, 31)

# Yahoo Finance에서 데이터 가져오기
df = wb.DataReader(code, 'yahoo', start, end)
print(df)
```

## 데이터 구조

### DataFrame 컬럼

| 컬럼 | 설명 | 예시 |
|------|------|------|
| Date | 날짜 | 2020-01-02 |
| Open | 시가 | 57000 |
| High | 고가 | 57400 |
| Low | 저가 | 56600 |
| Close | 종가 | 57000 |
| Volume | 거래량 | 15234567 |
| Adj Close | 수정 종가 | 57000 |

### 종목 코드 형식

- **KOSPI**: `005930.KS` (삼성전자)
- **KOSDAQ**: `035720.KQ` (카카오)

## 사용 예시

### 예제 1: 삼성전자 주가 조회

```python
import pandas_datareader as pdr

code = get_code(code_df, "삼성전자")  # "005930.KS"
df = pdr.get_data_yahoo(code)
print(df.tail())  # 최근 5일 주가
```

### 예제 2: 여러 종목 비교

```python
stocks = ["삼성전자", "SK하이닉스", "NAVER"]
codes = [get_code(code_df, stock) for stock in stocks]

for code in codes:
    df = pdr.get_data_yahoo(code)
    print(f"{code}: {df['Close'].iloc[-1]}")  # 최근 종가
```

### 예제 3: 이동평균 계산

```python
df = pdr.get_data_yahoo(code)
df['MA5'] = df['Close'].rolling(window=5).mean()   # 5일 이동평균
df['MA20'] = df['Close'].rolling(window=20).mean()  # 20일 이동평균
print(df[['Close', 'MA5', 'MA20']].tail())
```

## 데이터 분석 활용

### 1. 수익률 계산

```python
df['Return'] = df['Close'].pct_change() * 100
print(df[['Close', 'Return']].tail())
```

### 2. 시각화

```python
import matplotlib.pyplot as plt

df['Close'].plot(figsize=(12, 6), title='삼성전자 주가')
plt.ylabel('Price (KRW)')
plt.xlabel('Date')
plt.show()
```

### 3. 볼린저 밴드

```python
df['MA20'] = df['Close'].rolling(window=20).mean()
df['STD20'] = df['Close'].rolling(window=20).std()
df['Upper'] = df['MA20'] + (df['STD20'] * 2)
df['Lower'] = df['MA20'] - (df['STD20'] * 2)

df[['Close', 'Upper', 'MA20', 'Lower']].plot(figsize=(12, 6))
plt.show()
```

## 제한사항

- **Yahoo Finance 의존**: Yahoo Finance API 변경 시 작동 중단 가능
- **시차**: 실시간 데이터가 아닌 지연 데이터
- **에러 처리 부족**: 잘못된 회사명 입력 시 예외 처리 미흡
- **한글 인코딩**: 일부 환경에서 한글 회사명 처리 문제

## 개선 방향

### 1. 에러 처리

```python
def get_code(df, name):
    try:
        code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
        code = code.strip()
        if not code:
            raise ValueError(f"'{name}' 종목을 찾을 수 없습니다.")
        return code
    except Exception as e:
        print(f"오류: {e}")
        return None
```

### 2. 캐싱

```python
import pickle

# 종목 코드 저장
code_df.to_pickle('stock_codes.pkl')

# 종목 코드 로드
code_df = pd.read_pickle('stock_codes.pkl')
```

### 3. 웹 인터페이스

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/stock/<name>')
def get_stock_data(name):
    code = get_code(code_df, name)
    df = pdr.get_data_yahoo(code)
    return df.to_json()
```

## 트러블슈팅

### KRX 연결 오류

```
URLError: <urlopen error [Errno 11001] getaddrinfo failed>
```

해결: 인터넷 연결 확인 또는 VPN 사용

### Yahoo Finance 오류

```
RemoteDataError: Unable to read URL
```

해결: 종목 코드 형식 확인 (.KS 또는 .KQ 추가)

### 인코딩 오류

```python
# UTF-8 설정
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
```

## 대안 데이터 소스

### 1. FinanceDataReader

```python
import FinanceDataReader as fdr

# 삼성전자 주가
df = fdr.DataReader('005930', '2020-01-01', '2020-12-31')
```

### 2. pykrx (KRX 공식)

```python
from pykrx import stock

# 삼성전자 주가
df = stock.get_market_ohlcv_by_date("20200101", "20201231", "005930")
```

### 3. yfinance

```python
import yfinance as yf

ticker = yf.Ticker("005930.KS")
df = ticker.history(start="2020-01-01", end="2020-12-31")
```

## 활용 사례

- **퀀트 트레이딩**: 기술적 분석 기반 자동매매
- **백테스팅**: 투자 전략 검증
- **포트폴리오 분석**: 위험 및 수익률 계산
- **시각화 대시보드**: Streamlit, Dash 등

## 참고 자료

- [pandas_datareader 문서](https://pandas-datareader.readthedocs.io/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [KRX 정보데이터시스템](http://data.krx.co.kr/)

## 라이선스

교육 목적으로 작성된 프로젝트입니다.

## 면책 조항

이 도구는 교육 및 학습 목적으로 제공됩니다. 실제 투자 결정에 사용 시 발생하는 손실에 대한 책임은 사용자에게 있습니다.
