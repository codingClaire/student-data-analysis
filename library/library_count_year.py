import pandas as pd
import datetime
import pickle
from matplotlib import pyplot as plt 
import matplotlib.dates as dates
from matplotlib.dates import datestr2num,DateFormatter
plt.rcParams['font.sans-serif'] = ['SimHei']#可以plt绘图过程中中文无法显示的问题

def line_chart(excelFile):
    df = pd.DataFrame(pd.read_excel(excelFile))
    result=df['标准时间'].value_counts()
    result_df = result.rename_axis('arrive_date').reset_index(name='counts') #value_counts()后的值转为dataframe存储
    #按时间排序
    result_df = result_df.sort_values(by = 'arrive_date') 
    result_df.reset_index(inplace=True)
    del result_df['index']

    # 折线图
    arrive_date=pd.Series(result_df['arrive_date'].values, index=result_df['arrive_date'])
    counts=pd.Series(result_df['counts'].values, index=result_df['counts'])
    plt.plot(arrive_date,counts)
    plt.title("图书馆到馆次数随时间变化图(按日统计)")
    plt.xlabel("时间（年）")
    plt.ylabel("次数")
    plt.show()

def grade_line_chart(excelFile,a,b):
    df = pd.DataFrame(pd.read_excel(excelFile))
    df=df[['标准时间','年级','学号']] #筛选列
    df['id'] = range(len(df))
    #groupby=df.groupby(['标准时间','年级'],as_index=False).count()
    #groupby_df=groupby.reset_index(name="count")
    groupby_df=df.groupby(['标准时间','年级'])['id'].count().reset_index(name="count")
    result_list=[]
    for i in range(a,b):
        df_tmp=groupby_df.loc[groupby_df['年级'].isin([str(i)])]
        result_list.append(df_tmp)

    # 折线图 
    plt_label=a
    for i in result_list:
        arrive_date=pd.Series(i['标准时间'].values, index=i['标准时间'])
        counts=pd.Series(i['count'].values, index=i['count'])
        plt.plot(arrive_date,counts,label=str(plt_label) + '级')
        plt_label+=1
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.title(str(a)+"-"+str(b-1)+"级图书馆到馆次数随时间变化图(按日统计)")
    plt.xlabel("时间（年）")
    plt.ylabel("次数")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    line_chart("到馆详单_change2.xlsx")
    grade_line_chart("到馆详单_change2.xlsx",2012,2020)
    grade_line_chart("到馆详单_change2.xlsx",2015,2018)
