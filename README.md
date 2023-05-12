# Trading-Strategy-of-JH
Setting by MACD, MA, Vol, and many other methods. To analysis the potential trend of the stock each day.
# 优势
计算方式仅借助pandas和numpy，方便了解计算过程，调整参数和可视化。  
analysis_linear_close这一指标的计算方式为自编，根据收盘价以时间序列分为上升或下降，再构建线性回归，根据回归斜率以及收盘价关系确定是否适合买卖。  
# 简介
1. 导入csv的格式参照tushare。  
2. analysis分别用于计算buy、rise、decline、sell信号。  
3. A_strategy等权整合上述信号，分别用于测试交易策略、参数选择以及策略准确性。  
4. 根据MACD是否出现背离判断当前收盘价是否适合买入。  
5. 根据收盘价是否跌破或突破移动均线（20，60，150，300日）判断其趋势。  
6. 根据成交量与股价的关系作短期判断（例如量增价减视为下跌趋势）。  
7. 具体参数设置及计算方法见脚本。  
# 展望  
1. 优化票池以及可调参数。  
2. 简化交易策略（加入网格化&量化优化仓位，降低回撤）。  
