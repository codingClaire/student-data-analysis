import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import pickle

def save_pkl(pklname, save_num):
    with open(pklname, "wb") as fp:
        pickle.dump(save_num, fp, protocol=pickle.HIGHEST_PROTOCOL)

def open_pkl(pklname):
    with open(pklname, 'rb') as f:
        datadict = pickle.load(f)
        return datadict

def get_time_series(excelFile):
    # 所有的出入时间的时间序列
    df = pd.DataFrame(pd.read_excel(excelFile))
    result = df['标准时间'].value_counts()
    result_df = result.rename_axis('arrive_date').reset_index(name='counts')  # value_counts()后的值转为dataframe存储
    result_df = result.rename_axis('arrive_date').reset_index(name='counts')  # value_counts()后的值转为dataframe存储
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

def get_student_numbers(year_fajhh_stu_dic,year,fajhh):
    '''
    输入：学期 '201x-201(x+1)-y-1' y=1 or 2        
    方案计划号 849, 2853, 2905, 2915, 2932, 2957, 2959, 2960, 2975, 2988
    输出：学生名单
    '''
    return year_fajhh_stu_dic[year][fajhh]

if __name__ == "__main__":
    #df = pd.DataFrame(pd.read_excel(r"到馆详单_change.xlsx"))
    year_fajhh_stu_dic=open_pkl("year_fajhh_stu.pkl")
    stu_fajhh_dic=open_pkl("stu_fajhh.pkl")
    stu_nums=get_student_numbers(year_fajhh_stu_dic,"2015-2016-1-1",2988)
    print(stu_nums)
    print(type(stu_nums))


