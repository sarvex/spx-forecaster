import yfinance as yf
import pandas as pd
import datetime

spx = yf.Ticker("^GSPC")
index = pd.read_csv('./data/spx_list.zip')
companies = ''.join(f'{c} ' for c in index.ticker)

spx_500 = yf.download( #
    tickers=companies, 
    period='5y', 
    group_by='ticker',
    prepost=True,
    threads=12
    )

gspc = yf.download( #dailies for the last 5 years
    tickers='^GSPC', 
    period='5y', 
    group_by='ticker',
    prepost=True,
    threads=12
    )

gspc_ = yf.download( # in 5 min. intervals
    tickers='^GSPC', 
    period='60d', 
    interval='5m',
    group_by=spx,
    auto_adjust=True,
    prepost=True,
    threads=12
    )

timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H%MH -0800")
gspc_.to_csv(f'./data/stocks/gspc_60d_5min_{timenow}.zip', compression='zip')
gspc.to_csv(f'./data/stocks/gspc_5y_{timenow}.zip', compression='zip')
spx_500.to_csv(f'./data/stocks/spx_indexed_{timenow}.zip', compression='zip')