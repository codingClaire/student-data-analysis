import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import pickle
from dateutil.parser import parse
from datetime import datetime
import time
import os

def save_pkl(pklname, save_num):
    with open(pklname, "wb") as fp:
        pickle.dump(save_num, fp, protocol=pickle.HIGHEST_PROTOCOL)

def open_pkl(pklname):
    with open(pklname, 'rb') as f:
        datadict = pickle.load(f)
        return datadict

# 学期编号
termnum_dic={  "14-15秋":0,"14-15春":2,
                "15-16秋":4,"15-16春":6,
                "16-17秋":8,"16-17春":10,
                "17-18秋":12,"17-18春":14,
                "18-19秋":16,"18-19春":18,
            }

# 学期的开始和结束日期，用以区分寒暑假
dates=['2014-08-31','2015-01-17','2015-03-01','2015-07-18',
       '2015-09-06','2016-01-23','2016-02-28','2016-07-16',
       '2016-09-04','2017-01-14','2017-02-26','2017-07-15',
       '2017-09-03','2018-01-20','2018-03-04','2018-07-21', 
       '2018-09-02','2019-01-19','2019-02-24','2019-07-13',
       '2019-09-01','2020-01-11','2020-02-26']

# 每日时段编号 00：00-08：00是第0时段
# 以此类推，最后一个时段22：30-23：59的编号为16
t=[ "00:00","08:00", "09:00","09:55","11:00",
    "11:55","13:50","14:35","15:30",
    "16:25","17:30","18:25","19:20",
    "20:05","21:00","21:55","22:30","23:59"]

# 用于给时段编号，统一图书馆和课表时段
timenum_dic=[1,2,3,4,6,7,8,9,10,12,13,14,15]

# 学生-方案计划号字典
stu_fajhh_dic=open_pkl("stu_fajhh.pkl")


def term_num(year,month,date):
    time=datetime(year,month,date)
    calen=[parse(dates[i]) for i in range(len(dates))]
    for i in range(len(calen)):
        if(calen[i]<=time<=calen[i+1]):
            return i

def cur_num(cur_time):
    cur_time=str(cur_time)
    for i in range(0,len(t)):
        if(t[i]<=cur_time and cur_time<t[i+1]):
            return i

def curriculum(path):
    #先执行curriculum_statistic_first.py 在to_file里面生成文件
    dirs = os.listdir(path)
    c=["方案计划号","学期号","年级","星期","时段编号","课程数","图书馆次数"]
    curri_df= pd.DataFrame(columns=c) 
    for file in dirs:
        # termnum存储学期号 grade 年级 fajhh 方案计划号
        info=file.split(" ")
        term,grade,fajhh=info[0],info[1],info[2].split(".")[0]
        for k,v in termnum_dic.items():
            if term.find(k) != -1:
                termnum=v
                break
        # 读取对应文件
        df=pd.read_csv(path+"/"+file)
        days = ['mon','tue','wed','thu','fri','sat','sun']
        for index, row in df.iterrows():
            timenum=timenum_dic[index]
            for d in range(len(days)):
                weekday=d+1
                currinum=row[days[d]]
                librtime=0
                # type(fajhh) type(termnum) type(grade) type(weekday) type(timenum) type(currinum)
                # str          int              str         int          int          numpy.int64
                new_row= pd.DataFrame([[fajhh,termnum,grade,weekday,timenum,currinum,librtime]],columns=c)
                #        [{'方案计划号':fajhh,'学期号':termnum,'年级':grade,
                #        '星期':weekday,'时段编号':timenum,'课程数':currinum,
                #        '图书馆次数':librtime}]),
                curri_df=curri_df.append(new_row,ignore_index=True) 
    curri_df.to_csv("./curri.csv",index=False,encoding="UTF_8_sig")


    #library_df=pd.DataFrame(pd.read_excel("到馆详单_change.xlsx", engine='openpyxl'))
    library_df=pd.DataFrame(pd.read_csv("到馆详单_change.csv"))
    for index, row in library_df.iterrows():
        print(index)
        try:
            Fajhh=stu_fajhh_dic[row['学号']]
            Grade=row['年级']
            Termnum=term_num(int(row["年"]),int(row["月"]),int(row["日"]))
            Weekday=datetime(int(row["年"]),int(row["月"]),int(row["日"])).weekday()+1
            Timenum=cur_num(row["标准时间"])     
            curri_df.loc[(curri_df['方案计划号']==Fajhh) & (curri_df['年级']==Grade) &
                         (curri_df['时段编号']==Timenum) & (curri_df['星期']==Weekday) &
                         (curri_df['学期号']==Termnum),"图书馆次数"]+=1
        except:
            a=1
    curri_df.to_csv("./combined.csv",index=False,encoding="UTF_8_sig")

def generate_staticcsv(df,stu_fajhh_dic):
    new_df = pd.DataFrame(columns=["方案计划号","学期号","时间","星期","大节编号"]) 
    length=len(df["年"])
    fajhh_list=[]
    for i in range(len(df["学号"])):
        try:
            fajhh_list.append(stu_fajhh_dic[df['学号'][i]])
        except:
            fajhh_list.append(-1)
    new_df['方案计划号']=fajhh_list
    new_df['学期号']=[term_num(int(df["年"][i]),int(df["月"][i]),int(df["日"][i])) for i in range(length)]
    new_df["时间"]=df["标准时间"]
    new_df["星期"]=[datetime(int(df["年"][i]),int(df["月"][i]),int(df["日"][i])).weekday()+1 for i in range(length)]
    new_df["大节编号"]=[cur_num(df["标准时间"][i]) for i in range(length)]
    new_df[new_df["方案计划号"]!=-1]
    new_df=new_df.dropna()
    #new_df.to_csv("./static_4.csv",index=False,encoding="UTF_8_sig")
    return new_df




if __name__ == "__main__":
    #df = pd.DataFrame(pd.read_excel("到馆详单_change.xlsx", engine='openpyxl'))
    #
    #generate_staticcsv(df,stu_fajhh_dic)
    curriculum("./to_file")
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
