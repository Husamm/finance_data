from datetime import datetime

from get_finance_data import GetFinanceData


def EPS_announcements_to_price_change(ticker):
    EPS_announcements = GetFinanceData().get_EPS_annoucments(ticker)
    result_map = {}
    for announcement in EPS_announcements:
        percentage_change = GetFinanceData().get_stock_percentage_change(ticker, announcement.reported_date)
        if percentage_change is None:
            continue
        result_map[announcement.reported_date] = [announcement, percentage_change]
