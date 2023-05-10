# 标准差：方差的算术平方根，由于方差是数据的平方，一般与检测值本身相差太大，人们难以直观地衡量，
# 所以常用方差开根号（取算术平方根）换算回来。这就是我们要说的标准差（SD）。
# 以日布林线指标为例（N一般=20）：
# 中轨线=N日的移动平均线
# 上轨线（up线）=中轨线+两倍的标准差（2SD）
# 下轨线（down线）=中轨线-两倍的标准差（2SD）
import numpy as np
import pandas as pd


class Boll:

    def __init__(self,df):
        self.closes = df["close"].tolist()
        self.date = df["trade_date"].tolist()
        self.high = df["high"].tolist()
        self.low = df["low"].tolist()

    def summary(self):
        n = 20
        malist = []
        sd_list = []
        i = n
        while (i <= len(self.closes)):
            ma = sum((self.closes[i-n:i])) / n
            i = i + 1
            malist.append(ma)
        i = 1
        while (i < n):
            malist.append(0)
            #sd_list.append(None)
            i = i + 1

        m_a = pd.Series(malist)
        c_l = pd.Series(self.closes)
        persd_list = (c_l - m_a)**2
        persd_list = persd_list.tolist()

        i = n
        while(abs(i)<len(self.closes)):
             # sd = np.sqrt((sum(persd_list[i-n:i])/n))
             # sd = np.std(persd_list[i-n:i])
             sd = np.std(self.closes[i-n:i])
             sd_list.append(sd)
             i = i + 1

        sd_list = pd.Series(sd_list)
        boll_up = m_a + sd_list*2
        boll_down = m_a - sd_list*2
        summary = pd.DataFrame({
            "date":self.date,
            "close":self.closes,
            "boll.mid":m_a,
            "boll.up":boll_up,
            "boll.down":boll_down
        })
        return summary

    def analysis(self):
        n = 20
        malist = []
        sd_list = []
        i = n
        while i <= len(self.closes):
            ma = sum((self.closes[i-n:i])) / n
            i = i + 1
            malist.append(ma)
        i = 1
        while i < n:
            malist.append(self.closes[-1])
            #sd_list.append(None)
            i = i + 1

        m_a = pd.Series(malist)
        c_l = pd.Series(self.closes)
        persd_list = (c_l - m_a)**2
        persd_list = persd_list.tolist()

        i = n
        while abs(i)<len(self.closes):
             # sd = np.sqrt((sum(persd_list[i-n:i])/n))
             # sd = np.std(persd_list[i-n:i])
             sd = np.std(self.closes[i-n:i])
             sd_list.append(sd)
             i = i + 1

        sd_list = pd.Series(sd_list)
        boll_up = m_a + sd_list*2
        boll_down = m_a - sd_list*2
        summary = pd.DataFrame({
            "date": self.date,
            "close": self.closes,
            "high": self.high,
            "low": self.low,
            "boll.mid": m_a,
            "boll.up": boll_up,
            "boll.down": boll_down
        })
        signal = []
        for index, row in summary.iterrows():
            if row['close'] >= row['boll.mid']:     # close >= boll.mid
                if row['close'] >= row['boll.up']:
                    signal.append('up-↑')
                elif row['high'] >= row['boll.up']:
                    signal.append('up-sell')
                elif row['low'] <= row['boll.mid']:
                    signal.append('mid-↑')
                else:
                    signal.append('0')
            elif row['close'] < row['boll.mid']:    # close < boll.mid
                if row['close'] <= row['boll.down']:
                    signal.append('down-↓')
                elif row['low'] <= row['boll.down']:
                    signal.append('down-buy')
                elif row['high'] >= row['boll.mid']:
                    signal.append('mid-↓')
                else:
                    signal.append('0')

        # for index,row in summary.iterrows():
        #     if row['low'] <= row['boll.down']:
        #         signal.append('buy')
        #     elif row['high'] >= row['boll.up']:
        #         signal.append('sell')
        #     else:
        #         signal.append('0')
        summary['signal'] = signal
        return summary

#
# df = pd.read_csv("diary_002385.SZ.csv")
# closes = df["close"].tolist()
# date = df["trade_date"].tolist()
# high = df["high"].tolist()
# low = df["low"].tolist()
#
# boll = Boll(closes,date,high,low)
#
#
# # print(closes)
# # print(len(closes))
#
# print(boll.analysis()[:60])
