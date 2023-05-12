import numpy as np
import pandas as pd


class KDJ:
    def __init__(self, df):
        self.df = df[['trade_date', 'close', 'high', 'low']]

    def analysis(self):
        n = 9   # period
        low_list = []
        high_list = []
        k = [50]
        rsv = [50]
        d = [50]
        j = []
        for index, row in self.df[::-1].iterrows():
            close = row['close']
            high = row['high']
            low = row['low']
            if len(low_list) < n-1:
                low_list.append(low)
                lowest = min(low_list)      # lowest in n days
                high_list.append(high)
                highest = max(high_list)    # highest in n days
            else:
                low_list.append(low)
                lowest = min(low_list)
                del low_list[0]
                high_list.append(high)
                highest = max(high_list)
                del high_list[0]
            rsv.append(((close-lowest)/(highest-lowest))*100)
            k.append(k[-1]*2/3+rsv[-1]/3)
            d.append(d[-1]*2/3+k[-1]/3)
            j.append(3*k[-1]-2*d[-1])
        del k[0]
        del d[0]
        k.reverse()
        d.reverse()
        j.reverse()
        re = pd.DataFrame({
            'date': self.df['trade_date'],
            'close': self.df['close'],
            'high': self.df['high'],
            'low': self.df['low'],
            'K': k,
            'D': d,
            'J': j
            })
        # intersection
        kd_cross = []
        for index,row in re[::-1].iterrows():
            k = row['K']
            d = row['D']
            if len(kd_cross) == 0:
                kd_cross.append(0)
                if k > d:
                    trend = 0
                else:
                    trend = 1
            elif k > d and trend == 0:
                kd_cross.append(0)
            elif k > d and trend == 1:
                kd_cross.append('↑')
                trend = 0
            elif k <= d and trend == 1:
                kd_cross.append(0)
            elif k <= d and trend == 0:
                kd_cross.append('↓')
                trend = 1
        kd_cross.reverse()
        re['×'] = kd_cross
        # signal
        signal = []
        high_list = []
        low_list = []
        k_list = []
        for index, row in re[::-1].iterrows():
            high = row['high']
            low = row['low']
            k = row['K']
            if len(high_list) < n:
                high_list.append(high)
                low_list.append(low)
                k_list.append(k)
                signal.append(0)
            else:
                df_tmp = pd.DataFrame({         # 0:8
                    'high': high_list,
                    'low': low_list,
                    'k': k_list
                })
                highest = df_tmp[::-1]['high'].max()
                lowest = df_tmp[::-1]['low'].min()
                highest_index = df_tmp[::-1]['high'].idxmax()  # 获取highest所在行的index
                lowest_index = df_tmp[::-1]['low'].idxmin()
                high_k = df_tmp[::-1].at[highest_index, 'k']  # 获取highest所在行的k
                low_k = df_tmp[::-1].at[lowest_index, 'k']
                if high > highest and k <= high_k:
                    signal.append('sell')
                elif low <= lowest and k > low_k:
                    signal.append('buy')
                elif low <= lowest and k <= low_k:
                    signal.append('↓')
                elif high > highest and k > high_k:
                    signal.append('↑')
                else:
                    signal.append(0)
                del high_list[0]
                del low_list[0]
                del k_list[0]
                high_list.append(high)
                low_list.append(low)
                k_list.append(k)
                # df_tmp.loc[len(df_tmp)] = [high,low,k]
                # df_tmp.drop([0])
        signal.reverse()
        re['signal'] = signal
        return re
