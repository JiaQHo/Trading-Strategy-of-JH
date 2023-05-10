import matplotlib.pyplot as plt
import pandas as pd


# MA
class Ma:
    def __init__(self,df):
        self.closes = df["close"].tolist()
        self.date = df["trade_date"].tolist()
        self.high = df["high"].tolist()
        self.low = df["low"].tolist()
        # self.n = n

    def ma(self,n):
        malist = []
        i = n
        while i<=len(self.closes):
            ma = sum((self.closes[i-self.n:i])) / self.n
            i = i+1
            malist.append(ma)
        i = 1
        while i < n:
            malist.append(None)
            i = i + 1
        return malist

    def expma(self,n):
        expma = self.closes[-1]
        expmalist = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i]*2+expma*(n-1))/(n+1)
            expmalist.insert(0,expma)
            i = i-1
        return expmalist

    def plot(self,n):
        expma = self.closes[-1]
        expmalist = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i] * 2 + expma * (n - 1)) / (n + 1)
            expmalist.insert(0, expma)
            i = i - 1
        x = pd.to_datetime(self.date, format='%Y%m%d')
        y = expmalist
        plt.plot(x, y)
        plt.title("Expma %s" % n)
        plt.show()

    def analysis(self,period_a=20,period_b=60,period_c=150,period_d=300):
        # closeshou首次跌穿短期均线再跌穿长期均线，首次回补，而再次跌穿后无法回补所有均线→向下
        # period_a term
        expma = self.closes[-1]
        period_a_expma_list = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i] * 2 + expma * (period_a - 1)) / (period_a + 1)
            period_a_expma_list.insert(0, expma)
            i = i - 1
        # period_b term
        expma = self.closes[-1]
        period_b_expma_list = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i] * 2 + expma * (period_b - 1)) / (period_b + 1)
            period_b_expma_list.insert(0, expma)
            i = i - 1
        # period_c term
        expma = self.closes[-1]
        period_c_expma_list = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i] * 2 + expma * (period_c - 1)) / (period_c + 1)
            period_c_expma_list.insert(0, expma)
            i = i - 1
        # period_d term
        expma = self.closes[-1]
        period_d_expma_list = [expma]
        i = -2
        while abs(i) <= len(self.closes):
            expma = (self.closes[i] * 2 + expma * (period_d - 1)) / (period_d + 1)
            period_d_expma_list.insert(0, expma)
            i = i - 1
        # df
        df_tmp = pd.DataFrame({
            'date': self.date,
            'close': self.closes,
            'period_a': period_a_expma_list,
            'period_b': period_b_expma_list,
            'period_c': period_c_expma_list,
            'period_d': period_d_expma_list
        })
        ls_signal = []
        ls_close = []
        ls_period_a = []
        ls_period_b = []
        ls_period_c = []
        ls_period_d = []
        for row in df_tmp[::-1].itertuples():
            close = getattr(row, 'close')
            period_a = getattr(row, 'period_a')
            period_b = getattr(row, 'period_b')
            period_c = getattr(row, 'period_c')
            period_d = getattr(row, 'period_d')

            if len(ls_close) > 10:
                if ls_close[-1] < ls_period_a[-1] and close > period_a and\
                        ls_close[-1] < ls_period_b[-1] and close > period_b and \
                        ls_close[-1] < ls_period_c[-1] and close > period_c:
                    ls_signal.append('↑↑↑')
                elif ls_close[-1] < ls_period_a[-1] and close > period_a and\
                        ls_close[-1] < ls_period_b[-1] and close > period_b:
                    ls_signal.append('↑↑')
                elif ls_close[-1] < ls_period_d[-1] and close > period_d:
                    ls_signal.append('↑300')
                elif ls_close[-1] < ls_period_c[-1] and close > period_c:
                    ls_signal.append('↑150')
                elif ls_close[-1] < ls_period_b[-1] and close > period_b:
                    ls_signal.append('↑60')
                elif ls_close[-1] < ls_period_a[-1] and close > period_a:
                    ls_signal.append('↑20')
                elif ls_close[-1] > ls_period_a[-1] and close < period_a and \
                        ls_close[-1] > ls_period_b[-1] and close < period_b and \
                        ls_close[-1] > ls_period_c[-1] and close < period_c:
                    ls_signal.append('↓↓↓')
                elif ls_close[-1] > ls_period_a[-1] and close < period_a and \
                        ls_close[-1] > ls_period_b[-1] and close < period_b:
                    ls_signal.append('↓↓')
                elif ls_close[-1] > ls_period_d[-1] and close < period_d:
                    ls_signal.append('↓300')
                elif ls_close[-1] > ls_period_c[-1] and close < period_c:
                    ls_signal.append('↓150')
                elif ls_close[-1] > ls_period_b[-1] and close < period_b:
                    ls_signal.append('↓60')
                elif ls_close[-1] > ls_period_a[-1] and close < period_a:
                    ls_signal.append('↓20')
                else:
                    ls_signal.append(0)
            else:
                ls_signal.append(0)
            ls_close.append(close)
            ls_period_a.append(period_a)
            ls_period_b.append(period_b)
            ls_period_c.append(period_c)
            ls_period_d.append(period_d)

        ls_signal.reverse()
        df_tmp['signal'] = ls_signal
        return df_tmp




# df = pd.read_csv("diary_000782.SZ.csv")
# closes = df["close"].tolist()
#
# ma = Ma(closes,5)
# test_ma = ma.ma()
# test_expma = ma.expma()
# #
# print("ma-5",test_ma)
# print("expma-5",test_expma)


# expma = closes[-1]
# n = 5
# expma = (closes[-2]*2+closes[-1]*(n-1))/(n+1)
# print(closes[-1])
# print(expma)
# print((closes[-2]*2+closes[-1]*(4))/6)