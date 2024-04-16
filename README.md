**Project Documentation - README.md**

# FlashBackTesting

[FlashBackTesting] Backtesting and Strategy Implementation

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#License)
- [Contact](#contact)

## Introduction

The [FlashBackTesting] project provides a backtesting framework and strategy implementation for analyzing financial data. This documentation serves as a guide to understand the project,it enables it to show highly accurate results by using smaller frames and simulating the live test., its setup, and how to utilize its features effectively.

## Prerequisites

Before getting started with [FlashBackTesting], ensure that you have the following prerequisites installed on your machine:

- Python (version >=  10.9.1)
- pandas (version >= '1.5.3')
- numpy (version >= 1.23.5')


## Installation

To install [FlashBackTesting], follow these steps:

1. Clone the repository: `git clone https://github.com/almprmg/FastBackTest/.git`
2. Change into the project directory: `cd FastBackTest`

## Usage

To use [FlashBackTesting], follow these guidelines:

1. Import the necessary libraries:
```python
import pandas as pd
from BackTest_bisc import FlashBackTesting
from Stratigy import Strategy
```

2. Set up the required variables and data:
```python
timeframe_high = "1h"
timeframe_low = "5m"
symbol = "AGLDUSDT"
data_low = pd.read_csv(f'........./data/{timeframe_low}/{symbol}.csv', index_col=0)
df1 = pd.read_csv(f'.....\{timeframe_high}/{symbol}.csv', index_col=0)
data_low.index = pd.to_datetime(data_low.index)

df1["Date"] = pd.to_datetime(df1["Date"], unit='ms')
df1 = df1.set_index('Date')
```

3. Define your strategy class by extending the base `Strategy` class:
```python
class myClass(Strategy):
    def init(self) -> None:
       super().init()

    def next(self) -> None:
        super().next()
        if self.data.Signal[-1] == 1:
            self.limit = self.data.highest_top[-1]
            highest_top = self.data.highest_bot[-1]
            self.sl = highest_top - ((self.limit - highest_top) * 3)
            self.tp = highest_top + ((self.limit - highest_top) * 5)
            self.buy(limit=self.limit, tp=self.tp, sl=self.sl)
        elif -1 != None and self.data.Signal[-1] == 2:
            self.limit = self.data.highest_bot[-1]
            highest_top = self.data.highest_top[-1]
            self.sl = highest_top - ((self.limit - highest_top) * 3)
            self.tp = highest_top + ((self.limit - highest_top) * 5)
            self.sell(limit=self.limit, tp=self.tp, sl=self.sl)
```

4. Create an instance of the `FlashBackTesting` class and run the backtest:
```python
bt = FlashBackTesting(df1, data_low, myClass, ratio_entry=20, cp=True)
bt.run()
```

5. Access the backtesting results:
```python
bt.result

            Start                    2022-08-26 18:00:00
            End                      2023-08-26 17:00:00
            Duration                   364 days 23:00:00
            Equity Final [$]                  782.198334
            Equity Peak [$]                  1013.011602
            Return [%]                        -22.463471
            Buy & Hold Return [%]              38.636364
            Max. Drawdown [%]                 -25.033789
            # Trades                                  71
            Win Rate [%]                       50.704225
            Best Trade [%]                     15.873016
            Worst Trade [%]                   -27.142857
            Avg. Trade [%]                     -2.049075
            Max. Trade Duration         27 days 17:00:00
            Avg. Trade Duration          2 days 03:00:00
            Profit Factor                       0.624392
            Expectancy [%]                     -1.647243
            SQN                                -1.609426
            _trades                            Size  ...
            dtype: obj
```

## Contributing

Contributions to [FlashBackTesting] are welcome! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code passes all tests.
4. Commit your changes with descriptive commit messages.
5. Push your branch to your forked repository.
6. Open a pull request, providing a detailed description of your changes.
## Features
1. Simple, well-documented API
2. Blazing fast execution
3. Supports any financial instrument with candlestick data
3. Detailed results
4. Accuracy in results
## License
[(AGPL-3.0 License](LICENSE)

## Contact

For any questions or feedback, please contact:

- [Hareth AL-Maqtari]: [uuyyhh9009@gmail.com]


---
