import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Jetton:
    def __init__(self, df):
        self.df = df

    def analysis(self):
        vol_list = []
        amount_list = []
        diary_avg = []
        most_list = []
        profit_percent = []
        for index, row in self.df[['close', 'vol', 'amount']][::-1].iterrows():
            vol_list.append(row['vol'])
            amount_list.append(row['amount'])
            most_list.append(sum(amount_list)*10/sum(vol_list))     # most
            diary_avg.append(row['amount']*10/row['vol'])           # AVG
            df_tmp = pd.DataFrame({
                'vol': vol_list,
                'avg': diary_avg,
                'most': most_list
            })
            df_tmp2 = df_tmp[df_tmp['avg'] < sum(amount_list) * 10 / sum(vol_list)]  # diary avg <  cost
            profit_percent.append(sum(df_tmp2['vol']) / sum(vol_list))
        most_list.reverse()         # 平均成本
        diary_avg.reverse()         # 日成交均价
        profit_percent.reverse()    # 盈利比例
        re = pd.DataFrame({
            'date': self.df['trade_date'],
            'vol': self.df['vol'],
            'close': self.df['close'],
            'avg': diary_avg,
            'avg cost': most_list,
            'profit vol': profit_percent
        })
        return re

    def plot(self):
        vol_list = []
        amount_list = []
        diary_avg = []
        most_list = []
        for index, row in self.df[['vol', 'amount']][::-1].iterrows():
            vol_list.append(row['vol'])
            amount_list.append(row['amount'])
            most_list.append(sum(amount_list)*10/sum(vol_list))
            diary_avg.append(row['amount']*10/row['vol'])
        most_list.reverse()     # 平均成本
        diary_avg.reverse()     # 日成交均价
        diary_avg = np.array(diary_avg)
        vol = np.array(self.df['vol'].tolist())
        re = pd.DataFrame({'vol': vol,
                           'avg': diary_avg,
                           'most': most_list})
        y = re['vol']
        x = re['avg']
        plt.barh(x,y,height=0.02,color='slategrey')
        plt.axhline(y=most_list[0],lw=1.5,ls='solid',color='darkorange',label='AVG deal',alpha=0.6)
        plt.axhline(y=self.df['close'].tolist()[0],lw=0.8,ls='--',color='darkblue',label='Today close')
        plt.axhline(y=diary_avg[0],lw=0.8,ls=':',color='darkviolet',label='Today deal')
        plt.legend()
        return plt.show()