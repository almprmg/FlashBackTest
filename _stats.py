
import numpy as np
import pandas as pd
from _util import _data_period


def geometric_mean(returns: pd.Series) -> float:
    returns = returns.fillna(0) + 1
    if np.any(returns <= 0):
        return 0
    return np.exp(np.log(returns).sum() / (len(returns) or np.nan)) - 1

def compute_stats(
        trades: pd.DataFrame,
        ohlc_data: pd.DataFrame,
) -> pd.Series:

    equity = trades['CumProfit'].to_numpy()
    index = ohlc_data.index
    dd = 1 - equity / np.maximum.accumulate(equity)


    # Came straight from Backtest.run()
    trades_df = pd.DataFrame({
            'Size': trades.Quantity,
            'EntryPrice': trades.enter_price ,
            'ExitPrice': trades.exit_price,
            'PnL': trades.PnL,
            'ReturnPct': trades.pct,
            'EntryTime': trades.enter_time ,
            'ExitTime': trades.exit_time ,
        })
    trades_df['Duration'] = trades_df['ExitTime'] - trades_df['EntryTime']
    del trades

    pl = trades_df['PnL']
    returns = trades_df['ReturnPct']
    durations = trades_df['Duration']

    def _round_timedelta(value, _period=_data_period(index)):
        if not isinstance(value, pd.Timedelta):
            return value
        resolution = getattr(_period, 'resolution_string', None) or _period.resolution
        return value.ceil(resolution)
    s = pd.Series(dtype=object)
    def _compute_all():
       
        s.loc['Start'] = index[0]
        s.loc['End'] = index[-1]
        s.loc['Duration'] = s.End - s.Start
        s.loc['Equity Final [$]'] = equity[-1]
        s.loc['Equity Peak [$]'] = equity.max()
        s.loc['Return [%]'] = (equity[-1] - equity[0]) / equity[0] * 100
        c = ohlc_data.Close.values
        s.loc['Buy & Hold Return [%]'] = (c[-1] - c[0]) / c[0] * 100  # long-only return
        max_dd = -np.nan_to_num(dd.max())
        s.loc['Max. Drawdown [%]'] = max_dd * 100
    def _trade_compute():
        s.loc['# Trades'] = n_trades = len(trades_df)
        s.loc['Win Rate [%]'] = np.nan if not n_trades else (pl > 0).sum() / n_trades * 100  # noqa: E501
        s.loc['Best Trade [%]'] = returns.max() * 100
        s.loc['Worst Trade [%]'] = returns.min() * 100
        mean_return = geometric_mean(returns)
        s.loc['Avg. Trade [%]'] = mean_return * 100
        s.loc['Max. Trade Duration'] = _round_timedelta(durations.max())
        s.loc['Avg. Trade Duration'] = _round_timedelta(durations.mean())
        s.loc['Profit Factor'] = returns[returns > 0].sum() / (abs(returns[returns < 0].sum()) or np.nan)  # noqa: E501
        s.loc['Expectancy [%]'] = returns.mean() * 100
        s.loc['SQN'] = np.sqrt(n_trades) * pl.mean() / (pl.std() or np.nan)
        s.loc['_trades'] = trades_df
    _compute_all()
    _trade_compute()


    s = _Stats(s)
    return s




class _Stats(pd.Series):
    def __repr__(self):
        # Prevent expansion due to _equity and _trades dfs
        with pd.option_context('max_colwidth', 20):
            return super().__repr__()
