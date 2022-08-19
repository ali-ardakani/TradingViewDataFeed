<div align="center">
<!-- Title: -->
<h1>TradingView Datafeed</h1>
<!-- Description: -->
<p>Computes the performance summary for a list of transactions downloaded from site TradingView.</p>
</div>

<div>
<!-- Table of Contents: -->
<h2>Table of Contents</h2>
<ul>
<li><a href="#installation">Installation</a></li>
<li><a href="#usage">Usage</a></li>
<li><a href="#performance-summary">Performance Summary</a></li>
<li><a href="#monthly-performance">Monthly Performance</a></li>
<ul>
</div>

<div>
<!-- Installation: -->
<h2 id="installation">Installation</h2>
<p>
<!-- Install the package: -->
<code>pip install -r requirements.txt</code>
</p>
</div>
 
<div>
<!-- Usage: -->
<h2 id="usage">Usage</h2>
<p>
<!-- Read trades from a csv file: -->
<code># Read trades from a csv file</code>
<code>import pandas as pd</code>
<code>trades = pd.read_csv("trades.csv")</code>

<!-- Construct a DataFrameTV object from a trades DataFrame downloaded from site TradingView: -->
<code># Construct a DataFrameTV object from a trades DataFrame downloaded from site TradingView</code>
<code>from tradingview import DataFrameTV</code>
<code>datafeed = DataFrameTV(trades)</code>
</p>

<h3 id="performance-summary">Performance Summary</h2>
<p>
<!-- Get performance summary: -->
<code># Get performance summary</code>
<code>datafeed.performance_summary</code>
<!-- Output: -->
<code># Output:</code>
<code>    
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
</code>
</br>
Note: Use <code>datafeed.performance_summary_long</code> and <code>datafeed.performance_summary_short</code> to get the performance summary for long and short trades.
</p>
 
<h3 id="monthly-performance">Monthly Performance</h2>
<p>
<!-- Get monthly performance: -->
<code># Get monthly performance</code>
<code>datafeed.monthly_performance()</code>
<!-- Output: -->
<code># Output:</code>
<code>
                Net Profit  Net Profit %  Gross Profit  Gross Profit %  ...  Largest Losing Trade %  Avg Bars in Trades  Avg Bars in Winning Trades  Avg Bars in Losing Trades
    2022-06-30     -116.72     -0.116720      90037.22       90.037294  ...                   -5.71     0 days 04:28:56             0 days 03:57:07            0 days 05:15:52
    2022-07-31    -1229.05     -1.230489      65434.20       65.510793  ...                   -5.50     0 days 09:43:28             0 days 09:20:32            0 days 10:13:45
    2022-08-31    26979.87     27.346035      36995.39       37.497483  ...                   -3.63     0 days 17:30:15             0 days 15:19:04            1 days 02:15:00
</code>
<!-- Note: -->
</br>
Note: If you want the result to be shown along with shorts and longs in the monthly performance, set the with_separate_long_short parameter to True.
</p>
</div>
