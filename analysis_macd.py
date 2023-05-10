import pandas as pd
import numpy as np

class Macd:
    def __init__(self, df):
        self.closes = df['close'].tolist()
        self.date = df['trade_date'].tolist()
        self.high = df['high'].tolist()
        self.low = df['low'].tolist()

    def merge_macd(self):
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]
        dif_list = [0]
        dea_list = [0]
        while (abs(i) < len(self.closes)):
            i = i - 1
            short_ema = float(short_alpha * self.closes[i] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i] + (1 - long_alpha) * long_ema)
            dif_list.append(short_ema - long_ema)
        alpha = 1 / 5
        i = 1
        dea = dif_list[0]
        while (i < len(self.closes)):
            dea = float(alpha * dif_list[i] + (1 - alpha) * dea)
            i = i + 1
            dea_list.insert(0,dea)# insert(index,obj) 在列表index的位置插入obj
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]  # 开盘首日
        dif_list = [0]
        while (abs(i) < len(self.closes)):
            short_ema = float(short_alpha * self.closes[i - 1] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i - 1] + (1 - long_alpha) * long_ema)
            i = i - 1
            dif = short_ema - long_ema
            dif_list.insert(0, dif)
        dif_array = np.array(dif_list)
        dea_array = np.array(dea_list)
        macd_array = 2*(dif_array-dea_array)
        macd_array = macd_array.tolist()
        # macd_list = [round(x, 2) for x in macd_array]
        macd_list = macd_array
        merge = []
        zhenglist = []
        fulist = []
        for a in macd_list[::-1]:
            if a <= 0:
                if zhenglist is not None:
                    merge.append(sum(zhenglist))
                    zhenglist = []
                    fulist.append(a)
                else:
                    fulist.append(a)
            elif a > 0:
                if fulist is not None:
                    merge.append(sum(fulist))
                    fulist = []
                    zhenglist.append(a)
                else:
                    zhenglist.append(a)
        merge.reverse()
        merge.insert(0,macd_list[0])
        merge.pop(-1)
        return merge

    def summary(self):
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]
        dif_list = [0]
        dea_list = [0]
        while (abs(i) < len(self.closes)):
            i = i - 1
            short_ema = float(short_alpha * self.closes[i] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i] + (1 - long_alpha) * long_ema)
            dif_list.append(short_ema - long_ema)
        alpha = 1 / 5
        i = 1
        dea = dif_list[0]
        while (i < len(self.closes)):
            dea = float(alpha * dif_list[i] + (1 - alpha) * dea)
            i = i + 1
            dea_list.insert(0,dea)# insert(index,obj) 在列表index的位置插入obj
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]  # 开盘首日
        dif_list = [0]
        while (abs(i) < len(self.closes)):
            short_ema = float(short_alpha * self.closes[i - 1] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i - 1] + (1 - long_alpha) * long_ema)
            i = i - 1
            dif = short_ema - long_ema
            dif_list.insert(0, dif)
        dif_array = np.array(dif_list)
        dea_array = np.array(dea_list)
        macd_array = 2*(dif_array-dea_array)
        macd_array = macd_array.tolist()
        macd_list = macd_array
        merge = []
        zhenglist = []
        fulist = []
        for a in macd_list[::-1]:
            if a <= 0:
                if zhenglist is not None:
                    merge.append(sum(zhenglist))
                    zhenglist = []
                    fulist.append(a)
                else:
                    fulist.append(a)
            elif a > 0:
                if fulist is not None:
                    merge.append(sum(fulist))
                    fulist = []
                    zhenglist.append(a)
                else:
                    zhenglist.append(a)
        merge.reverse()
        merge.insert(0,macd_list[0])
        merge.pop(-1)
        summary = pd.DataFrame({
            "date": self.date,
            "dif": dif_list,
            "dea": dea_list,
            "macd": macd_array,
            "merge": merge
        })
        return summary

    # def analysis(self):
    #     short_alpha = 2 / 13
    #     long_alpha = 2 / 27
    #     i = -1
    #     short_ema = self.closes[-1]
    #     long_ema = self.closes[-1]
    #     dif_list = [0]
    #     dea_list = [0]
    #     while (abs(i) < len(self.closes)):
    #         i = i - 1
    #         short_ema = float(short_alpha * self.closes[i] + (1 - short_alpha) * short_ema)
    #         long_ema = float(long_alpha * self.closes[i] + (1 - long_alpha) * long_ema)
    #         dif_list.append(short_ema - long_ema)
    #     alpha = 1 / 5
    #     i = 1
    #     dea = dif_list[0]
    #     while (i < len(self.closes)):
    #         dea = float(alpha * dif_list[i] + (1 - alpha) * dea)
    #         i = i + 1
    #         dea_list.insert(0,dea)# insert(index,obj) 在列表index的位置插入obj
    #     short_alpha = 2 / 13
    #     long_alpha = 2 / 27
    #     i = -1
    #     short_ema = self.closes[-1]
    #     long_ema = self.closes[-1]  # 开盘首日
    #     dif_list = [0]
    #     while (abs(i) < len(self.closes)):
    #         short_ema = float(short_alpha * self.closes[i - 1] + (1 - short_alpha) * short_ema)
    #         long_ema = float(long_alpha * self.closes[i - 1] + (1 - long_alpha) * long_ema)
    #         i = i - 1
    #         dif = short_ema - long_ema
    #         dif_list.insert(0, dif)
    #     dif_array = np.array(dif_list)
    #     dea_array = np.array(dea_list)
    #     macd_array = 2*(dif_array-dea_array)
    #     macd_array = macd_array.tolist()
    #     macd_list = macd_array
    #     merge = []
    #     zhenglist = []
    #     fulist = []
    #     for a in macd_list[::-1]:
    #         if a <= 0:
    #             if zhenglist is not None:
    #                 merge.append(sum(zhenglist))
    #                 zhenglist = []
    #                 fulist.append(a)
    #             else:
    #                 fulist.append(a)
    #         elif a > 0:
    #             if fulist is not None:
    #                 merge.append(sum(fulist))
    #                 fulist = []
    #                 zhenglist.append(a)
    #             else:
    #                 zhenglist.append(a)
    #     merge.reverse()
    #     merge.insert(0,macd_list[0])
    #     merge.pop(-1)
    #
    #     tmplist = []
    #     maxlist = []
    #     minlist = []
    #     #high
    #     for a, b in zip(merge[::-1], self.high[::-1]):
    #         if a == 0:
    #             tmplist.append(b)
    #         elif a != 0:
    #             tmplist.append(b)
    #             maxlist.append(max(tmplist))
    #             tmplist = []
    #     #low
    #     for a, b in zip(merge[::-1], self.low[::-1]):
    #         if a == 0:
    #             tmplist.append(b)
    #         elif a != 0:
    #             tmplist.append(b)
    #             minlist.append(min(tmplist))
    #             tmplist = []
    #
    #
    #     df2 = pd.DataFrame({'date': self.date, 'macd.merge': merge})
    #     df2 = df2.drop(index=(df2.loc[(df2['macd.merge'] == 0)].index))
    #     df2['high'] = maxlist[::-1]
    #     df2['low'] = minlist[::-1]
    #     #我们只需要在截取数据的语句后加一个.copy()复制一份数据为df就可以了。
    #     selldf = df2[df2['macd.merge'] > 0].copy()
    #     buydf = df2[df2['macd.merge'] < 0].copy()
    #     sell_signal = []
    #     mer_b = 0
    #     max_b = 0
    #     for index, row in selldf.iloc[::-1].iterrows():
    #         mer_a = row[1]
    #         max_a = row[2]
    #         if mer_a > mer_b and max_a < max_b:
    #             sell_signal.append('sell')
    #         elif mer_a < mer_b and max_a > max_b:
    #             sell_signal.append('sell')
    #         else:
    #             sell_signal.append('0')
    #         mer_b = mer_a
    #         max_b = max_a
    #     buy_signal = []
    #     mer_b = 0
    #     min_b = 0
    #     for index, row in buydf.iloc[::-1].iterrows():
    #         mer_a = row[1]
    #         min_a = row[3]
    #         if mer_a > mer_b and min_a < min_b:
    #             buy_signal.append('buy')
    #         elif mer_a < mer_b and min_a > min_b:
    #             buy_signal.append('buy')
    #         else:
    #             buy_signal.append('0')
    #         mer_b = mer_a
    #         min_b = min_a
    #     selldf["macd.signal"] = sell_signal[::-1]
    #     buydf["macd.signal"] = buy_signal[::-1]
    #     df3 = pd.concat(objs=[selldf, buydf], axis=0, ignore_index=False)
    #     date = pd.DataFrame({
    #         'date': self.date,
    #     })
    #     df3 = pd.merge(df3.sort_index(), date, how='right', on='date')
    #     return df3[['date','macd.merge','macd.signal']].fillna(0)

    # def analysis(self):
    #     short_alpha = 2 / 13
    #     long_alpha = 2 / 27
    #     i = -1
    #     short_ema = self.closes[-1]
    #     long_ema = self.closes[-1]
    #     dif_list = [0]
    #     dea_list = [0]
    #     while (abs(i) < len(self.closes)):
    #         i = i - 1
    #         short_ema = float(short_alpha * self.closes[i] + (1 - short_alpha) * short_ema)
    #         long_ema = float(long_alpha * self.closes[i] + (1 - long_alpha) * long_ema)
    #         dif_list.append(short_ema - long_ema)
    #     alpha = 1 / 5
    #     i = 1
    #     dea = dif_list[0]
    #     while (i < len(self.closes)):
    #         dea = float(alpha * dif_list[i] + (1 - alpha) * dea)
    #         i = i + 1
    #         dea_list.insert(0,dea)# insert(index,obj) 在列表index的位置插入obj
    #     short_alpha = 2 / 13
    #     long_alpha = 2 / 27
    #     i = -1
    #     short_ema = self.closes[-1]
    #     long_ema = self.closes[-1]  # 开盘首日
    #     dif_list = [0]
    #     while (abs(i) < len(self.closes)):
    #         short_ema = float(short_alpha * self.closes[i - 1] + (1 - short_alpha) * short_ema)
    #         long_ema = float(long_alpha * self.closes[i - 1] + (1 - long_alpha) * long_ema)
    #         i = i - 1
    #         dif = short_ema - long_ema
    #         dif_list.insert(0, dif)
    #     dif_array = np.array(dif_list)  # dif
    #     dea_array = np.array(dea_list)  # dea
    #     macd_array = (2*(dif_array-dea_array)).tolist()  # macd
    #     macd_array.reverse()
    #
    #     # macd trend
    #     i = 0
    #     macd_tmp = []
    #     macd_sum = []
    #     peak = []
    #     while(i<=len(macd_array)-1):
    #         if i == 0:
    #             a = 0
    #             b = macd_array[i]
    #             c = macd_array[i + 1]
    #         elif i == len(macd_array)-1:
    #             a = macd_array[i - 1]
    #             b = macd_array[i]
    #             c = 0
    #         else:
    #             a = macd_array[i-1]
    #             b = macd_array[i]
    #             c = macd_array[i+1]
    #
    #         if macd_array[i] > 0:               # -++   +++   +peak+   +++   ++-  +++
    #             if a <= 0 and b <= c:     # 负转正
    #                 macd_tmp.append(b)
    #                 peak.append("-→+")
    #                 macd_sum.append(0)
    #             elif a <= b and b <= c:       # 上升
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(0)
    #             elif a <= b and b > c and c > 0:    # 顶点
    #                 macd_tmp.append(b)
    #                 peak.append("peak")
    #                 macd_sum.append(0)
    #             elif a <= b and b > c and c <= 0:   # 顶点跳水
    #                 macd_tmp.append(b)
    #                 peak.append("peak")
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #             elif a > b and b > c and c > 0:     # 下降
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(0)
    #             elif a > b and b <= c and c > 0:    # 第二轮
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #             elif a > b and c <= 0:    # 正转负
    #                 macd_tmp.append(b)
    #                 peak.append("+→-")
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #         elif macd_array[i] <= 0:
    #             if a > 0 and b > c:
    #                 macd_tmp.append(b)
    #                 peak.append("+→-")
    #                 macd_sum.append(0)
    #             elif a > b and b > c:
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(0)
    #             elif a > b and b <= c and c < 0:
    #                 macd_tmp.append(b)
    #                 peak.append("peak-")
    #                 macd_sum.append(0)
    #             elif a > b and b <= c and c >= 0:
    #                 macd_tmp.append(b)
    #                 peak.append("peak-")
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #             elif a <= b and b <= c and c < 0:
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(0)
    #             elif a <= b and b > c and c < 0:
    #                 macd_tmp.append(b)
    #                 peak.append(0)
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #             elif a <= b and c > 0:
    #                 macd_tmp.append(b)
    #                 peak.append("-→+")
    #                 macd_sum.append(sum(macd_tmp))
    #                 macd_tmp = []
    #         i = i+1
    #     peak.reverse()
    #     macd_sum.reverse()
    #     macd_array.reverse()
    #
    #     # extract section highest and lowest
    #     low = self.low[::-1]
    #     high = self.high[::-1]
    #     low_ls = []
    #     high_ls = []
    #     lowest_ls = []
    #     highest_ls = []
    #     i = 0
    #     for a in macd_sum[::-1]:
    #         if a == 0:
    #             low_ls.append(low[i])
    #             high_ls.append(high[i])
    #             lowest_ls.append(0)
    #             highest_ls.append(0)
    #             i = i + 1
    #         elif a != 0:
    #             low_ls.append(low[i])
    #             high_ls.append(high[i])
    #             lowest_ls.append(min(low_ls))
    #             highest_ls.append(max(high_ls))
    #             low_ls = []
    #             high_ls = []
    #             i = i + 1
    #
    #     # signal
    #     lowest_ls.reverse()
    #     highest_ls.reverse()
    #     df_tmp = pd.DataFrame({
    #         'macd.sum': macd_sum,
    #         'macd': macd_array,
    #         'highest': highest_ls,
    #         'lowest': lowest_ls
    #     })
    #     signal = []
    #     zheng_sum = 0
    #     zheng_high = 0
    #     fu_sum = 0
    #     fu_low = 0
    #     for index,row in df_tmp[::-1].iterrows():
    #         a = row['macd.sum']
    #         new_high = row['highest']
    #         new_low = row['lowest']
    #         if a == 0:
    #             signal.append(0)
    #         elif a >0 and zheng_sum==0:
    #             signal.append('hold')
    #             zheng_sum = a       # 上一轮的sum macd
    #             zheng_high = new_high       # 上一轮的最高价
    #         elif a<0 and fu_sum==0:
    #             signal.append('hold')
    #             fu_sum = a
    #             fu_low = new_low
    #         # macd > 0
    #         elif zheng_sum>a>0:     # macd小于上一轮
    #             if new_high>zheng_high:
    #                 signal.append('sell')
    #             elif new_high<=zheng_high:
    #                 signal.append('hold')
    #             zheng_sum = a
    #             zheng_high = new_high
    #             zheng_low = new_low
    #         elif a>zheng_sum>0:     # macd大于上一轮
    #             if new_high>zheng_high:
    #                 signal.append('hold')
    #             if new_high<=zheng_high:
    #                 signal.append('sell')
    #             zheng_sum = a
    #             zheng_high = new_high
    #             zheng_low = new_low
    #         # macd<0
    #         elif 0>a>fu_sum and new_low<=fu_low:    # macd 绿区收缩
    #             signal.append('buy')
    #             fu_low = new_low
    #             fu_sum = a
    #         elif 0>a>fu_sum and new_low>fu_low:     # macd 绿区收缩
    #             signal.append('buy')
    #             fu_low = new_low
    #             fu_sum = a
    #         elif 0>fu_sum>a and new_low>fu_low:
    #             signal.append('buy')
    #             fu_low = new_low
    #             fu_sum = a
    #         elif 0>fu_sum>a and new_low<=fu_low:
    #             signal.append('hold')
    #             fu_low = new_low
    #             fu_sum = a
    #     signal.reverse()
    #
    #
    #     # 按行历遍peak，“peak”in 则添加macd.sum
    #     sum_tmp = []
    #     for a in macd_sum:
    #         if a != 0:
    #             sum_tmp.append(a)
    #
    #     highest_tmp = []
    #     for a in highest_ls:
    #         if a != 0:
    #             highest_tmp.append(a)
    #
    #     lowest_tmp = []
    #     for a in lowest_ls:
    #         if a != 0:
    #             lowest_tmp.append(a)
    #
    #     signal_tmp = []
    #     for a in signal:
    #         if a != 0:
    #             signal_tmp.append(a)
    #
    #     peak_tmp = []
    #     for a in peak:
    #         if 'peak' in str(a):
    #             peak_tmp.append(a)
    #
    #     macd_sum1 = []  # macd_sum1 对准peak
    #     highest_ls1 = []
    #     lowest_ls1 = []
    #     signal1 = []
    #     i = 0
    #     for a in peak:
    #         if 'peak' in str(a):
    #             macd_sum1.append(sum_tmp[i])
    #             highest_ls1.append(highest_tmp[i])
    #             lowest_ls1.append(lowest_tmp[i])
    #             signal1.append(signal_tmp[i])
    #             i = i + 1
    #         else:
    #             macd_sum1.append(0)
    #             highest_ls1.append(0)
    #             lowest_ls1.append(0)
    #             signal1.append(0)
    #
    #     re = pd.DataFrame({
    #         'date': self.date,
    #         'close':self.closes,
    #         'high': self.high,
    #         'low': self.low,
    #         'macd': macd_array,
    #         'macd.trend': peak,
    #         'macd.sum': macd_sum1,
    #         'highest': highest_ls1,
    #         'lowest': lowest_ls1,
    #         'signal': signal1
    #     })
    #
    #     return re

    def analysis(self):
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]
        dif_list = [0]
        dea_list = [0]
        while (abs(i) < len(self.closes)):
            i = i - 1
            short_ema = float(short_alpha * self.closes[i] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i] + (1 - long_alpha) * long_ema)
            dif_list.append(short_ema - long_ema)
        alpha = 1 / 5
        i = 1
        dea = dif_list[0]
        while (i < len(self.closes)):
            dea = float(alpha * dif_list[i] + (1 - alpha) * dea)
            i = i + 1
            dea_list.insert(0,dea)  # insert(index,obj) 在列表index的位置插入obj
        short_alpha = 2 / 13
        long_alpha = 2 / 27
        i = -1
        short_ema = self.closes[-1]
        long_ema = self.closes[-1]  # 开盘首日
        dif_list = [0]
        while (abs(i) < len(self.closes)):
            short_ema = float(short_alpha * self.closes[i - 1] + (1 - short_alpha) * short_ema)
            long_ema = float(long_alpha * self.closes[i - 1] + (1 - long_alpha) * long_ema)
            i = i - 1
            dif = short_ema - long_ema
            dif_list.insert(0, dif)
        dif_array = np.array(dif_list)  # dif
        dea_array = np.array(dea_list)  # dea
        macd_array = (2*(dif_array-dea_array)).tolist()  # macd

        # macd trend  明日不可预测的前提
        macd_array.reverse()
        i = 0
        macd_tmp = []
        macd_sum = []
        trend = []
        signal = []
        while(i<=len(macd_array)-1):
            if i == 0:                      # first day
                a = 0                       # yesterday
                b = macd_array[i]           # today
            # elif i == len(macd_array)-1:    # last day
            #     a = macd_array[i - 1]
            #     b = macd_array[i]
            else:
                a = macd_array[i-1]
                b = macd_array[i]

            if b > 0:
                if a <= 0:                          # 负转正
                    trend.append("-→+")
                    macd_sum.append(sum(macd_tmp))
                    macd_tmp = []
                    macd_tmp.append(b)
                elif b > a and '↓' in trend[-1]:    # 再上升
                    trend.append("+→+")
                    macd_tmp.append(b)
                    macd_sum.append(0)
                elif b > a:                         # 上升
                    trend.append(" ↑ ")
                    macd_tmp.append(b)
                    macd_sum.append(0)
                elif a > b:                         # 下降
                    trend.append(" ↓ ")
                    macd_sum.append(0)
                    macd_tmp.append(b)
                elif a == b:
                    trend.append(" = ")
                    macd_sum.append(0)
                    macd_tmp.append(b)
            elif b <= 0:
                if a > 0:                           # 正转负
                    trend.append("+→-")
                    macd_sum.append(sum(macd_tmp))
                    macd_tmp = []
                    macd_tmp.append(b)
                elif b > a:                         # 上升
                    trend.append(" ↑ ")
                    macd_tmp.append(b)
                    macd_sum.append(0)
                elif b < a and '↑' in trend[-1]:    # 再下降
                    trend.append("-→-")
                    macd_sum.append(0)
                    macd_tmp.append(b)
                elif b < a:                         # 下降
                    trend.append(" ↓ ")
                    macd_sum.append(0)
                    macd_tmp.append(b)
                elif a == b:
                    trend.append(" = ")
                    macd_sum.append(0)
                    macd_tmp.append(b)
            i = i+1
        trend.reverse()
        macd_sum.reverse()  # 按大于零小于零区分的macd
        macd_array.reverse()

        df = pd.DataFrame({
            'date': self.date,
            'close': self.closes,
            'high': self.high,
            'low': self.low,
            'macd': macd_array,
            'trend': trend
        })



        high_list = []
        low_list = []
        zheng_list = []
        fu_list =[]
        signal = []
        zheng = 0   # 保存上一轮macd的和
        fu = 0      # 保存上一轮macd的和

        for index,row in df[::-1].iterrows():
            macd = row['macd']
            high = row['high']
            low = row['low']
            trend = row['trend']
            if macd > 0:
                if zheng == 0:  # first round
                    if '+→-' in trend or '+→+' in trend:
                        zheng = zheng_tmp_sum
                        last_highest = highest
                        zheng_list = []
                        high_list = []
                        zheng_list.append(macd)
                        high_list.append(high)
                        zheng_tmp_sum = sum(zheng_list)  # 当前区间的macd
                        highest = max(high_list)  # 当前区间的最低价
                        signal.append(0)
                    else:
                        zheng_list.append(macd)
                        high_list.append(high)
                        zheng_tmp_sum = sum(zheng_list)  # 当前区间的macd
                        highest = max(high_list)
                        signal.append(0)
                elif '+→+' in trend:      # 轮次结束
                    zheng = zheng_tmp_sum
                    last_highest = highest
                    zheng_list = []
                    high_list = []
                    zheng_list.append(macd)
                    high_list.append(high)
                    zheng_tmp_sum = sum(zheng_list)  # 当前区间的macd
                    highest = max(high_list)  # 当前区间的最高价
                    if zheng_tmp_sum <= zheng and highest > last_highest:       # macd面积小于上一轮 最高价高于上轮
                        signal.append('(+→+)sell')
                    elif zheng_tmp_sum <= zheng and highest <= last_highest:    # macd面积小于上一轮 最高价小于上轮
                        signal.append('(+→+)0')
                    elif zheng_tmp_sum > zheng and highest > last_highest:      # macd面积大于上一轮 最高价高于上轮
                        signal.append('(+→+)0')
                    elif zheng_tmp_sum > zheng and highest <= last_highest:     # macd面积大于上一轮 最高价小于上轮
                        signal.append('(+→+)sell')
                elif '-→+' in trend:
                    zheng = zheng_tmp_sum
                    last_highest = highest
                    zheng_list = []
                    high_list = []
                    fu_list = []
                    low_list = []
                    zheng_list.append(macd)
                    high_list.append(high)
                    zheng_tmp_sum = sum(zheng_list)  # 当前区间的macd
                    highest = max(high_list)  # 当前区间的最高价
                    if zheng_tmp_sum <= zheng and highest > last_highest:       # macd面积小于上一轮 最高价高于上轮
                        signal.append('(-→+)sell')
                    elif zheng_tmp_sum <= zheng and highest <= last_highest:    # macd面积小于上一轮 最高价小于上轮
                        signal.append('(-→+)0')
                    elif zheng_tmp_sum > zheng and highest > last_highest:      # macd面积大于上一轮 最高价高于上轮
                        signal.append('(-→+)0')
                    elif zheng_tmp_sum > zheng and highest <= last_highest:     # macd面积大于上一轮 最高价小于上轮
                        signal.append('(-→+)sell')
                else:
                    zheng_list.append(macd)
                    high_list.append(high)
                    zheng_tmp_sum = sum(zheng_list)  # 当前区间的macd
                    highest = max(high_list)
                    if zheng_tmp_sum <= zheng and high > last_highest:       # macd面积小于上一轮 最高价高于上轮
                        signal.append('sell')
                    elif zheng_tmp_sum <= zheng and high <= last_highest:    # macd面积小于上一轮 最高价小于上轮
                        signal.append(0)
                    elif zheng_tmp_sum > zheng and high > last_highest:      # macd面积大于上一轮 最高价高于上轮
                        signal.append(0)
                        # if '↓' in trend:
                        #     signal.append('T-sell')
                        # else:
                        #     signal.append(0)
                    elif zheng_tmp_sum > zheng and high <= last_highest:     # macd面积大于上一轮 最高价小于上轮
                        signal.append(0)

            elif macd <= 0:
                if fu == 0:  # first round
                    if '-→+' in trend or '-→-' in trend:
                        fu = fu_tmp_sum
                        last_lowest = lowest
                        fu_list = []
                        low_list = []
                        fu_list.append(macd)
                        low_list.append(low)
                        fu_tmp_sum = sum(fu_list)  # 但前区间的macd
                        lowest = min(low_list)  # 但前区间的最低价
                        signal.append(0)
                    else:
                        fu_list.append(macd)
                        low_list.append(low)
                        fu_tmp_sum = sum(fu_list)  # 但前区间的macd
                        lowest = min(low_list)  # 但前区间的最低价
                        signal.append(0)
                elif '+→-' in trend:      # 轮次结束
                    fu = fu_tmp_sum
                    last_lowest = lowest
                    fu_list = []
                    low_list = []
                    zheng_list = []
                    high_list = []
                    fu_list.append(macd)
                    low_list.append(low)
                    fu_tmp_sum = sum(fu_list)  # 当前区间的macd
                    lowest = min(low_list)  # 当前区间的最低价
                    if fu_tmp_sum <= fu and lowest > last_lowest:  # macd面积大于上一轮 最低价高于上轮
                        signal.append('(+→-)buy')
                    elif fu_tmp_sum <= fu and lowest <= last_lowest:  # macd面积大于上一轮 最低价小于上轮
                        signal.append('(+→-)0')
                    elif fu_tmp_sum > fu and lowest > last_lowest:  # macd面积小于上一轮 最低价高于上轮
                        signal.append('(+→-)0')
                    elif fu_tmp_sum > fu and lowest <= last_lowest:  # macd面积小于上一轮 最低价小于上轮
                        signal.append('(+→-)buy')
                elif '-→-' in trend:
                    fu = fu_tmp_sum
                    last_lowest = lowest
                    fu_list = []
                    low_list = []
                    fu_list.append(macd)
                    low_list.append(low)
                    fu_tmp_sum = sum(fu_list)  # 当前区间的macd
                    lowest = min(low_list)  # 当前区间的最低价
                    if fu_tmp_sum <= fu and lowest > last_lowest:  # macd面积大于上一轮 最低价高于上轮
                        signal.append('(-→-)buy')
                    elif fu_tmp_sum <= fu and lowest <= last_lowest:  # macd面积大于上一轮 最低价小于上轮
                        signal.append('(-→-)0')
                    elif fu_tmp_sum > fu and lowest > last_lowest:  # macd面积小于上一轮 最低价高于上轮
                        signal.append('(-→-)0')
                    elif fu_tmp_sum > fu and lowest <= last_lowest:  # macd面积小于上一轮 最低价小于上轮
                        signal.append('(-→-)buy')
                else:
                    fu_list.append(macd)
                    low_list.append(low)
                    fu_tmp_sum = sum(fu_list)  # 当前区间的macd
                    lowest = min(low_list)  # 当前区间的最低价
                    if fu_tmp_sum <= fu and low > last_lowest:     # macd面积大于上一轮 最低价高于上轮
                        signal.append('buy')
                        # if '↑' in trend:
                        #     signal.append('buy')
                        # else:
                        #     signal.append(0)
                    elif fu_tmp_sum <= fu and low <= last_lowest:    # macd面积大于上一轮 最低价小于上轮
                        signal.append(0)
                    elif fu_tmp_sum > fu and low > last_lowest:      # macd面积小于上一轮 最低价高于上轮
                        signal.append(0)
                    elif fu_tmp_sum > fu and low <= last_lowest:     # macd面积小于上一轮 最低价小于上轮
                        signal.append('buy')
        signal.reverse()
        df['signal'] = signal
        return df