import pandas as pd
import datetime
import pickle
from matplotlib import pyplot as plt 
import matplotlib.dates as dates
from matplotlib.dates import datestr2num,DateFormatter

def line_chart(excelFile):
    # 所有的出入时间的时间序列
    df = pd.DataFrame(pd.read_excel(excelFile))
    result=df['标准时间'].value_counts()
    result_df = result.rename_axis('arrive_date').reset_index(name='counts') #value_counts()后的值转为dataframe存储
    #按时间排序
    result_df = result_df.sort_values(by = 'arrive_date') 
    result_df.reset_index(inplace=True)
    del result_df['index']

    # 折线图
    arrive_date=pd.Series(result_df['arrive_date'].values)
    counts=pd.Series(result_df['counts'].values)
    plt.plot(arrive_date,counts)
    #plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()

def grade_line_chart(excelFile):
    df = pd.DataFrame(pd.read_excel(excelFile))
    df=df[['标准时间','年级','学号']] #筛选列
    df['id'] = range(len(df))
    #groupby=df.groupby(['标准时间','年级'],as_index=False).count()
    #groupby_df=groupby.reset_index(name="count")
    groupby_df=df.groupby(['标准时间','年级'])['id'].count().reset_index(name="count")

    result_list=[]
    for i in range(2012,2020):
        df_tmp=groupby_df.loc[groupby_df['年级'].isin([str(i)])]
        result_list.append(df_tmp)

    # 折线图
    plt_label=2012
    for i in result_list:
        arrive_date=pd.Series(i['标准时间'].values, index=i['标准时间'])
        counts=pd.Series(i['count'].values, index=i['count'])
        plt.plot(arrive_date,counts,label=str(plt_label) + '年')
        plt_label+=1
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.rcParams['font.sans-serif'] = ['SimHei']#可以plt绘图过程中中文无法显示的问题
    plt.legend()
    plt.show()



if __name__ == "__main__":
    excelFile=r"到馆详单_change.xlsx"
    line_chart(excelFile)