from datetime import datetime, timedelta

from finance_analysis import EPS_announcements_to_price_change
from generate_report import aggs_list_to_csv, create_EPS_announcements_to_price_change_csv
from get_finance_data import GetFinanceData
print()
aggs = GetFinanceData().get_ticker_aggs('META', datetime.now() - timedelta(days=10),
                                        datetime.now() - timedelta(days=5))

aggs_list_to_csv(aggs_list=aggs,csv_file='meta.csv')



create_EPS_announcements_to_price_change_csv(csv_file='meta_changes.csv',result_map=EPS_announcements_to_price_change('META'))

