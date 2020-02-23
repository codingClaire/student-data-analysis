import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
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
    return ts.index, ts.values


def save_linechart(arrive_month, counts, name):
    fig, ax = plt.subplots()
    plt.plot(arrive_month, counts)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
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
        arrive_month, counts = calculate_freq_month(i, excelFile, "M")
        name = str(i)+".png"
        print(name)
        save_barchart(arrive_month, counts, name)


def get_student_numbers(excelFile, grade):
    df = pd.DataFrame(pd.read_excel(excelFile))
    df_grade = df[df["年级"] == str(grade)+"级"]
    return df_grade["学号"]


if __name__ == "__main__":
    # get_time_series(excelFile)
    all_num = get_student_numbers("借书次数_change.xls", 2015)
    df = pd.DataFrame(pd.read_excel(r"到馆详单_change.xlsx"))
    get_pic_for_all(all_num, df)

    '''
    arrive_month,counts=calculate_freq_month("2015757724600",df,"W")
    save_barchart(arrive_month,counts,"2015757724600")
    
    rng=pd.date_range("2014-01-01",periods=12,freq="M")
    time=pd.Series(np.random.randn(12),index=pd.date_range(dt.datetime(2014,1,1),periods=12,freq="M"))
    time.truncate(before="2014-2-1")
    '''
