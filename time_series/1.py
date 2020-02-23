import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import pickle
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import datestr2num, DateFormatter
import matplotlib.pylab as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def get_time_series(excelFile):
    # 所有的出入时间的时间序列
    df = pd.DataFrame(pd.read_excel(excelFile))
    result = df['标准时间'].value_counts()
    result_df = result.rename_axis('arrive_date').reset_index(
        name='counts')  # value_counts()后的值转为dataframe存储
    result_df = result.rename_axis('arrive_date').reset_index(
        name='counts')  # value_counts()后的值转为dataframe存储
    # 按时间排序
    result_df = result_df.sort_values(by='arrive_date')
    result_df.reset_index(inplace=True)
    del result_df['index']


def calculate_freq_month(student_num, df, freq):
    df_stu = df.loc[df["学号"] == student_num]
    index_time = []
    for i, row in df_stu.iterrows():
        time = dt.datetime(int(row['年']), int(row['月']), int(row['日']))
        index_time.append(time)
    t = pd.Series([1]*len(index_time), index=index_time)
    ts = t.resample(freq, closed="left").sum()
    #return ts.index, ts.values
    return ts

def save_linechart(arrive_month, counts, name):
    fig, ax = plt.subplots()
    register_matplotlib_converters()
    plt.plot(arrive_month, counts)
    #plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.xticks(rotation=90)
    # plt.show()
    fig.savefig(name, dpi=300, bbox_inches='tight')


def save_barchart(arrive_month, counts, name):
    fig, ax = plt.subplots()
    plt.bar(arrive_month, counts, width=1, color='steelblue', alpha=0.8)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    plt.title("到馆次数时间序列（以周统计）")
    plt.xlabel("时间")
    plt.ylabel("到馆次数")
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.xticks(rotation=90)
    # plt.show()
    fig.savefig(name, dpi=300, bbox_inches='tight')


def get_pic_for_all(all_num, excelFile):
    for i in all_num:
        ts= calculate_freq_month(i, excelFile, "M")
        arrive_month, counts=ts.index, ts.values
        name = str(i)+".png"
        print(name)
        save_barchart(arrive_month, counts, name)


def get_student_numbers(excelFile, grade):
    df = pd.DataFrame(pd.read_excel(excelFile))
    df_grade = df[df["年级"] == str(grade)+"级"]
    return df_grade["学号"]

def show_onediff(train_series,name):
    series_diff = train_series.diff()
    series_diff = series_diff.dropna()
    plt.figure()
    plt.plot(series_diff)
    plt.title('一阶差分')
    #plt.show()
    plt.savefig(name, dpi=300, bbox_inches='tight')

def ACF_and_PACF(train_series,name):
    acf = plot_acf(train_series, lags=20)
    plt.title("ACF")
    #acf.show()
    acf.savefig(name+"_acf.png", dpi=300, bbox_inches='tight')
    pacf = plot_pacf(train_series, lags=20)
    plt.title("PACF")
    #pacf.show()
    pacf.savefig(name+"_pacf.png", dpi=300, bbox_inches='tight')

def predict_model(train_series,name):
    model = ARIMA(train_series, order=(3, 1, 2),freq='W')
    result = model.fit()
    pred = result.predict('2019-12-01', '2020-05-03',dynamic=True, typ='levels')
    print (pred)
    plt.figure(figsize=(6, 6))
    plt.xticks(rotation=45)
    plt.plot(pred)
    plt.plot(train_series)
    plt.savefig(name+"_pacf.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    # get_time_series(excelFile)
    all_num = get_student_numbers("借书次数_change.xls", 2015)
    df = pd.DataFrame(pd.read_excel(r"到馆详单_change.xlsx"))
    #get_pic_for_all(all_num, df)
    
    num=2017757294552
    ts=calculate_freq_month(num,df,"W")
    arrive_month, counts=ts.index, ts.values
    #save_linechart(arrive_month,counts,"new.png")
    #show_onediff(ts,"onediff.png")
    #ACF_and_PACF(ts,str(num))
    predict_model(ts,str(num)+"predict.png")

    '''
    rng=pd.date_range("2014-01-01",periods=12,freq="M")
    time=pd.Series(np.random.randn(12),index=pd.date_range(dt.datetime(2014,1,1),periods=12,freq="M"))
    time.truncate(before="2014-2-1")
    '''
