# coding=utf-8
import os, sys
import signal

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


class LinearClose:
    def __init__(self,df,period):
        self.df = df[['trade_date', 'close', 'high', 'low']][::-1]
        self.df['trade_date'] = pd.to_datetime(self.df['trade_date'], format='%Y%m%d')
        self.period = period

    def analysis(self,a):
        self.df['highest_in_period'] = self.df.high.rolling(self.period, min_periods=1).max()  # 周期内最高high
        self.df['lowest_in_period'] = self.df.low.rolling(self.period, min_periods=1).min()  # 周期内最低low
        i = 1
        ls_trend = [0]
        ls_section = []
        ls_k = []
        ls_close = []
        df_tmp = pd.DataFrame(columns=['close','section'])
        # df_tmp = pd.DataFrame({'close': None, 'section': None})
        model = LinearRegression()

        for row in self.df.itertuples():
            close = getattr(row, 'close')
            high = getattr(row, 'high')
            low = getattr(row, 'low')
            highest_in_period = getattr(row, 'highest_in_period')
            lowest_in_period = getattr(row, 'lowest_in_period')
            ls_close.append(close)
            # 'rise':1, 'decline':-1
            if low == lowest_in_period:
                ls_trend.append(-1)
                ls_section.append(i)
            elif high == highest_in_period:
                ls_trend.append(1)
                ls_section.append(i)
            else:
                ls_trend.append(ls_trend[-1])
                ls_section.append(i)
            # eliminate signal trend, adjust the trend of yesterday
            if len(ls_trend) >= self.period:
                if ls_trend[-1] == ls_trend[-3] != ls_trend[-2]:
                    ls_trend[-2] = ls_trend[-1]
                    i -= 1
                    ls_section[-1] = ls_section[-1] - 1
                    # ls_section[-2] = ls_section[-2] - 1
            # section
            if len(ls_trend) >= self.period:
                if ls_trend[-1] != ls_trend[-2]:
                    ls_section[-1] = ls_section[-1] + 1
                    i += 1
            # # 1
            # df_tmp['close'] = ls_close
            # df_tmp['section'] = ls_section
            # df_tmp = df_tmp.append(pd.Series({'close': close, 'section': ls_section[-1]}), ignore_index=True)
            df_tmp = pd.concat([df_tmp,pd.DataFrame({'close':[close],'section':ls_section[-1]})],axis=0,ignore_index=True)
            # real time k
            # # print(df_tmp)
            if len(ls_section) > 1:
                if ls_section[-2] == ls_section[-1]:
                    x = np.arange(0,ls_section.count(ls_section[-1]),1).reshape(-1, 1)
                    y = df_tmp[df_tmp['section'] == ls_section[-1]]['close'].values.reshape(-1, 1)
                    model.fit(x, y)
                    ls_k.append(np.ravel(model.coef_)[0])
                else:
                    ls_k.append(0)
            else:
                ls_k.append(0)
        df_tmp['k'] = ls_k
        df_tmp['data'] = self.df['trade_date'].tolist()
        df_tmp['high'] = self.df['high'].tolist()
        df_tmp['low'] = self.df['low'].tolist()
        # return df_tmp[::-1]
        # 2
        del ls_trend[0]
        self.df['trend'] = ls_trend
        self.df['section'] = ls_section
        model = LinearRegression()
        tmp = {}
        begin = [0]
        # dict_k = {}
        # i = 1
        # fig, ax = plt.subplots(figsize=(10, 6))
        # ax.plot(np.arange(0, len(self.df['trade_date']), 1), self.df['close'])
        for i in self.df['section'].unique():
            y = self.df[self.df['section'] == i]['close'].values.reshape(-1, 1)
            x = np.arange(sum(begin), sum(begin) + len(y), 1).reshape(-1, 1)
            model.fit(x, y)
            tmp[i] = pd.DataFrame({
                # 'trade_date': self.df[self.df['section'] == i]['trade_date'],
                # 'close': self.df[self.df['section'] == i]['close'],
                # 'x': np.ravel(x),
                'predict': np.ravel(model.predict(x).tolist()),
                'coefficient': np.ravel(list(model.coef_)*len(y)),
                'intercept': np.ravel(list(model.intercept_)*len(y))})
            # dict_k[i] = model.coef_
            # ax.plot(x, np.ravel(model.predict(x)), '--', color='r')
            begin.append(len(y))
            i += 1
        # concat the dataset
        re = pd.concat(list(tmp.values()), ignore_index=True)
        # re['section'] = ls_section
        re = pd.concat([re,df_tmp],axis=1,join='outer')
        # # 3
        re['max_k'] = re.k.rolling(a,min_periods=1).max()
        re['min_k'] = re.k.rolling(a,min_periods=1).min()
        re['max_high'] = re.high.rolling(a,min_periods=1).max()
        re['max_low'] = re.low.rolling(a,min_periods=1).min()
        ls_signal = []
        # ls_max_k_in_period = []
        # ls_min_k_in_period = []
        # ls_max_k_in_period_close = []
        # ls_min_k_in_period_close = []
        for row in re.itertuples():
            max_k_in_period = getattr(row,'max_k')
            min_k_in_period = getattr(row,'min_k')
            max_high_in_period = getattr(row,'max_high')
            max_low_in_period = getattr(row,'max_low')
            high = getattr(row,'high')
            low = getattr(row,'low')
            k = getattr(row,'k')
            if k == max_k_in_period and high < max_high_in_period:
                ls_signal.append('sell')
            elif k < max_k_in_period and high == max_high_in_period:
                ls_signal.append('sell')
            elif k == max_k_in_period and high == max_high_in_period:
                ls_signal.append('↑')
            elif k == min_k_in_period and low > max_low_in_period:
                ls_signal.append('buy')
            elif k > min_k_in_period and low == max_low_in_period:
                ls_signal.append('buy')
            elif k == min_k_in_period and low == max_low_in_period:
                ls_signal.append('↓')
            else:
                ls_signal.append(0)
            # if k == max_k_in_period:
            #     ls_max_k_in_period.append(k)
            #     ls_max_k_in_period_close.append(close)
            # elif k == min_k_in_period:
            #     ls_min_k_in_period.append(k)
            #     ls_min_k_in_period_close.append(close)
            #
            # if k == max_k_in_period and len(ls_max_k_in_period) >= 2:
            #     if max_k_in_period < ls_max_k_in_period[-2] and close > ls_max_k_in_period_close[-2]:
            #         ls_signal.append('sell')
            #     else:
            #         ls_signal.append(0)
            # elif k == min_k_in_period and len(ls_min_k_in_period) >= 2:
            #     if min_k_in_period < ls_min_k_in_period[-2] and close > ls_min_k_in_period_close[-2]:
            #         ls_signal.append('buy')
            #     else:
            #         ls_signal.append(0)
            # else:
            #     ls_signal.append(0)
        re['signal'] = ls_signal
        return re[::-1]

    def plot(self,plt_row,plt_col,plt_position):
        self.df['highest_in_period'] = self.df.high.rolling(self.period, min_periods=1).max()  # 周期内最高high
        self.df['lowest_in_period'] = self.df.low.rolling(self.period, min_periods=1).min()  # 周期内最低low
        i = 1
        ls_trend = [0]
        ls_section = []
        for row in self.df.itertuples():
            close = getattr(row, 'close')
            high = getattr(row, 'high')
            low = getattr(row, 'low')
            highest_in_period = getattr(row, 'highest_in_period')
            lowest_in_period = getattr(row, 'lowest_in_period')
            # 'rise':1, 'decline':-1
            if low == lowest_in_period:
                ls_trend.append(-1)
                ls_section.append(i)
            elif high == highest_in_period:
                ls_trend.append(1)
                ls_section.append(i)
            else:
                ls_trend.append(ls_trend[-1])
                ls_section.append(i)
            # eliminate signal trend, adjust the trend of yesterday
            if len(ls_trend) >= self.period:
                if ls_trend[-1] == ls_trend[-3] != ls_trend[-2]:
                    ls_trend[-2] = ls_trend[-1]
                    i -= 1
                    ls_section[-1] = ls_section[-1] - 1
                    ls_section[-2] = ls_section[-2] - 1
            # section
            if len(ls_trend) >= self.period:
                if ls_trend[-1] != ls_trend[-2]:
                    ls_section[-1] = ls_section[-1] + 1
                    i += 1
        del ls_trend[0]
        self.df['trend'] = ls_trend
        self.df['section'] = ls_section
        model = LinearRegression()
        begin = [0]
        # fig, ax = plt.subplots(figsize=(10, 6))
        ax = plt.subplot(plt_row,plt_col,plt_position)
        for i in self.df['section'].unique():
            y = self.df[self.df['section'] == i]['close'].values.reshape(-1, 1)
            x = np.arange(sum(begin), sum(begin) + len(y), 1).reshape(-1, 1)
            model.fit(x, y)
            if np.ravel(model.coef_)[0] > 0:
                color = 'red'
            else:
                color = 'green'
            ax.plot(x, np.ravel(model.predict(x)), '--', linewidth=1.25,color=color, label=round(np.ravel(model.coef_)[0],3))
            # ax.axhline(xmin=x[0],xmax=x[-1],y=highest_in_period, linestyle='--', linewidth=.75, color='grey')
            # ax.axhline(xmin=x[0],xmax=x[-1],y=lowest_in_period, linestyle='--', linewidth=.75, color='grey')
            begin.append(len(y))
            i += 1
        ax.plot(np.arange(0, len(self.df['trade_date']), 1), self.df['close'],color='black',alpha=0.25)
        plt.xticks(np.arange(0, len(self.df['trade_date']), 1), labels=self.df['trade_date'].dt.date.tolist())
        plt.xticks(rotation=0)
        ax.xaxis.set_major_locator(plt.MultipleLocator(30))



# code = '000677.SZ'
# test_df = pd.read_csv("D:/脚本/stock diary/diary_%s.csv" % code)
# print(LinearClose(test_df[:300],20).analysis()[1])
# LinearClose(test_df[:300],20).plot(1,1,1)
# plt.show()

# code_list = ["000782.SZ","000677.SZ","601857.SH","000886.SZ"]
# position = 1
# for code in code_list:
#     df = pd.read_csv("D:/脚本/stock diary/diary_%s.csv" % code)[:300]
#     # # 1
#     LinearClose(df, 20).plot(2, 2, position)
#     plt.title(code)
#     position += 1
#     # # 2
#     # ax = plt.subplot(2, 2, position)
#     # plt.plot(np.arange(0, len(df['trade_date']), 1), df['close'][::-1])
#     # plt.xticks(np.arange(0, len(df['trade_date']), 1), labels=df['trade_date'][::-1].tolist())
#     # ax.xaxis.set_major_locator(plt.MultipleLocator(30))
#     # plt.xticks(rotation=30)
#     # a = LinearClose(df, 20).analysis()
#     # for i in np.arange(1,len(a)+1,1):
#     #     plt.plot(a[i]['x'], a[i]['predict'], '--', color='r')
#     #     # plt.plot(a[i]['x'], a[i]['close'], color='black')
#     #     plt.title(code)
#     # position += 1
# plt.suptitle('Linear Regression Close')
# plt.show()

# # # raw code
# 用pandas读取csv
# code = '000677.SZ'
# df = pd.read_csv("D:/脚本/stock diary/diary_%s.csv" % code)[['trade_date','close','high','low']][:300][::-1]
# df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')

# # # 分段
# # high 大于周期内 max high，r
# # low  小于周期内 min low， d
# period = 10
# df['highest_in_period'] = df.high.rolling(period, min_periods=1).max()  # 周期内最高high
# df['lowest_in_period'] = df.low.rolling(period, min_periods=1).min()   # 周期内最低low
# i = 1
# ls_trend = [0]
# ls_section = []
# for row in df.itertuples():
#     close = getattr(row, 'close')
#     high = getattr(row, 'high')
#     low = getattr(row, 'low')
#     highest_in_period = getattr(row, 'highest_in_period')
#     lowest_in_period = getattr(row, 'lowest_in_period')
#     # 'rise':1, 'decline':-1
#     if low == lowest_in_period:
#         ls_trend.append(-1)
#         ls_section.append(i)
#     elif high == highest_in_period:
#         ls_trend.append(1)
#         ls_section.append(i)
#     else:
#         ls_trend.append(ls_trend[-1])
#         ls_section.append(i)
#     # eliminate signal trend, adjust the trend of yesterday
#     if len(ls_trend) >= period:
#         if ls_trend[-1] == ls_trend[-3] != ls_trend[-2]:
#             ls_trend[-2] = ls_trend[-1]
#             i -= 1
#             ls_section[-1] = ls_section[-1] - 1
#             ls_section[-2] = ls_section[-2] - 1
#     # section
#     if len(ls_trend) >= period:
#         if ls_trend[-1] != ls_trend[-2]:
#             ls_section[-1] = ls_section[-1] + 1
#             i += 1
# del ls_trend[0]
# # ls_trend.reverse()
# # ls_section.reverse()
# df['trend'] = ls_trend
# df['section'] = ls_section
# # print(df[:60])
# # print(df['trend'].tolist())
# # print(df['section'].tolist())
# # print([df['trend'] == -1])
# # print(df['section'].unique())
# # # output
# model = LinearRegression()
# # tmp = {}
# begin = [0]
# dict_k = {}
# i = 1
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(np.arange(0,len(df['trade_date']),1),df['close'])
# for i in df['section'].unique():
#     # tmp[i] = df[df['section'] == i][['trade_date','close']]
#     y = df[df['section'] == i]['close'].values.reshape(-1, 1)
#     x = np.arange(sum(begin), sum(begin)+len(y), 1).reshape(-1, 1)
#     model.fit(x,y)
#     # tmp[i] = pd.DataFrame({'trade_date': df[df['section'] == i]['trade_date'],
#     #                        'predict': np.ravel(model.predict(x).tolist())})
#     dict_k[i] = model.coef_
#     ax.plot(x,np.ravel(model.predict(x)),'--',color='r')
#     begin.append(len(y))
#     i += 1
# # ax.axes.xaxis.set_ticklabels([])
# plt.xticks(np.arange(0,len(df['trade_date']),1),labels=df['trade_date'].dt.date.tolist())
# ax.xaxis.set_major_locator(plt.MultipleLocator(30))
# plt.xticks(rotation=30)
# plt.show()
# # print(dict_k)
# # print(tmp)
# # print(pd.DataFrame(tmp[5]))
