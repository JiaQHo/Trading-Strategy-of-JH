import numpy as np
import pandas as pd
from analysis_macd import Macd
from analysis_boll import Boll
from analysis_vol import VolRatio
from analysis_kdj import KDJ
from analysis_ma import Ma
from analysis_linear_close import LinearClose
from analysis_jetton import Jetton
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize    # 独热编码
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

# np.seterr(divide='ignore',invalid='ignore')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width',1000)


def formulate_sign(ls):
    # print(np.array([1, 5, 5, 5]))
    output = []
    for a in ls:
        a = str(a)
        if 'buy' in a:
            a = 1
        elif 'sell' in a:
            a = 2
        elif '↑' in a:
            a = 3
        elif '↓' in a:
            a = 4
        else:
            a = 0
        output.append(a)
    return output


# def formulate_sign(ls):
#     # print(np.array([1, 5, 5, 5]))
#     output = pd.DataFrame(columns=['h1','h2','h3','h1','h5'])
#     for a in ls:
#         a = str(a)
#         if 'buy' in a:
#             a = [0, 1, 0, 0, 0]
#         elif 'sell' in a:
#             a = [0, 0, 1, 0, 0]
#         elif '↑' in a:
#             a = [0, 0, 0, 1, 0]
#         elif '↓' in a:
#             a = [0, 0, 0, 0, 1]
#         else:
#             a = [0, 0, 0, 0, 0]
#         # output.append(a)
#         output.loc[len(output)] = a
#     return output.values


# stock num
code_list = ["000886.SZ"]
# code_list = ["000782.SZ","000677.SZ","601857.SH","000886.SZ"]
# code_list = ["000782.SZ", "000677.SZ", "601857.SH", "000886.SZ", "600905.SH", "000651.SZ", "000333.SZ", "601838.SH",
#              "002258.SZ", "002385.SZ", "000627.SZ", "000420.SZ", "600028.SH", "002129.SZ", "603298.SH", "002432.SZ",
#              "002969.SZ"]

# zhuban = pd.read_csv("zhuban_list.csv")
# code_list = zhuban['code'][:30].tolist() + code_list

for code in code_list:
    # 计算有关指标并整合成数据框
    df = pd.read_csv("D:/脚本/stock diary/diary_%s.csv" % code)[:400]
    # pct_chg = df['pct_chg']
    macd = formulate_sign(Macd(df).analysis()['signal'])
    boll = formulate_sign(Boll(df).analysis()['signal'])
    vol = formulate_sign(VolRatio(df).analysis()['signal'])
    avg = formulate_sign(VolRatio(df).analysis()['AVG'])
    kdj = formulate_sign(KDJ(df).analysis()['signal'])
    ma = formulate_sign(Ma(df).analysis()['signal'])
    lr = formulate_sign(LinearClose(df,20).analysis(20).signal)
    df_X = pd.DataFrame({
        # 'date': df['trade_date'].tolist(),
        # 'close': df['close'].tolist(),
        # 'high': df['high'],
        # 'low': df['low'],
        # 'pct_chg': df['pct_chg'],     # 4.15  close 涨跌幅
        # 'avg': avg,
        'signal_macd': macd,
        'signal_boll': boll,
        'signal_vol': vol,
        'signal_kdj': kdj,
        'signal_ma': ma,
        'signal_lr': lr
    })

    df_y = pd.DataFrame({
        'date': df['trade_date'].tolist(),
        'close': df['close'].tolist(),
        'high': df['high'],
        'low': df['low']
    })
        
    df_y['close_high'] = df_y[::-1].close.rolling(20,min_periods=1).max()
    df_y['close_low'] = df_y[::-1].close.rolling(20,min_periods=1).min()
    ls_target = []
    for row in df_y[::-1].itertuples():
        close_high = getattr(row,'close_high')
        close_low = getattr(row,'close_low')
        close = getattr(row,'close')
        if close == close_high:
            ls_target.append(2)
        elif close == close_low:
            ls_target.append(1)
        else:
            ls_target.append(0)
    ls_target.reverse()

    print(df_X)
    # X = df_X[['signal_macd','signal_boll','signal_vol','signal_kdj','signal_ma','signal_lr']].copy()
    # y = ls_target.copy()
    # # X = X.values
    # print(X)
    # # print(X.values.reshape(-1,6).shape)
    # print(y)
    #
    # base_knn = KNeighborsClassifier()
    # base_lr = LogisticRegression()
    # base_gnb = GaussianNB()
    # base_mnb = MultinomialNB()
    #
    # print('\n',code)
    #
    # print('knn', cross_val_score(base_knn, X, y, cv=5).mean())
    # print('lr', cross_val_score(base_lr, X, y, cv=5).mean())
    # print('gnb', cross_val_score(base_gnb, X, y, cv=5).mean())
    # print('mnb', cross_val_score(base_mnb, X, y, cv=5).mean())
    #
    # gbdt = GradientBoostingClassifier()
    # gbdt.fit(X, y)
    # # 特征重要性
    # # print('Signal:\t', X.columns.values)
    # # print('GBDT_feature_importances_:\t', gbdt.feature_importances_)
    # print(dict(zip(X.columns.values,gbdt.feature_importances_)))
    # print(np.vstack((X.columns.values,gbdt.feature_importances_)))

    # # 数值映射处理
    # unique_arr = X.signal_macd.unique()
    #
    #
    # def map_race(x):
    #     index = np.argwhere(x == unique_arr)[0, 0]
    #     return index
    #
    #
    # X.signal_macd = X.signal_macd.map(map_race)

    # 先映射（用数字替换文本），再转换为独热编码
    # label_binarize(X.signal_macd, classes=np.unique(X.signal_macd))
    # label_binarize(X.signal_boll, classes=np.unique(X.signal_boll))
    # label_binarize(vol, classes=np.unique(vol))
    # label_binarize(kdj, classes=np.unique(kdj))
    # label_binarize(ma, classes=np.unique(ma))
    # label_binarize(lr, classes=np.unique(lr))

    # target = label_binarize(ls_target,classes=np.unique(ls_target))
    # data = df_tmp.values()
    # print(np.ravel(data))
    # X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=1)
    # print(X_train)
