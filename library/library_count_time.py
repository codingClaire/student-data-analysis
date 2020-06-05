import pandas as pd
import datetime
import pickle
import numpy as np
from matplotlib import pyplot as plt 
import matplotlib.dates as mdates
from matplotlib.dates import datestr2num,DateFormatter
plt.rcParams['font.sans-serif'] = ['SimHei']

'''
这个程序用于显示一天中的各个时间点的进入图书馆次数
值得注意的地方是:
为了使横坐标显示正常，我们需要将横坐标转换为DatetimeIndex的形式
然后用子图里的set_major_locator确定间隔宽度，用set_major_formatter确定显示格式
但是处理后的数据时间列是datetime.time,datetime.time无法转换成datetime.datetime
因此这里先将datetime.time转换成string 然后再从string转到datetime.datetime (to_datetime函数)
最后再用setIndex把该列设置为Index，格式就是DatetimeIndex

'''

def save_variable(v,filename):
    f=open(filename,'wb')
    pickle.dump(v,f)
    f.close()
    return filename

def open_pkl(pklname):
    with open(pklname, 'rb') as f:
        datadict = pickle.load(f)
        return datadict

excelFile=r"library_time_all_4.xlsx"
df = pd.DataFrame(pd.read_excel(excelFile))
result=df['标准时间'].value_counts()
result_df = result.rename_axis('arrive_date').reset_index(name='counts') 
#value_counts()后的值转为dataframe存储
#按时间排序
result_df = result_df.sort_values(by = 'arrive_date') 
result_df.reset_index(inplace=True)
del result_df['index']
#save_variable(result_df,"debug.pkl")
#result_df=open_pkl("debug.pkl")
alist=[]
for i in range(970):
    alist.append(str(result_df['arrive_date'][i]))
arrive_date=pd.to_datetime(alist)
result_df['arrive_date']=arrive_date
result_df['arrive_date']=pd.to_datetime(result_df['arrive_date'])
result_df.set_index("arrive_date",inplace=True)
arrive_date=pd.DatetimeIndex(result_df.index)
# 折线图
counts=pd.Series(result_df['counts'].values)
fig, ax = plt.subplots()
ax.set_title("图书馆入馆时间统计")
ax.plot(arrive_date,counts,'-',label='total')
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))   
ax.set_xlabel(u"时间")
ax.set_ylabel(u"次数")
plt.show()

