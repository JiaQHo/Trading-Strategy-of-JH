# Trading-Strategy-of-JH
Setting by MACD, MA, Vol, and many other methods. To analysis the potential trend of the stock each day.
# 优势
计算方式仅借助pandas和numpy，方便了解计算过程，调整参数和可视化。  
# 简介
1. 根据MACD是否出现背离判断当前收盘价是否适合买入。  
2. 根据收盘价是否跌破或突破移动均线（20，60，150，300日）判断其趋势。  
3. 根据成交量与股价的关系作短期判断（例如量增价减视为下跌趋势）。  
4. 具体参数设置及计算方法见脚本。  
