import numpy as np
import pandas as pd
from analysis_macd import Macd
from analysis_boll import Boll
from analysis_vol import VolRatio
from analysis_kdj import KDJ
from analysis_ma import Ma
import matplotlib.pyplot as plt

# Strategy 2.23 14：00 (To be back-tested)
# 1.总体判断
# 总趋势向上？向下？横盘？（Decline与Rise的差值？Expma？Close？）
# 以此依据分类再制定具体操作（止损？止盈？激进？保守？）
# 2.某段趋势
# 连续向下趋势（Decline连续出现）,后续B的出现可视为转折点？在后续第二个B出现时权重加大？
# 连续向上趋势（Rise连续出现），后续首个S的权重减少，将减少权重转移到第二个出现的S？
# B或R出现意味某段向下的趋势结束？→买入/补仓？
# S或D出现意味某段向上的趋势结束？→卖出/平仓？
# B与S之间无明确趋势时（横盘）
# 某段内均为D或者B，B的位置持续变低→单向下行？
# 某段内均为R或者S，S的位置持续变高→单向上行？
# 当某个B的位置高于上一个B或D→反弹？（相对高位时不适用）
# 当某个S的位置低于上一个S或R→反转？
# 3.区间
# B/S 脱离某一区间后，加大权重？
# 区间判断？（B/S位置比上一次低/高）
# 当前B高于上一个周期的B/D，而S低于或接近上一个周期的S/R→观望
# 4.权重
# 单向下行后出现S→优先平仓？（止盈？）
# 单向上行不出现B→最大盈利？
# 5.执行
# 创建一个数据框/列表记录量级
# 重置？


def formulate_sign(a):
    if 'buy' in a:
        a = 'buy'
    elif 'sell' in a:
        a = 'sell'
    elif '↑' in a:
        a = '↑'
    elif '↓' in a:
        a = '↓'
    return a


# parameter
# df_parameter = pd.DataFrame({
#     'standard_for_buy_r': np.arange(0,20,2).tolist(),
#     'standard_for_buy_d': np.arange(20,0,-2).tolist(),
#     'standard_for_buy_w': np.arange(2,22,2).tolist(),
#     'standard_for_sell_r': np.arange(20,0,-2).tolist(),
#     'standard_for_sell_d': np.arange(0,20,2).tolist(),
#     'standard_for_sell_w': np.arange(2,22,2).tolist(),
#     'standard_for_holding_r': np.round(np.arange(1,0,-0.1),2).tolist(),     # 0.6
#     'standard_for_holding_d': np.round(np.arange(0,1,0.1),2).tolist(),      # 0.4
#     'standard_for_holding_w': np.round(np.arange(0.1,1.1,0.1),2).tolist(),  # 0.5
#     'degree_buy1': np.round(np.arange(0.5,1,0.05),2).tolist(),              # 0.75
#     'degree_buy2': np.round(np.arange(0.25,0.5,0.025),2).tolist(),          # 0.375
#     'degree_buy3': np.round(np.arange(0.16,0.32,0.016),2).tolist(),         # 0.25
#     'degree_buy4': np.round(np.arange(0.08,0.16,0.008),2).tolist(),         # 0.125
#     'degree_sell1': np.round(np.arange(0.5,1,0.05),2).tolist(),
#     'degree_sell2': np.round(np.arange(0.25,0.5,0.025),2).tolist(),
#     'degree_sell3': np.round(np.arange(0.16,0.32,0.016),2).tolist(),
#     'degree_sell4': np.round(np.arange(0.08,0.16,0.008),2).tolist(),
# })

df_parameter = pd.DataFrame({
    'standard_for_buy_r': [6,8,10,12,14],
    'standard_for_buy_d': [14,12,10,8,6],
    'standard_for_buy_w': [10,10,10,10,10],
    'standard_for_sell_r': [14,12,10,8,6],
    'standard_for_sell_d': [6,8,10,12,14],
    'standard_for_sell_w': [10,10,10,10,10],
    'standard_for_holding_r': [0.6,0.55,0.5,0.45,0.4],      # 0.6
    'standard_for_holding_d': [0.4,0.45,0.5,0.55,0.6],      # 0.4
    'standard_for_holding_w': [0.5,0.5,0.5,0.5,0.5],        # 0.5
    'standard_for_num_rise': [3,4,5,6,7],
    'standard_for_num_decline': [3,4,5,6,7],
    'degree_buy1': np.array([0.65,0.7,0.75,0.8,0.85])/4,                # 0.75
    'degree_buy2': np.array([0.325,0.35,0.375,0.4,0.425])/4,            # 0.375
    'degree_buy3': np.array([0.2,0.225,0.25,0.275,0.3])/4,              # 0.25
    'degree_buy4': np.array([0.075,0.1,0.125,0.15,0.175])/4,            # 0.125
    'degree_sell1': np.array([0.65,0.7,0.75,0.8,0.85])/4,                # 0.75
    'degree_sell2': np.array([0.325,0.35,0.375,0.4,0.425])/4,            # 0.375
    'degree_sell3': np.array([0.2,0.225,0.25,0.275,0.3])/4,              # 0.25
    'degree_sell4': np.array([0.075,0.1,0.125,0.15,0.175])/4,           # 0.125
    # 'degree_buy1': [0.85, 0.8, 0.75, 0.7, 0.65],  # 0.75
    # 'degree_buy2': [0.425, 0.4, 0.375, 0.35, 0.325],  # 0.375
    # 'degree_buy3': [0.3, 0.275, 0.25, 0.225, 0.2],  # 0.25
    # 'degree_buy4': [0.175, 0.15, 0.125, 0.1, 0.075],  # 0.125
    # 'degree_sell1': [0.85, 0.8, 0.75, 0.7, 0.65],  # 0.75
    # 'degree_sell2': [0.425, 0.4, 0.375, 0.35, 0.325],  # 0.375
    # 'degree_sell3': [0.3, 0.275, 0.25, 0.225, 0.2],  # 0.25
    # 'degree_sell4': [0.175, 0.15, 0.125, 0.1, 0.075]  # 0.125
})
# print(df_parameter)

df_y = pd.DataFrame(columns=("code","parameter","Current profit","Max retracement"))
i = 0

for row in df_parameter.itertuples():
    i = i+1
    standard_for_buy_r = getattr(row, 'standard_for_buy_r')
    standard_for_buy_d = getattr(row, 'standard_for_buy_r')
    standard_for_buy_w = getattr(row, 'standard_for_buy_r')
    standard_for_sell_r = getattr(row, 'standard_for_sell_r')
    standard_for_sell_d = getattr(row, 'standard_for_sell_r')
    standard_for_sell_w = getattr(row, 'standard_for_sell_r')
    standard_for_holding_r = getattr(row, 'standard_for_holding_r')
    standard_for_holding_d = getattr(row, 'standard_for_holding_r')
    standard_for_holding_w = getattr(row, 'standard_for_holding_r')
    standard_for_num_rise = getattr(row, 'standard_for_num_rise')
    standard_for_num_decline = getattr(row, 'standard_for_num_decline')
    degree_buy1 = getattr(row, 'degree_buy1')
    degree_buy2 = getattr(row, 'degree_buy2')
    degree_buy3 = getattr(row, 'degree_buy3')
    degree_buy4 = getattr(row, 'degree_buy4')
    degree_sell1 = getattr(row, 'degree_sell1')
    degree_sell2 = getattr(row, 'degree_sell2')
    degree_sell3 = getattr(row, 'degree_sell3')
    degree_sell4 = getattr(row, 'degree_sell4')

    # code_list = ["000782.SZ"]
    # code_list = ["000782.SZ","000677.SZ","601857.SH","000886.SZ"]
    code_list = ["000782.SZ", "000677.SZ", "601857.SH", "000886.SZ", "600905.SH", "000651.SZ", "000333.SZ", "601838.SH",
                 "002258.SZ", "002385.SZ", "000627.SZ", "000420.SZ", "600028.SH", "002129.SZ", "603298.SH", "002432.SZ",
                 "002969.SZ"]

    # 4.11  parameter
    # 1.生成包含预设参数的数据框
    # 2.历遍该数据框并输出不同参属下的利润率以及最大回撤率
    # 3.机器学习？

    for code in code_list:
        # 计算有关指标并整合成数据框
        df = pd.read_csv("D:/脚本/stock diary/diary_%s.csv" % code)[:300]
        # pct_chg = df['pct_chg']
        macd = Macd(df).analysis()['signal']
        boll = Boll(df).analysis()['signal']
        vol = VolRatio(df).analysis()['signal']
        avg = VolRatio(df).analysis()['AVG']
        kdj = KDJ(df).analysis()['signal']
        df_tmp = pd.DataFrame({
            'date': df['trade_date'],
            'close': df['close'],
            'high': df['high'],
            'low': df['low'],
            'avg': avg,
            'Macdsign': macd,
            'Bollsign': boll,
            'Volsign': vol,
            'Kdjsign': kdj
        })

        size_buy = list()
        size_sell = list()
        size_rise = list()
        size_decline = list()

        # 按行历遍 + 整理
        for row in df_tmp[::-1].itertuples():
            close = getattr(row,'close')
            avg = getattr(row,'avg')
            b = formulate_sign(str(getattr(row,'Bollsign')))
            m = formulate_sign(str(getattr(row,'Macdsign')))
            v = str(getattr(row,'Volsign'))
            k = str(getattr(row, 'Kdjsign'))
            list_tmp = [b,m,v,k]
            num_buy = list_tmp.count('buy')
            num_sell = list_tmp.count('sell')
            num_rise = list_tmp.count('↑')
            num_decline = list_tmp.count('↓')
            # B、S、R、D赋值1
            if num_buy > num_sell and num_buy > 1:
                size_buy.append(1*(num_buy-num_sell))
                size_sell.append(0)
            elif num_buy < num_sell and num_sell > 1:
                size_sell.append(1*(num_sell-num_buy))
                size_buy.append(0)
            else:
                size_buy.append(0)
                size_sell.append(0)

            if num_rise > num_decline and num_rise > 1:
                size_rise.append(1*(num_rise-num_decline))
                size_decline.append(0)
            elif num_rise < num_decline and num_decline > 1:
                size_decline.append(1*(num_decline-num_rise))
                size_rise.append(0)
            else:
                size_rise.append(0)
                size_decline.append(0)

        size_sell.reverse()
        size_buy.reverse()
        size_sell = np.maximum(size_sell, 0)
        size_buy = np.maximum(size_buy, 0)
        size_rise.reverse()
        size_decline.reverse()
        size_rise = np.maximum(size_rise, 0)
        size_decline = np.maximum(size_decline, 0)

        df_tmp['buy'] = size_buy
        df_tmp['sell'] = size_sell
        df_tmp['rise'] = size_rise
        df_tmp['decline'] = size_decline

        section = 20    # 周期    # parameter
        df_tmp['closehighest'] = df_tmp[::-1].close.rolling(section, min_periods=1).max()    # 周期内最高收盘价
        df_tmp['closelowest'] = df_tmp[::-1].close.rolling(section, min_periods=1).min()      # 周期内最低收盘价

        df_tmp['numbuy'] = df_tmp[::-1].buy.rolling(section, min_periods=1).sum()
        df_tmp['numsell'] = df_tmp[::-1].sell.rolling(section, min_periods=1).sum()
        df_tmp['numrise'] = df_tmp[::-1].rise.rolling(section, min_periods=1).sum()
        df_tmp['numdecline'] = df_tmp[::-1].decline.rolling(section, min_periods=1).sum()

        # accumulation_buy = np.array(size_buy)           # 2023.4.5 23:31
        # accumulation_sell = np.array(size_sell)
        # df_tmp['accumubuy'] = np.cumsum(accumulation_buy)
        # df_tmp['accumusell'] = np.cumsum(accumulation_sell)

        # print(code)
        # print(df_tmp[:60])

        zonge = 10000       # 现金+股价   # parameter
        chengben = 10000    # 成本
        mairu = 0           # 买入额
        maichu = 0          # 卖出额
        mairu_num = 0       # 买入量
        yue = 10000         # 现金余额
        yingli = 0          # 盈利
        cangwei = 0         # 仓位
        cost = 0            # 成本价
        retracement = 0     # 回撤

        last_num_buy = 0  # 区间内B的程度
        last_num_buy_close = 0  # 上一B对应收盘价
        last_num_sell = 0
        last_num_sell_close = 0
        # last_num_rise = 0
        last_rise_close = 0
        # last_num_decline = 0
        last_decline_close = 0
        ls_zonge = []
        ls_mairu = []
        ls_yue = []
        ls_yingli = [0]
        ls_cangwei = []
        ls_cost = []                # 成本价
        ls_retracement = []         # 回撤
        ls_trend = []               # 趋势
        ls_degree_buy = []          # 策略操作点
        ls_degree_sell = []         # 策略操作点
        ls_manipulation_buy = []    # 实际操作点
        ls_manipulation_sell = []   # 实际操作点
        # ls_accumulation_buy = []    # 累计策略B
        # ls_accumulation_sell = []   # 累计策略S
        # ls_stop = []
        ls_last_num_buy_close = []    # 4.15 历史买入价
        ls_last_num_sell_close = []   # 4.15 历史卖出价
        # ls_rise_close = []              # 4.15 历史rise价位
        # ls_decline_close = []           # 4.15 历史decline价位
        ls_close = []

        # 按行历遍 trend + strategy + back test
        for row in df_tmp[::-1].itertuples():
            close = getattr(row,'close')
            avg = getattr(row,'avg')
            high = getattr(row,'high')
            low = getattr(row,'low')
            close_highest = getattr(row,'closehighest')
            close_lowest = getattr(row,'closelowest')
            size_buy = getattr(row,'buy')
            size_sell = getattr(row,'sell')
            size_rise = getattr(row,'rise')
            size_decline = getattr(row,'decline')
            num_buy = getattr(row,'numbuy')
            num_sell = getattr(row,'numsell')
            num_rise = getattr(row,'numrise')
            num_decline = getattr(row,'numdecline')
            # accumulation_buy = getattr(row,'accumubuy')
            # accumulation_sell = getattr(row,'accumusell')

            # 4.15 历史收盘价，计涨跌幅
            ls_close.append(close)

            # # 1.trend
            if close == close_highest:  # highest为周期内最高收盘价
                trend = 'r'   # rise
            elif close == close_lowest:
                trend = 'd'   # decline
            else:
                trend = 'w'   # wobbled
            ls_trend.append(trend)

            # 4.15 rise close
            if size_rise != 0:
                last_rise_close = close
                # ls_rise_close.append(close)
            # else:
            #     ls_rise_close.append(0)
            # 4.15 decline close
            if size_decline != 0:
                last_decline_close = close
                # ls_decline_close.append(close)
            # else:
            #     ls_decline_close.append(0)

            # 2.parameter (adjusted by trend or holding)
            # 4.11  通过穷举/机器学习制定个股最优参数（+收益率&-最大回撤率）
            # 4.11  进一步应用到analysis中的参数优化
            if ls_trend.count('r') > ls_trend.count('d'):
                # +B -S ↓standard_for_buy +hold   +cang
                # overall_trend = 'r'
                standard_for_buy = standard_for_buy_r
                standard_for_sell = standard_for_sell_r
                standard_for_holding = standard_for_holding_r
            elif ls_trend.count('d') > ls_trend.count('r'):
                # -B +S ↑standard_for_buy -hold   -cang
                # overall_trend = 'd'
                standard_for_buy = standard_for_buy_d  # 0-20  # parameter
                standard_for_sell = standard_for_sell_d  # 0-20  # parameter
                standard_for_holding = standard_for_holding_d  # 0-1   # parameter
            else:
                # overall_trend = 'w'
                standard_for_buy = standard_for_buy_w
                standard_for_sell = standard_for_sell_w
                standard_for_holding = standard_for_holding_w

            # 3.manipulation + strategy

            # 4.11  当前B价位<上一个B价位，买入-
            # 4.11  当前S价位>上一个S价位，卖出-
            # 4.11  增加止盈点/止损点

            # number of B & S
            accumulation_buy = np.nonzero(ls_degree_buy)[0].size    # Total number of B
            accumulation_sell = np.nonzero(ls_degree_sell)[0].size  # Total number of S
            latest_days = 60    # parameter
            if len(ls_degree_buy) < latest_days:
                accumulation_buy = np.nonzero(ls_degree_buy)[0].size    # 4.13  Latest number of B in ? days
                accumulation_sell = np.nonzero(ls_degree_sell)[0].size  # 4.13  Latest number of S in ? days
            else:
                accumulation_buy = np.nonzero(ls_degree_buy[len(ls_degree_buy)-latest_days:len(ls_degree_buy)-1])[0].size
                accumulation_sell = np.nonzero(ls_degree_sell[len(ls_degree_sell)-latest_days:len(ls_degree_sell)-1])[0].size
            
            # 4.15
            # accumulation_buy = sum(ls_degree_buy)
            # accumulation_sell = sum(ls_degree_sell)
            
            # strategy
            # 4.13  止盈/止损点设置
            # 4.15 当前卖出价小于阶段内上一卖出价，清仓？
            # 4.15 当前卖出价接近上一买入价，清仓？
            # 4.15 短期增幅较大，清仓？

            # buy
            if size_buy >= 1 and num_buy > standard_for_buy and close > last_num_buy_close:
                # 仓位管理
                # if cangwei > standard_for_holding:
                #     degree_buy = degree_buy4
                if accumulation_buy < accumulation_sell:
                    if 2 * accumulation_sell - accumulation_buy > accumulation_sell:
                        degree_buy = degree_buy1
                    else:
                        degree_buy = degree_buy2
                else:
                    degree_buy = degree_buy3
                # degree_buy = 0.5
                last_num_buy_close = close
                ls_last_num_buy_close.append(close)     # 4.15
                ls_degree_buy.append(degree_buy)
            elif size_buy >= 1 and last_decline_close <= close:  # 4.15 additional indicator 当前买入价大于上一D价位
                # 仓位管理
                # if cangwei > standard_for_holding:
                #     degree_buy = degree_buy4
                if accumulation_buy < accumulation_sell:
                    if 2 * accumulation_sell - accumulation_buy > accumulation_sell:
                        degree_buy = degree_buy1
                    else:
                        degree_buy = degree_buy2
                else:
                    degree_buy = degree_buy3
                # degree_buy = 0.5
                last_num_buy_close = close
                ls_last_num_buy_close.append(close)     # 4.15
                ls_degree_buy.append(degree_buy)
            elif size_buy >= 1 and num_decline > standard_for_num_decline:   # parameter
                # 仓位管理
                # if cangwei > standard_for_holding:
                #     degree_buy = degree_buy4
                if accumulation_buy < accumulation_sell:
                    if 2 * accumulation_sell - accumulation_buy > accumulation_sell:
                        degree_buy = degree_buy1
                    else:
                        degree_buy = degree_buy2
                else:
                    degree_buy = degree_buy3
                # degree_buy = 0.5
                last_num_buy_close = close
                ls_last_num_buy_close.append(close)     # 4.15
                ls_degree_buy.append(degree_buy)
            else:
                degree_buy = 0
                ls_degree_buy.append(degree_buy)
            # 4.15 degree_buy adjustment
            # if degree_buy != 0 and last_decline_close > close:
            #     degree_buy = degree_buy * 0.5
            # elif degree_buy != 0 and last_decline_close < close:
            #     degree_buy = degree_buy * 2

            # sell
            if size_sell >= 1 and num_sell > standard_for_sell:
                # 仓位管理
                # if cangwei < standard_for_holding:
                #     degree_sell = degree_sell4
                if accumulation_buy > accumulation_sell:
                    if 2 * accumulation_buy - accumulation_sell > accumulation_buy:
                        degree_sell = degree_sell1
                    else:
                        degree_sell = degree_sell2
                else:
                    degree_sell = degree_sell3
                # degree_sell = 0.5
                last_num_sell_close = close
                ls_last_num_sell_close.append(close)     # 4.15
                ls_degree_sell.append(degree_sell)
            elif size_sell >= 1 and last_rise_close:      # 4.15 additional indicator
                if (last_rise_close - close) / last_rise_close > 0.03:       # 当前卖出价小于上一R价位 # parameter
                    # 仓位管理
                    # if cangwei < standard_for_holding:
                    #     degree_sell = degree_sell4
                    if accumulation_buy > accumulation_sell:
                        if 2 * accumulation_buy - accumulation_sell > accumulation_buy:
                            degree_sell = degree_sell1
                        else:
                            degree_sell = degree_sell2
                    else:
                        degree_sell = degree_sell3
                    # degree_sell = 0.5
                    last_num_sell_close = close
                    ls_last_num_sell_close.append(close)  # 4.15
                    ls_degree_sell.append(degree_sell)
                else:
                    degree_sell = 0
                    ls_degree_sell.append(degree_sell)
            elif size_sell >= 1 and num_rise > standard_for_num_rise:   # parameter
                # 仓位管理
                # if cangwei < standard_for_holding:
                #     degree_sell = degree_sell4
                if accumulation_buy > accumulation_sell:
                    if 2 * accumulation_buy - accumulation_sell > accumulation_buy:
                        degree_sell = degree_sell1
                    else:
                        degree_sell = degree_sell2
                else:
                    degree_sell = degree_sell3
                # degree_sell = 0.5
                last_num_sell_close = close
                ls_last_num_sell_close.append(close)     # 4.15
                ls_degree_sell.append(degree_sell)
            else:
                degree_sell = 0
                ls_degree_sell.append(degree_sell)
            # 4.15 degree_sell adjustment
            if degree_sell != 0 and (close - ls_close[-3])/ls_close[-3] >= 0.2:    # 4.15 短期20%涨幅清仓止盈
                degree_sell = 1
            elif degree_sell != 0 and (close - ls_close[-4])/ls_close[-4] >= 0.2:    # 4.15 短期20%涨幅清仓止盈
                degree_sell = 1
            elif degree_sell != 0 and (close - ls_close[-5])/ls_close[-5] >= 0.2:    # 4.15 短期20%涨幅清仓止盈
                degree_sell = 1
            # elif degree_sell != 0 and abs((close-last_num_buy_close)/close) < 0.03:    # 当前卖出价接近上一买入价，清
            #     degree_sell = 1

            # 4.back test
            # retracement & profit
            if degree_buy != 0 and (1-cangwei) >= degree_buy:
                mairu_num = mairu_num + (degree_buy * chengben) // avg   # current stock number
                mairu = mairu_num * avg                                  # current stock in market
                yue = yue - ((degree_buy * chengben) // avg) * avg       # current balance
                zonge = yue + mairu
                cangwei = cangwei + degree_buy
                yingli = zonge - chengben
                # 计算成本价
                if mairu_num != 0:
                    cost = (mairu-yingli) / mairu_num
                else:
                    cost = 0
                # 回撤
                if yingli < ls_yingli[-1]:
                    retracement = max(ls_yingli) - yingli
                else:
                    retracement = 0
                ls_mairu.append(mairu)
                ls_zonge.append(zonge)
                ls_yue.append(yue)
                ls_yingli.append(yingli)
                ls_cangwei.append(cangwei)
                ls_manipulation_buy.append(degree_buy)
                ls_manipulation_sell.append(0)
                ls_cost.append(cost)
                ls_retracement.append(retracement)
            elif degree_buy != 0 and (1-cangwei) < degree_buy:
                degree_buy = 1-cangwei
                mairu_num = mairu_num + (degree_buy * chengben) // avg   # current stock number
                mairu = mairu_num * avg                                  # current stock in market
                yue = yue - ((degree_buy * chengben) // avg) * avg       # current balance
                zonge = yue + mairu
                cangwei = cangwei + degree_buy
                yingli = zonge - chengben
                # 计算成本价
                if mairu_num != 0:
                    cost = (mairu-yingli) / mairu_num
                else:
                    cost = 0
                # 回撤
                if yingli < ls_yingli[-1]:
                    retracement = max(ls_yingli) - yingli
                else:
                    retracement = 0
                ls_mairu.append(mairu)
                ls_zonge.append(zonge)
                ls_yue.append(yue)
                ls_yingli.append(yingli)
                ls_cangwei.append(cangwei)
                ls_manipulation_buy.append(degree_buy)
                ls_manipulation_sell.append(0)
                ls_cost.append(cost)
                ls_retracement.append(retracement)
            elif degree_sell != 0 and cangwei >= degree_sell:
                maichu = int(mairu_num * degree_sell / cangwei) * avg
                mairu_num = mairu_num * (cangwei - degree_sell) / cangwei
                mairu_num = int(mairu_num)
                mairu = mairu_num * avg
                yue = yue + maichu
                zonge = yue + mairu
                cangwei = cangwei - degree_sell
                yingli = zonge - chengben
                if mairu_num != 0:
                    cost = (mairu-yingli) / mairu_num
                else:
                    cost = 0
                if yingli < ls_yingli[-1]:
                    retracement = max(ls_yingli) - yingli
                else:
                    retracement = 0
                ls_mairu.append(mairu)
                ls_zonge.append(zonge)
                ls_yue.append(yue)
                ls_yingli.append(yingli)
                ls_cangwei.append(cangwei)
                ls_manipulation_sell.append(degree_sell)
                ls_manipulation_buy.append(0)
                ls_cost.append(cost)
                ls_retracement.append(retracement)
            elif degree_sell != 0 and 0 < cangwei < degree_sell:
                degree_sell = cangwei
                maichu = int(mairu_num * degree_sell / cangwei) * avg
                mairu_num = mairu_num * (cangwei - degree_sell) / cangwei
                mairu_num = int(mairu_num)
                mairu = mairu_num * avg
                yue = yue + maichu
                zonge = yue + mairu
                cangwei = cangwei - degree_sell
                yingli = zonge - chengben
                if mairu_num != 0:
                    cost = (mairu-yingli) / mairu_num
                else:
                    cost = 0
                if yingli < ls_yingli[-1]:
                    retracement = max(ls_yingli) - yingli
                else:
                    retracement = 0
                ls_mairu.append(mairu)
                ls_zonge.append(zonge)
                ls_yue.append(yue)
                ls_yingli.append(yingli)
                ls_cangwei.append(cangwei)
                ls_manipulation_sell.append(degree_sell)
                ls_manipulation_buy.append(0)
                ls_cost.append(cost)
                ls_retracement.append(retracement)
            else:
                mairu = mairu_num * avg
                zonge = yue + mairu
                yingli = zonge - chengben
                if mairu_num != 0:
                    cost = (mairu-yingli) / mairu_num
                else:
                    cost = 0
                if yingli < ls_yingli[-1]:
                    retracement = max(ls_yingli) - yingli
                else:
                    retracement = 0
                ls_mairu.append(mairu)
                ls_zonge.append(zonge)
                ls_yue.append(yue)
                ls_yingli.append(yingli)
                ls_cangwei.append(cangwei)
                ls_manipulation_buy.append(0)
                ls_manipulation_sell.append(0)
                ls_cost.append(cost)
                ls_retracement.append(retracement)

        ls_mairu.reverse()
        ls_zonge.reverse()
        ls_yue.reverse()
        del ls_yingli[0]
        ls_yingli.reverse()
        ls_cangwei.reverse()
        ls_cost.reverse()
        ls_retracement.reverse()

        ls_trend.reverse()
        ls_degree_buy.reverse()         # theory B
        ls_degree_sell.reverse()        # theory S
        # ls_accumulation_buy.reverse()   # accumulation of theory B
        # ls_accumulation_sell.reverse()  # accumulation of theory S
        ls_manipulation_buy.reverse()   # fact B
        ls_manipulation_sell.reverse()  # fact S

        dict_y = {"code": code, "parameter": i, "Current profit": round(ls_yingli[0]/100,2),
                  "Max retracement": round(max(ls_retracement)/100,2)}
        df_y.loc[len(df_y)] = dict_y
        # print(code, '\tCurrent profit:', round(ls_yingli[0]/100,2),
        #       '\t Max retracement', round(max(ls_retracement)/100,2))

# print(df_y.sort_values(by=['code','parameter']))

        output = pd.DataFrame({
            'date': df_tmp['date'],
            'close': df_tmp['close'],
            'cost': ls_cost,
            # 'avg': df_tmp['avg'],
            'B': df_tmp['buy'],
            'S': df_tmp['sell'],
            # 'num B': df_tmp['numbuy'],      # B number in section
            # 'num S': df_tmp['numsell'],     # S number in section
            'R': df_tmp['rise'],
            'D': df_tmp['decline'],
            'in market': ls_mairu,
            'yue': ls_yue,
            'total': ls_zonge,
            'profit': np.array(ls_yingli)/100,
            # 'trend': ls_trend,
            'cangwei': ls_cangwei
        })

        # 5.plot
        x = pd.to_datetime(output['date'], format='%Y%m%d')
        y1 = output['close']
        y2 = output['profit']
        y3 = output['cangwei']
        y4 = output['in market']
        # y5 = (np.array(y1) - y1.tolist()[0] / y1.tolist()[0])  # 相比计算首日涨跌
        y5 = output['cost']
        # y6 = output['trend']
        expmaS = Ma(df, 20).expma()
        expmaL = Ma(df, 60).expma()

        # fig = plt.figure()                # 不同股票在不同figure显示
        fig = plt.figure(figsize=(16, 12))  # 设置画布大小

        # 买卖点
        ax7 = plt.subplot(2, 2, 1)
        ax7.plot(x, y1, color='black')
        ax7.scatter(x, y1, s=np.array(output['B'])*20, color='red', alpha=0.5, label='B', marker='^')
        ax7.scatter(x, y1, s=np.array(output['S'])*20, color='green', alpha=0.5, label='S', marker='v')
        ax7.scatter(x, y1, s=np.array(output['R'])*5, color='purple', alpha=0.5, label='R', marker='^')
        ax7.scatter(x, y1, s=np.array(output['D'])*5, color='blue', alpha=0.5, label='D', marker='v')
        ax7.set_ylabel('close')
        ax7.plot(x, expmaS, color='chocolate', label='20',alpha=0.5)
        ax7.plot(x, expmaL, color='peachpuff', label='60',alpha=0.9)
        plt.title('predicted indicator', loc='left')
        plt.xticks(fontsize=8)
        ax7.legend()
        # ax8 = ax7.twinx()
        # ax8.bar(x, output['B'], color='red', alpha=0.3)
        # ax8.bar(x, output['S'], color='green', alpha=0.3)
        # ax8.bar(x, output['R'], color='purple', alpha=0.3)
        # ax8.bar(x, output['D'], color='blue', alpha=0.3)

        # 利润 + 实际买卖点
        ax1 = plt.subplot(2, 2, 2)
        ax1.plot(x, y1, color='black')
        ax1.scatter(x, y1, s=np.array(ls_degree_buy) * 800, color='red', alpha=0.5, label='B (theory)', marker='x')
        ax1.scatter(x, y1, s=np.array(ls_degree_sell) * 800, color='green', alpha=0.5, label='S (theory)', marker='x')
        ax1.scatter(x, y1, s=np.array(ls_manipulation_buy) * 1000, color='red', alpha=0.5, label='B (fact)')
        ax1.scatter(x, y1, s=np.array(ls_manipulation_sell) * 1000, color='green', alpha=0.5, label='S (fact)')
        ax1.set_ylabel('close')
        plt.xticks(fontsize=8)
        ax2 = ax1.twinx()
        ax2.plot(x, y2, color='tomato',label='profit',linewidth=1,alpha=0.8)
        ax2.set_ylabel('profit / %')
        plt.title('trend & profit', loc='left')
        ax1.legend()
        # ax2.legend()

        # 仓位
        ax3 = plt.subplot(2, 2, 3)
        ax3.plot(x, y1, color='black')
        ax3.scatter(x, y1, s=np.array(ls_manipulation_buy) * 1000, color='red', alpha=0.5, label='B')
        ax3.scatter(x, y1, s=np.array(ls_manipulation_sell) * 1000, color='green', alpha=0.5, label='S')
        # ax3.scatter(x, y1, s=np.array(output['R'])*5, color='purple', alpha=0.5, label='R')
        # ax3.scatter(x, y1, s=np.array(output['D'])*5, color='blue', alpha=0.5, label='D')
        # ax3.plot(x,ls_cost,linestyle='--',linewidth=1,label='cost')
        ax3.axhline(y=ls_cost[0],color='darkorange',linestyle='-',linewidth=1,label='current cost')
        ax3.plot(x, y5,color='gold', linestyle='--',linewidth=1,label='cost')
        ax3.set_ylabel('close')
        ax3.legend()
        plt.xticks(fontsize=8)
        ax4 = ax3.twinx()
        ax4.plot(x, y3, color='dimgrey', label='hold')
        ax4.bar(x, y3, color='lightgrey', alpha=0.1, width=5)
        ax4.set_ylabel('hold / %')
        ax4.legend()
        plt.title('trend & stock position', loc='left')

        # 回撤 + 利润
        ax5 = plt.subplot(2, 2, 4)
        ax5.plot(x, y3, color='dimgrey')
        ax5.bar(x, y3, color='lightgrey', label='hold', alpha=0.1, width=5)
        ax5.set_ylabel('hold / %')
        ax6 = ax5.twinx()
        ax6.plot(x, np.array(ls_retracement)/100, color='skyblue', label='retracement', linewidth=1, alpha=0.8)
        ax6.legend()
        ax6.set_ylabel('retracement / %')
        plt.xticks(fontsize=8)
        ax6.plot(x, y2, color='tomato', label='profit', linewidth=1, alpha=0.8)
        # ax6.plot(x, y5, linewidth=1, alpha=0.8)
        ax6.set_ylabel('profit & retracement / %')
        ax6.legend()
        plt.title('stock position & profit', loc='left')
        plt.suptitle(code, fontsize=30)     # 主标题

        plt.savefig("D:/脚本/test/strategy_%s_%s.png" % (code, str(i)), bbox_inches='tight', dpi=300)
        print(code,'parameter'+str(i),'complete')
        plt.close()
#
#     #     # plt.show()
# print(df_y.sort_values(by=['code','parameter']))
# df_y.sort_values(by=['code','parameter']).to_csv("D:/脚本/stock strategy/411.csv",index=False)