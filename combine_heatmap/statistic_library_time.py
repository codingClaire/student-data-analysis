import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import pickle
from dateutil.parser import parse
from datetime import datetime

def save_pkl(pklname, save_num):
    with open(pklname, "wb") as fp:
        pickle.dump(save_num, fp, protocol=pickle.HIGHEST_PROTOCOL)

def open_pkl(pklname):
    with open(pklname, 'rb') as f:
        datadict = pickle.load(f)
        return datadict

def term_num(year,month,date):
    time=datetime(year,month,date)
    #print(time)
    dates=['2014-08-31','2015-01-17','2015-03-01','2015-07-18',
           '2015-09-06','2016-01-23','2016-02-28','2016-07-16',
           '2016-09-04','2017-01-14','2017-02-26','2017-07-15',
           '2017-09-03','2018-01-20','2018-03-04','2018-07-21', 
           '2018-09-02','2019-01-19','2019-02-24','2019-07-13',
           '2019-09-01','2020-01-11','2020-02-26']
    calen=[parse(dates[i]) for i in range(len(dates))]
    for i in range(len(calen)):
        if(calen[i]<=time<=calen[i+1]):
            return i
    '''
    14-15秋 2014-08-31 2015-01-17 0
    14-15春 2015-03-01 2015-07-18 2
    15-16秋 2015-09-06 2016-01-23 4
    15-16春 2016-02-28 2016-07-16 6
    16-17秋 2016-09-04 2017-01-14 8
    16-17春 2017-02-26 2017-07-15 10
    17-18秋 2017-09-03 2018-01-20 12
    17-18春 2018-03-04 2018-07-21 14
    18-19秋 2018-09-02 2019-01-19 16
    18-19春 2019-02-24 2019-07-13 18
    '''

def generate_staticcsv(df,stu_fajhh_dic):
    new_df = pd.DataFrame(columns=["方案计划号","学期号","时间","星期"]) 
    fajhh_list=[]
    for i in range(len(df["学号"])):
        try:
            fajhh_list.append(stu_fajhh_dic[df['学号'][i]])
        except:
            #fajhh_list.append(-1)
    new_df['方案计划号']=fajhh_list
    new_df['学期号']=[term_num(int(df["年"][i]),int(df["月"][i]),int(df["日"][i])) for i in range(len(df["年"]))]
    new_df["时间"]=df["标准时间"]
    print(type(df["年"]))
    new_df["星期"]=[datetime(int(df["年"][i]),int(df["月"][i]),int(df["日"][i])).weekday() for i in range(len(df["年"]))]
    new_df[new_df["方案计划号"]!=-1]
    new_df.to_csv("./static_2.csv",index=False,encoding="UTF_8_sig")

def generate_fajhh_year_csv(csv_file):
    df = pd.DataFrame(pd.read_csv("static.csv"))
    group=df.groupby(["方案计划号","学期号"])
    for (k1,k2),g in group:
        print((k1,k2))
        filename=str(k1)+"-"+str(k2)+".csv"
        if(k1!=-1):
            g_df=g.reset_index()
            new_g=generate_d3_csv(g_df)
            new_g.to_csv(filename,index=False,encoding="UTF_8_sig")

def generate_d3_csv(df):
    '''
    这里是随便使用了一个用上一个函数生成的csv文件，
    目的是为了看看csv文件能不能跑通，实际上最终以数据库存储方式的话
    就不需要这个过程
    '''
    #df = pd.DataFrame(pd.read_csv("2901-16.0.csv"))
    weekdays=["周一","周二","周三","周四","周五","周六","周日"]
    
    counts=[0,0,0,0,0,0,0]
    new_list=[[],[],[],[],[],[],[]]
    new_df = pd.DataFrame(columns=weekdays)
    for i in range(len(df["星期"])):
        n=int(df["星期"][i])
        new_list[n].append(int(int(df["时间"][i].split(":")[0])*60+int(df["时间"][i].split(":")[1])))
    for i in range(7):
        print(len(new_list[i]))
        print(new_list[i])
        new_df[weekdays[i]]=pd.Series(new_list[i])
    #new_df.to_csv("change.csv",index=False,encoding="UTF_8_sig")
    return new_df


if __name__ == "__main__":
    #df = pd.DataFrame(pd.read_excel("到馆详单_change.xlsx", engine='openpyxl'))
    #stu_fajhh_dic=open_pkl("stu_fajhh.pkl")
    generate_staticcsv(df,stu_fajhh_dic)
    #generate_fajhh_year_csv("static.csv")
    
    '''
    year_fajhh_stu_dic=open_pkl("year_fajhh_stu.pkl")
    stu_fajhh_dic=open_pkl("stu_fajhh.pkl")
    stu_nums=get_student_numbers(year_fajhh_stu_dic,"2015-2016-1-1",2988)
    print(stu_nums)
    print(type(stu_nums))
    '''
