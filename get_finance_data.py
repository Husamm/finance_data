import polygon
from polygon import RESTClient
from datetime import datetime, timedelta
from urllib.request import urlopen
import json

POLYGON_API_KEY = 'T1SYYcOIqlp0edh1Y17IdNBad0873V5_'
ALPHAVANTAGE_API_KEY = 'MJUGHAYZ89VMQ2VE'
YEARS_BACK = 2.0


class GetFinanceData:
    def __init__(self):
        self.client = RESTClient(POLYGON_API_KEY)

    def get_combined_aggs(self, tickers_list, from_date, to_date):
        if (datetime.now() - from_date).days > YEARS_BACK * 365:
            return None
        tickers_maps = []
        for i in range(len(tickers_list)):
            ticker_data = self.client.get_aggs(ticker=tickers_list[i], from_=from_date.strftime("%Y-%m-%d"),
                                               to=to_date.strftime("%Y-%m-%d"), limit=5000, multiplier=1,
                                               timespan='day')
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

    def get_EPS_annoucments(self, ticker):
        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        return QuarterlyEarnings.parse_json_list(data_json['quarterlyEarnings'])

    def get_stock_percentage_change(self, ticker, date):
        if (datetime.now() - date).days > YEARS_BACK * 365:
            return None
        try:
            aggs = self.client.get_aggs(
                ticker,
                1,
                "day",
                date.strftime("%Y-%m-%d"),
                (date + timedelta(days=1)).strftime("%Y-%m-%d"),
            )
        except:
            return None
        return ((aggs[1].open - aggs[0].close) / aggs[0].close) * 100


class QuarterlyEarnings:
    def __str__(self) -> str:
        return super().__str__()

    def __init__(self, json_obj):
        self.surprise_percentage = float(json_obj['surprisePercentage'])
        self.surprise = float(json_obj['surprise'])
        self.estimated_EPS = float(json_obj['estimatedEPS'])
        self.reported_EPS = float(json_obj['reportedEPS'])
        self.reported_date = datetime.strptime(json_obj['reportedDate'], '%Y-%m-%d')
        self.fiscal_date_ending = datetime.strptime(json_obj['fiscalDateEnding'], '%Y-%m-%d')

    @staticmethod
    def parse_json_list(json_list):
        json_list = list(filter(lambda json_obj: (json_obj['surprise'] != 'None'), json_list))
        res_list = list(map(lambda json_obj: QuarterlyEarnings(json_obj), json_list))
        return list(filter(None, res_list))
