from datetime import datetime, timedelta, date

from get_finance_data import GetFinanceData


class GenerateStocksGraphState:
    def __init__(self):
        self.from_date = datetime.now() - timedelta(days=5)
        self.to_date = datetime.now()
        self.stocks_list = []


class GenerateStocksGraphError:
    def __init__(self, err_str):
        self.err_str = err_str


class GenerateStocksGraphBloc:
    def __init__(self):
        self.state = GenerateStocksGraphState()
        self._listeners = []

    def choose_from_to_dates(self, from_date, to_date):
        if from_date > date.today() or to_date > date.today():
            return GenerateStocksGraphError('Choose Dates From The Past!!')
        if from_date > to_date:
            return GenerateStocksGraphError('From Date Should be Before To Date!!')

        self.state.from_date = from_date
        self.state.to_date = to_date
        self._notify_listeners()
        return self.state

    def add_to_stocks_list(self, stock_name):
        if not GetFinanceData().is_valid_ticker_name(stock_name):
            return GenerateStocksGraphError('Wrong stock name {0}!!'.format(stock_name))
        self.state.stocks_list.append(stock_name)
        self._notify_listeners()
        return self.state

    def clear_stocks_list(self):
        self.state.stocks_list.clear()
        self._notify_listeners()

    def _notify_listeners(self):
        for listener in self._listeners:
            listener(self.state)

    def add_listener(self, listener):
        self._listeners.append(listener)

