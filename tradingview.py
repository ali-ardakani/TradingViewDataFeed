import math
import pandas as pd
from dataclasses import dataclass


class Type:
    LONG = 'long'
    SHORT = 'short'


@dataclass
class Trade:
    type: Type
    entry_date: float
    entry_price: float
    contract: float
    entry_signal: str = None
    exit_date: float = None
    exit_price: float = None
    exit_signal: str = None
    profit: float = None
    profit_percent: float = None
    draw_down: float = None
    draw_down_percent: float = None
    run_up: float = None
    run_up_percent: float = None
    cum_profit: float = None
    cum_profit_percent: float = None


@dataclass
class PerformanceSummary:
    net_profit: float
    net_profit_percent: float
    gross_profit: float
    gross_profit_percent: float
    gross_loss: float
    gross_loss_percent: float
    max_run_up: float
    max_run_up_percent: float
    max_draw_down: float
    max_draw_down_percent: float
    buy_and_hold: float
    buy_and_hold_percent: float
    profit_factor: float
    max_contract_held: float
    total_closed_trades: int
    total_open_trades: int
    number_winning_trades: int
    number_losing_trades: int
    percent_profitable: float
    avg_trade: float
    avg_trade_percent: float
    avg_winning_trade: float
    avg_winning_trade_percent: float
    avg_losing_trade: float
    avg_losing_trade_percent: float
    ratio_avg_win_avg_loss: float
    largest_winning_trade: float
    largest_winning_trade_percent: float
    largest_losing_trade: float
    largest_losing_trade_percent: float
    avg_bars_in_trades: int
    avg_bars_in_winning_trades: int
    avg_bars_in_losing_trades: int


class DataFrameTV:
    """
    Computes the performance summary for a list of transactions downloaded from site TradingView.
    
    Example:
    --------
    Read trades from file:
    
    >>> import pandas as pd
    >>> trades = pd.read_csv(<path to file>)
    
    Construct a DataFrameTV object from a trades DataFrame downloaded from site TradingView.
    
    >>> dftv = DataFrameTV(trades)
    
    Computes the performance summary for the trades.
    
    >>> dftv.performance_summary
    Net Profit                            25634.1
    Net Profit %                        25.634121
    Gross Profit                        192466.81
    Gross Profit %                     192.466967
    Gross Loss                         -166832.71
    Gross Loss %                      -166.832846
    Max Run Up                            6013.65
    Max Run Up %                              6.5
    Max Draw Down                        -5975.55
    Max Draw Down %                          -6.1
    Buy and Hold                    -24347.780603
    Buy and Hold %                     -24.347801
    Profit Factor                        1.153652
    Max Contract Held                     5.36759
    Total Closed Trades                       184
    Total Open Trades                           1
    Number Winning Trades                     112
    Number Losing Trades                       72
    Avg Trade                          139.315761
    Avg Trade %                          0.150326
    Avg Winning Trade                 1718.453661
    Avg Winning Trade %                  1.787946
    Avg Losing Trade                 -2317.120972
    Avg Losing Trade %                  -2.397083
    Ratio Avg Win Avg Loss               0.741633
    Largest Winning Trade                 5404.13
    Largest Winning Trade %                  5.84
    Largest Losing Trade                 -5819.46
    Largest Losing Trade %                  -5.71
    Avg Bars in Trades            0 days 07:44:58
    Avg Bars in Winning Trades    0 days 07:21:23
    Avg Bars in Losing Trades     0 days 08:21:40
    dtype: object
    
    Monthly performance summary for the trades.
    
    >>> dftv.monthly_performance()
                Net Profit  Net Profit %  Gross Profit  Gross Profit %  ...  Largest Losing Trade %  Avg Bars in Trades  Avg Bars in Winning Trades  Avg Bars in Losing Trades
    2022-06-30     -116.72     -0.116720      90037.22       90.037294  ...                   -5.71     0 days 04:28:56             0 days 03:57:07            0 days 05:15:52
    2022-07-31    -1229.05     -1.230489      65434.20       65.510793  ...                   -5.50     0 days 09:43:28             0 days 09:20:32            0 days 10:13:45
    2022-08-31    26979.87     27.346035      36995.39       37.497483  ...                   -3.63     0 days 17:30:15             0 days 15:19:04            1 days 02:15:00
    """

    def __init__(self, trades: pd.DataFrame):
        self.trades = [
            ConvertTradeTV.convert(trade[1])
            for trade in trades.groupby("Trade #") if len(trade) == 2
        ]

    @property
    def performance_summary(self):
        return PerformanceSummary.performance_summary(self.trades)

    @property
    def performance_summary_long(self):
        long_trades = [trade for trade in self.trades if trade.type == "long"]
        return PerformanceSummary.performance_summary(long_trades)

    @property
    def performance_summary_short(self):
        short_trades = [
            trade for trade in self.trades if trade.type == "short"
        ]
        return PerformanceSummary.performance_summary(short_trades)

    def monthly_performance(self,
                            with_separate_long_short: bool = False
                            ) -> pd.DataFrame:
        """
        Returns a DataFrame with monthly performance summary.
        
        Parameters
        ----------
        with_separate_long_short: If True, returns performance summary separately for long and short trades.
            else returns performance summary for all trades.
        """
        return PerformanceSummary.monthly_performance(
            self.trades, with_separate_long_short)

    def __repr__(self) -> str:
        return self.performance_summary.__repr__()


class ConvertTradeTV:

    @staticmethod
    def convert(pair_trade: pd.DataFrame) -> Trade:
        _entry = pair_trade.iloc[1]
        _exit = pair_trade.iloc[0]
        _type = _entry.Type.split(" ")[1].lower()
        trade = Trade(
            type=Type.LONG if _type == "long" else Type.SHORT,
            entry_date=pd.to_datetime(_entry["Date/Time"]),
            exit_date=pd.to_datetime(_exit["Date/Time"]),
            entry_price=_entry["Price"],
            exit_price=_exit["Price"],
            contract=_entry["Contracts"],
            entry_signal=_entry["Signal"],
            exit_signal=_exit["Signal"],
            profit=_entry["Profit USDT"],
            profit_percent=_entry["Profit %"],
            draw_down=_entry["Drawdown USDT"],
            draw_down_percent=_entry["Drawdown %"],
            run_up=_entry["Run-up USDT"],
            run_up_percent=_entry["Run-up %"],
            cum_profit=_entry["Cum. Profit USDT"],
            cum_profit_percent=_entry["Cum. Profit %"],
        )
        return trade


class PerformanceSummary:

    @staticmethod
    def performance_summary(trades: list or pd.DataFrame):
        net_profit = CalculatePerformanceSummary.net_profit(trades)
        net_profit_percent = CalculatePerformanceSummary.net_profit_percent(
            trades)
        gross_profit = CalculatePerformanceSummary.gross_profit(trades)
        gross_profit_percent = CalculatePerformanceSummary.gross_profit_percent(
            trades)
        gross_loss = CalculatePerformanceSummary.gross_loss(trades)
        gross_loss_percent = CalculatePerformanceSummary.gross_loss_percent(
            trades)
        max_run_up = CalculatePerformanceSummary.max_run_up(trades)
        max_run_up_percent = CalculatePerformanceSummary.max_run_up_percent(
            trades)
        max_draw_down = CalculatePerformanceSummary.max_draw_down(trades)
        max_draw_down_percent = CalculatePerformanceSummary.max_draw_down_percent(
            trades)
        buy_and_hold = CalculatePerformanceSummary.buy_and_hold(trades)
        buy_and_hold_percent = CalculatePerformanceSummary.buy_and_hold_percent(
            trades)
        profit_factor = CalculatePerformanceSummary.profit_factor(trades)
        max_contract_held = CalculatePerformanceSummary.max_contract_held(
            trades)
        total_closed_trades = CalculatePerformanceSummary.total_closed_trades(
            trades)
        total_open_trades = CalculatePerformanceSummary.total_open_trades(
            trades)
        number_winning_trades = CalculatePerformanceSummary.number_winning_trades(
            trades)
        number_losing_trades = CalculatePerformanceSummary.number_losing_trades(
            trades)
        avg_trade = CalculatePerformanceSummary.avg_trade(trades)
        avg_trade_percent = CalculatePerformanceSummary.avg_trade_percent(
            trades)
        avg_winning_trade = CalculatePerformanceSummary.avg_winning_trade(
            trades)
        avg_winning_trade_percent = CalculatePerformanceSummary.avg_winning_trade_percent(
            trades)
        avg_losing_trade = CalculatePerformanceSummary.avg_losing_trade(trades)
        avg_losing_trade_percent = CalculatePerformanceSummary.avg_losing_trade_percent(
            trades)
        ratio_avg_win_avg_loss = CalculatePerformanceSummary.ratio_avg_win_avg_loss(
            trades)
        largest_winning_trade = CalculatePerformanceSummary.largest_winning_trade(
            trades)
        largest_winning_trade_percent = CalculatePerformanceSummary.largest_winning_trade_percent(
            trades)
        largest_losing_trade = CalculatePerformanceSummary.largest_losing_trade(
            trades)
        largest_losing_trade_percent = CalculatePerformanceSummary.largest_losing_trade_percent(
            trades)
        avg_bars_in_trades = CalculatePerformanceSummary.avg_bars_in_trades(
            trades)
        avg_bars_in_winning_trades = CalculatePerformanceSummary.avg_bars_in_winning_trades(
            trades)
        avg_bars_in_losing_trades = CalculatePerformanceSummary.avg_bars_in_losing_trades(
            trades)
        data = [
            net_profit, net_profit_percent, gross_profit, gross_profit_percent,
            gross_loss, gross_loss_percent, max_run_up, max_run_up_percent,
            max_draw_down, max_draw_down_percent, buy_and_hold,
            buy_and_hold_percent, profit_factor, max_contract_held,
            total_closed_trades, total_open_trades, number_winning_trades,
            number_losing_trades, avg_trade, avg_trade_percent,
            avg_winning_trade, avg_winning_trade_percent, avg_losing_trade,
            avg_losing_trade_percent, ratio_avg_win_avg_loss,
            largest_winning_trade, largest_winning_trade_percent,
            largest_losing_trade, largest_losing_trade_percent,
            avg_bars_in_trades, avg_bars_in_winning_trades,
            avg_bars_in_losing_trades
        ]
        index = [
            "Net Profit", "Net Profit %", "Gross Profit", "Gross Profit %",
            "Gross Loss", "Gross Loss %", "Max Run Up", "Max Run Up %",
            "Max Draw Down", "Max Draw Down %", "Buy and Hold",
            "Buy and Hold %", "Profit Factor", "Max Contract Held",
            "Total Closed Trades", "Total Open Trades",
            "Number Winning Trades", "Number Losing Trades", "Avg Trade",
            "Avg Trade %", "Avg Winning Trade", "Avg Winning Trade %",
            "Avg Losing Trade", "Avg Losing Trade %", "Ratio Avg Win Avg Loss",
            "Largest Winning Trade", "Largest Winning Trade %",
            "Largest Losing Trade", "Largest Losing Trade %",
            "Avg Bars in Trades", "Avg Bars in Winning Trades",
            "Avg Bars in Losing Trades"
        ]
        res = pd.Series(data, index=index)
        return res

    @staticmethod
    def monthly_performance(trades: list or pd.DataFrame,
                            with_separate_long_short: bool = False):
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        trades.index = pd.to_datetime(trades.entry_date)
        monthly = trades.groupby(pd.Grouper(freq="M"))
        res = pd.DataFrame()
        for name, group in monthly:
            name = name.strftime("%Y-%m-%d")
            performance = PerformanceSummary.performance_summary(group)
            performance.name = name
            res = pd.concat([res, performance], axis=1)
            if with_separate_long_short:
                performance_long = PerformanceSummary.performance_summary(
                    group[group.type == "long"])
                performance_long.name = str(name) + " Long"
                performance_short = PerformanceSummary.performance_summary(
                    group[group.type == "short"])
                performance_short.name = str(name) + " Short"
                res = pd.concat([res, performance_long, performance_short],
                                axis=1)
        return res.T


class CalculatePerformanceSummary:

    @staticmethod
    def initial_capital(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            return trades[0].entry_price * trades[0].contract
        return trades.iloc[0].entry_price * trades.iloc[0].contract

    @staticmethod
    def net_profit(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.profit.sum()

    @staticmethod
    def net_profit_percent(trades: list or pd.DataFrame) -> float:
        net_profit = CalculatePerformanceSummary.net_profit(trades)
        initial_capital = CalculatePerformanceSummary.initial_capital(trades)
        return (net_profit / initial_capital) * 100

    @staticmethod
    def gross_profit(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].profit.sum()

    @staticmethod
    def gross_profit_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        gross_profit = CalculatePerformanceSummary.gross_profit(trades)
        initial_capital = CalculatePerformanceSummary.initial_capital(trades)
        return (gross_profit / initial_capital) * 100

    @staticmethod
    def gross_loss(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].profit.sum()

    @staticmethod
    def gross_loss_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        gross_loss = CalculatePerformanceSummary.gross_loss(trades)
        initial_capital = CalculatePerformanceSummary.initial_capital(trades)
        return (gross_loss / initial_capital) * 100

    @staticmethod
    def max_run_up(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.run_up.max()

    @staticmethod
    def max_run_up_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.run_up_percent.max()

    @staticmethod
    def max_draw_down(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return -trades.draw_down.max()

    @staticmethod
    def max_draw_down_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return -trades.draw_down_percent.max()

    @staticmethod
    def buy_and_hold(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        first_price = trades.entry_price.iloc[0]
        last_price = trades.iloc[-1].exit_price
        if math.isnan(last_price):
            last_price = trades.iloc[-1].entry_price
        return (last_price - first_price) * trades.contract.iloc[0]

    @staticmethod
    def buy_and_hold_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        buy_and_hold = CalculatePerformanceSummary.buy_and_hold(trades)
        initial_capital = CalculatePerformanceSummary.initial_capital(trades)
        return (buy_and_hold / initial_capital) * 100

    @staticmethod
    def profit_factor(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        gross_profit = CalculatePerformanceSummary.gross_profit(trades)
        gross_loss = abs(CalculatePerformanceSummary.gross_loss(trades))
        if gross_profit != 0:
            return gross_profit / gross_loss
        return gross_profit

    @staticmethod
    def max_contract_held(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.contract.max()

    @staticmethod
    def total_closed_trades(trades: list or pd.DataFrame) -> int:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
            trades = trades.dropna(subset=["contract"])
        return len(trades)

    @staticmethod
    def total_open_trades(trades: list or pd.DataFrame) -> int:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.contract.isna().sum()

    @staticmethod
    def number_winning_trades(trades: list or pd.DataFrame) -> int:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].contract.count()

    @staticmethod
    def number_losing_trades(trades: list or pd.DataFrame) -> int:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].contract.count()

    @staticmethod
    def avg_trade(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.profit.mean()

    @staticmethod
    def avg_trade_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades.profit_percent.mean()

    @staticmethod
    def avg_winning_trade(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].profit.mean()

    @staticmethod
    def avg_winning_trade_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].profit_percent.mean()

    @staticmethod
    def avg_losing_trade(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].profit.mean()

    @staticmethod
    def avg_losing_trade_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].profit_percent.mean()

    @staticmethod
    def ratio_avg_win_avg_loss(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        avg_winning_trade = CalculatePerformanceSummary\
            .avg_winning_trade(trades)
        avg_losing_trade = abs(CalculatePerformanceSummary\
            .avg_losing_trade(trades))
        return avg_winning_trade / avg_losing_trade

    @staticmethod
    def largest_winning_trade(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].profit.max()

    @staticmethod
    def largest_winning_trade_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit > 0].profit_percent.max()

    @staticmethod
    def largest_losing_trade(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].profit.min()

    @staticmethod
    def largest_losing_trade_percent(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        return trades[trades.profit < 0].profit_percent.min()

    @staticmethod
    def avg_bars_in_trades(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        duration = trades.exit_date - trades.entry_date
        return duration.mean().round("1s")

    @staticmethod
    def avg_bars_in_winning_trades(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        trades = trades[trades.profit > 0]
        duration = trades.exit_date - trades.entry_date
        return duration.mean().round("1s")

    @staticmethod
    def avg_bars_in_losing_trades(trades: list or pd.DataFrame) -> float:
        if isinstance(trades, list):
            trades = pd.DataFrame(trades)
        trades = trades[trades.profit < 0]
        duration = trades.exit_date - trades.entry_date
        return duration.mean().round("1s")
