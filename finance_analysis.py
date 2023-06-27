from datetime import datetime, timedelta
from get_finance_data import GetFinanceData

YEARS_BACK = 2.0


def EPS_announcements_to_price_change(ticker):
    EPS_announcements = GetFinanceData().get_EPS_annoucments(ticker)
    result_map = {}
    for announcement in EPS_announcements:
        percentage_change = get_stock_percentage_change(ticker, announcement.reported_date)
        if percentage_change is None:
            continue
        result_map[announcement.reported_date] = [announcement, percentage_change]
    return result_map


def get_stock_percentage_change(ticker, date):
    if (datetime.now() - date).days > YEARS_BACK * 365:
        return None

    aggs = GetFinanceData().get_ticker_aggs(ticker, date,
                                date + timedelta(days=1))
    if aggs is None:
        return None
    return ((aggs[1].open - aggs[0].close) / aggs[0].close) * 100


def get_combined_aggs(tickers_list, from_date, to_date):
    if (datetime.now() - from_date).days > YEARS_BACK * 365:
        return None
    tickers_maps = []
    for i in range(len(tickers_list)):
        ticker_data = GetFinanceData().get_ticker_aggs(ticker=tickers_list[i], from_date=from_date, to_date=to_date)
        tickers_maps.insert(i, {ticker_data[j].timestamp: ticker_data[j] for j in range(len(ticker_data))})
    # sum all the data to first ticker dictionary
    for i in range(1, len(tickers_list)):
        for timestamp_i in tickers_maps[0].keys():
            ticker_i_agg = tickers_maps[i].get(timestamp_i)
            if ticker_i_agg is None:
                tickers_maps[0].pop(timestamp_i)
            else:
                # sum the open,close,high,low,volume
                for field_name in ['open', 'close', 'high', 'low', 'volume']:
                    curr_val = getattr(tickers_maps[0].get(timestamp_i), field_name)
                    other_val = getattr(tickers_maps[i].get(timestamp_i), field_name)
                    setattr(tickers_maps[0].get(timestamp_i), field_name, curr_val + other_val)

    return tickers_maps[0]
