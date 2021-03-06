import datetime
import pandas as pd


def get_stocks(market=None):
    market_type = ''
    if market == 'kospi':
        market_type = '&marketType=stockMkt'
    elif market == 'kospi200':
        market_type = '&marketTypekosdaqMkt'
    elif market == 'kosdaq':
        market_type = '&marketTypekonexMkt'
        
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?currentPageSize=5000&pageIndex=1&method=download&searchType=13{market_type}'.format(market_type=market_type)

    list_df_stocks = pd.read_html(url, header=0, converters={'종목코드': lambda x: str(x)})
    df_stocks = list_df_stocks[0]
    return df_stocks
