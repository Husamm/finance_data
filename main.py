from datetime import date, datetime, timedelta

from get_finance_data import GetFinanceData

print("-HHH- ")
res = GetFinanceData().get_combined_aggs(tickers_list=['META'],from_date=datetime.today()-timedelta(days=6),to_date=datetime.today()-timedelta(days=5))
print(res)

res = GetFinanceData().get_combined_aggs(tickers_list=['TSLA'],from_date=datetime.today()-timedelta(days=6),to_date=datetime.today()-timedelta(days=5))
print(res)

res = GetFinanceData().get_combined_aggs(tickers_list=['META','TSLA'],from_date=datetime.today()-timedelta(days=6),to_date=datetime.today()-timedelta(days=5))
print(res)

#res = GetFinanceData().get_combined_aggs(tickers_list=['AAPL'],from_date=datetime.today()-timedelta(days=6),to_date=datetime.today()-timedelta(days=5))
print(res)


res = GetFinanceData().get_combined_aggs(tickers_list=['META','TSLA','AAPL'],from_date=datetime.today()-timedelta(days=6),to_date=datetime.today()-timedelta(days=5))
print(res)


