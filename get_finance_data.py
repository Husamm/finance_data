import polygon
from polygon import RESTClient
from datetime import datetime, timedelta
from urllib.request import urlopen
import json

from polygon.rest.models import Agg

POLYGON_API_KEY = 'T1SYYcOIqlp0edh1Y17IdNBad0873V5_'
ALPHAVANTAGE_API_KEY = 'MJUGHAYZ89VMQ2VE'
YEARS_BACK = 2.0


class GetFinanceData:
    def __init__(self):
        self.client = RESTClient(POLYGON_API_KEY)

    def is_valid_ticker_name(self, ticker_name):
        try:
            return len(list(self.client.list_tickers(ticker=ticker_name))) != 0
        except Exception as err:
            return 0

    def get_ticker_aggs(self, ticker, from_date, to_date):
        try:
            polygon_aggs = self.client.get_aggs(ticker=ticker, from_=from_date.strftime("%Y-%m-%d"),
                                                to=to_date.strftime("%Y-%m-%d"), limit=5000, multiplier=1,
                                                timespan='day')
        except Exception as error:
            print('-E- ', error)
            return None
        return list(map(lambda polygon_agg: Aggregate(polygon_agg), polygon_aggs))

    def get_EPS_annoucments(self, ticker):
        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        return QuarterlyEarnings.parse_json_list(data_json['quarterlyEarnings'])


class Aggregate:
    def __init__(self, polygon_agg: Agg):
        self.open = polygon_agg.open
        self.close = polygon_agg.close
        self.high = polygon_agg.high
        self.low = polygon_agg.low
        self.volume = polygon_agg.volume
        self.timestamp = polygon_agg.timestamp

    def __str__(self):
        return f"Aggregate(open={self.open}, close={self.close}, high={self.high}, low={self.low}, volume={self.volume}, timestamp={self.timestamp})"

    def __repr__(self):
        return self.__str__()

    def to_csv_map(self):
        agg_time = datetime.fromtimestamp(self.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return {'time': agg_time, 'open': str(self.open),
                'close': str(self.close), 'high': str(self.high), 'low': str(self.low), 'volume': str(self.volume)}


class QuarterlyEarnings:
    def __str__(self):
        return f"QuarterlyEarnings(surprise_percentage={self.surprise_percentage}, surprise={self.surprise}, estimated_EPS={self.estimated_EPS}, reported_EPS={self.reported_EPS}, reported_date={self.reported_date}, fiscal_date_ending={self.fiscal_date_ending})"

    def __repr__(self):
        return self.__str__()

    def __init__(self, json_obj):
        self.surprise_percentage = float(json_obj['surprisePercentage'])
        self.surprise = float(json_obj['surprise'])
        self.estimated_EPS = float(json_obj['estimatedEPS'])
        self.reported_EPS = float(json_obj['reportedEPS'])
        self.reported_date = datetime.strptime(json_obj['reportedDate'], '%Y-%m-%d')
        self.fiscal_date_ending = datetime.strptime(json_obj['fiscalDateEnding'], '%Y-%m-%d')

    def to_csv_map(self):
        return {'surprise_percentage': str(self.surprise_percentage),
                'surprise': str(self.surprise),
                'estimated_EPS': str(self.estimated_EPS),
                'reported_EPS': str(self.reported_EPS),
                'reported_date': self.reported_date.strftime('%Y-%m-%d'),
                'fiscal_date_ending': self.fiscal_date_ending.strftime('%Y-%m-%d')}

    @staticmethod
    def parse_json_list(json_list):
        json_list = list(filter(lambda json_obj: (json_obj['surprise'] != 'None'), json_list))
        res_list = list(map(lambda json_obj: QuarterlyEarnings(json_obj), json_list))
        return list(filter(None, res_list))
