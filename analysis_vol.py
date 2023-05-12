import numpy as np
import pandas as pd


class VolRatio:
    def __init__(self, df):
        self.closes = df['close'].tolist()
        self.date = df['trade_date'].tolist()
        self.vol = df['vol'].tolist()
        self.amount = df['amount'].tolist()
        self.high = df['high'].tolist()
        self.low = df['low'].tolist()

    def analysis(self):
        # 成交额
        volratio_list = []
        yesterday_vol = 0
        for a in self.vol[::-1]:
            if yesterday_vol == 0:
                yesterday_vol = a
                volratio_list.append(0)
            else:
                volratio_list.append((a-yesterday_vol)/yesterday_vol)
                yesterday_vol = a
        volratio_list.reverse()
        # 成交量
        amountratio_list = []
        yesterday_amount = 0
        for a in self.amount[::-1]:
            if yesterday_amount == 0:
                yesterday_amount = a
                amountratio_list.append(0)
            else:
                amountratio_list.append((a-yesterday_amount)/yesterday_amount)
                yesterday_amount = a
        amountratio_list.reverse()
        # 成交均价
        vol_array = np.array(self.vol)
        amount_array = np.array(self.amount)
        average_deal_price = (amount_array/vol_array)*10
        average_deal_price = np.array(average_deal_price)
        # 收盘价变化
        change_list = []
        yesterday_close = 0
        for a in self.closes[::-1]:
            if yesterday_close == 0:
                yesterday_close = a
                change_list.append(0)
            else:
                change_list.append((a-yesterday_close)/yesterday_close)
                yesterday_close = a
        change_list.reverse()
        re = pd.DataFrame({
            'date': self.date,
            'close': self.closes,
            'high': self.high,
            'low': self.low,
            'AVG': average_deal_price,
            'Vol': self.vol,
            'Close Change': change_list,
            'Vol Change': volratio_list,
            # 'Amount Change': amountratio_list,
        })

        # AVG price change
        # AVGP_change_list = []
        # yesterday_close = 0
        # for a in average_deal_price[::-1]:
        #     if yesterday_close == 0:
        #         yesterday_close = a
        #         AVGP_change_list.append(0)
        #     else:
        #         AVGP_change_list.append((a - yesterday_close) / yesterday_close)
        #         yesterday_close = a
        # AVGP_change_list.reverse()
        # re["AVGP Change"] = AVGP_change_list

        # signal
        signal = []
        high_list = []
        low_list = []
        vol_list = []
        cc_list = []
        n = 10
        for index, row in re[::-1].iterrows():
            # close = row['close']
            # avg = row['AVG Price']
            vol = row['Vol']
            cc = row['Close Change']
            high = row['high']
            low = row['low']
            if len(high_list) < n:      # latest 10 days
                high_list.append(high)
                low_list.append(low)
                vol_list.append(vol)
                cc_list.append(cc)
                signal.append(0)
            elif len(high_list) == n:
                df_tmp = pd.DataFrame({
                    'high':high_list,
                    'low':low_list,
                    'vol':vol_list,
                    'cc':cc_list
                })
                highest = df_tmp['high'].max()
                lowest = df_tmp['low'].min()
                highest_index = df_tmp['high'].idxmax()  # 获取highest所在行的index
                lowest_index = df_tmp['low'].idxmin()
                high_vol = df_tmp.at[highest_index, 'vol']  # 获取highest所在行的vol
                low_vol = df_tmp.at[lowest_index, 'vol']
                if high > highest and vol <= high_vol:
                    signal.append('sell')
                elif low <= lowest and vol <= low_vol:
                    signal.append('buy')
                elif low <= lowest and vol > low_vol:
                    signal.append('↓')
                elif high > highest and vol > high_vol:
                    signal.append('↑')
                else:
                    signal.append(0)
                high_list.append(high)      # len(high_list) = 11
                low_list.append(low)
                vol_list.append(vol)
                cc_list.append(cc)
                del high_list[0]
                del low_list[0]
                del vol_list[0]
                del cc_list[0]
        signal.reverse()
        re['signal'] = signal
            # else:
            #     # highest = 0
            #     # lowest = 2000
            #     # for index,row in df_tmp.iterrows():
            #     #     if row['high'] > highest:
            #     #         highest = row['high']
            #     #         high_vol = row['vol']
            #     #     if row['low'] <= lowest:
            #     #         lowest = row['low']
            #     #         low_vol = row['vol']
            #     highest = df_tmp['high'].max()
            #     lowest = df_tmp['low'].min()
            #     highest_index = df_tmp['high'].idxmax()     # 获取highest所在行的index
            #     lowest_index = df_tmp['low'].idxmax()
            #     high_vol = df_tmp.at[highest_index,'vol']   # 获取highest所在行的vol
            #     low_vol = df_tmp.at[lowest_index,'vol']
            #     if high > highest and vol <= high_vol:
            #         signal.append('sell')
            #     elif low <= lowest and vol <= low_vol:
            #         signal.append('buy')
            #     elif low <= lowest and vol > low_vol:
            #         signal.append('↓')
            #     elif high > highest and vol > high_vol:
            #         signal.append('↑')
            #     else:
            #         signal.append(0)
            #     df_tmp.drop([0])                    # 移除行
            #     df_tmp.loc[n] = [high,low,vol,cc]    # 插入行

        # ratio = []
        # for index,row in re[::-1].iterrows():
        #     close = row['close']
        #     avg = row['AVG Price']
        #     if close > avg:
        #         ratio.append((close-avg)/avg)
        #     elif close <= avg:
        #         ratio.append((close - avg) / avg)
        # ratio.reverse()
        # re['ratio'] = ratio
        return re[['date','close','high','low','AVG','Vol','Vol Change','signal',]]
