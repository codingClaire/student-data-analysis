import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import pickle
from dateutil.parser import parse
from datetime import datetime
import time
import os
import gc
import re
from functools import reduce

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
# 倒排索引
Inverted_termnum_dic={
    0:"14-15秋",1:"14-15寒假",2:"14-15春",3:"14-15暑假",
    4:"15-16秋",5:"15-16寒假",6:"15-16春",7:"15-16暑假",
    8:"16-17秋",9:"16-17寒假",10:"16-17春",11:"16-17暑假",
    12:"17-18秋",13:"17-18寒假",14:"17-18春",15:"17-18暑假",
    16:"18-19秋",17:"18-19寒假",18:"18-19秋",19:"18-19暑假"
}

term_info={
    "14-15秋":['2014-08-31','2015-01-17'],
}


# 学期的开始和结束日期，用以区分寒暑假
dates=['2014-08-31','2015-01-17','2015-03-01','2015-07-18',
       '2015-09-06','2016-01-23','2016-02-28','2016-07-16',
       '2016-09-04','2017-01-14','2017-02-26','2017-07-15',
       '2017-09-03','2018-01-20','2018-03-04','2018-07-21', 
       '2018-09-02','2019-01-19','2019-02-24','2019-07-13',
       '2019-09-01','2020-01-11','2020-02-26']

# 每日时段编号 00：00-08：00是第0时段 
# 1 2 3 4 表示 1-4节课
# 第5时段表示的是中午，该时段直接归为第六节课
# 6 7 8 9 10表示5-9节课
# 第11时段表示下午，该时段的入馆计为第十一节课
# 12 13 14表示11-13节课
# 以此类推，最后一个时段22：30-23：59的编号为16
t=[ "00:00:00","08:00:00", "09:00:00","09:55:00","11:00:00",
    "11:55:00","13:50:00","14:35:00","15:30:00",
    "16:25:00","17:30:00","18:25:00","19:20:00",
    "20:05:00","21:00:00","21:55:00","22:30:00","23:59:00"]
time_list=[]
for i in range(len(t)):
    f=datetime.strptime(t[i],'%X')
    time_list.append(f)
# 用于给时段编号，统一图书馆和课表时段
timenum_dic=[1,1,2,3,4,5,5,6,7,8,9,10,10,11,12,12,12]
time_dic={
    0:"第1节",
    1:"第1节",2:"第2节",3:"第3节",4:"第4节",
    5:"第5节",
    6:"第5节",7:"第6节",8:"第7节",9:"第8节",10:"第9节",
    11:"第10节",
    12:"第10节",13:"第11节",14:"第12节",15:"第12节"
}

# 原图书馆记录为时间记录，修改为节数记录
# 规则如下： 默认其自习完当前整大节课
# 若未到饭点且仍有下一大节课，就通过课表排除其自习的时间
# 在第i节课到达图书馆后，对应列表为记录添加时间
add_dic={
    1:[1,2],2:[2],3:[3,4],4:[4],
    5:[5,6,7],6:[6,7],7:[7],8:[8,9],9:[9],
    10:[10,11,12],11:[11,12],12:[12],
}
# 课表排查列表
check_dic={
    1:[3,4],2:[3,4],3:[],4:[],
    5:[8,9],6:[8,9],7:[8,9],8:[],9:[],
    10:[],11:[],12:[],
}

# 学生-方案计划号字典
stu_fajhh_dic=open_pkl("stu_fajhh.pkl")
# 学号-学院字典
stu_school_dic=open_pkl("stu_school_dic.pkl")
# 学号-专业字典
stu_major_dic=open_pkl("stu_major_dic.pkl")

def calculate_weeknum(datetime1,datetime2):
    # 给定开始日期和当前日期，计算当前日期距离开始日期的周数
    # 用于计算学期周数
    d=(datetime2-datetime1).days
    weeknum=int(d/7+1)
    return weeknum


# 根据时间确定学期
def term_num(year,month,date):
    time=datetime(year,month,date)
    calen=[parse(dates[i]) for i in range(len(dates))]
    for i in range(len(calen)):
        if(calen[i]<=time<=calen[i+1]):
            return i

# 根据时-分-秒时间确定
def cur_num(cur_time):
    formatted_time= datetime.strptime(str(cur_time),'%X')
    for i in range(len(time_list)-1):
        if(time_list[i]<=formatted_time and formatted_time<time_list[i+1]):
            return i

def compute_major():
    # 构建字典 学号-学院和学号-专业
    school_dic={}
    major_dic={}
    df=pd.DataFrame(pd.read_excel("借书次数_change.xls"))
    for index,row in df.iterrows():
        school_dic[row["学号"]]=row["学院"]
        major_dic[row["学号"]]=row["专业"]
    for k,v in school_dic.items():
        print(str(k)+" "+str(v))
    for k,v in school_dic.items():
        print(str(k)+" "+str(v))
    save_pkl("stu_school_dic.pkl",school_dic)
    save_pkl("stu_major_dic.pkl",major_dic)
    
curri_df=pd.DataFrame(pd.read_excel("课程表.xlsx"))
# yhr写的函数
def check_curriculum(stu,term,weeknum,weekday,timenum):
    def partweek(spam1):# 计算周数的函数
        global Set
        Set = set()
        if '/' in spam1:
            spam1 = spam1.split('/')[0]
        beginEndWeek = re.findall(r'\d+', str(spam1))
        if (('单' or '双') in spam1) and ('-' in spam1):
            beginWeek = beginEndWeek[0]
            endWeek = beginEndWeek[1]
            for week in range(int(beginWeek),int(endWeek) + 1,2):
                Set.add(week)
        if (('单' or '双') not in spam1) and ('-' in spam1):
            beginWeek = beginEndWeek[0]
            endWeek = beginEndWeek[1]
            for week in range(int(beginWeek),int(endWeek) + 1,1):
                Set.add(week)
        if len(beginEndWeek) == 1:
             Set.add(int(beginEndWeek[0]))

    global df1,df2,df3,df4,week,weekList
    if stu in curri_df.学号.values:
        df1 = curri_df[curri_df.学号 == stu]
    else:
        return False
    if term in df1.开课学期.values:
        df2 = df1[df1.开课学期 == term]
    else:
        return False
    # weekday 该周的第几天
    if weekday in df2.星期几.values:
        df3 = df2[df2.星期几 == weekday]
    else:
        return False
    # timenum: 第几节课
    if timenum in df3.节数.values:
        df4 = df3[df3.节数 == timenum]
    else:
        return False
    week = re.findall(r'\d+', str(weeknum))
    weekList = []
    for item in df4.itertuples():       
        value = item.上课周次
        partValues = str(value).split(',')
        for partValue in partValues:
            partweek(partValue)
            weekList.append(Set)    
    weekList = reduce(lambda left,right:left | right,weekList)        
    if int(week[0]) in weekList:
        return True
    else:
        return False

def generate_newformat():
    # 新格式
    c=["学号","方案号","院系","专业","年级","学期","星期几","节数","学期第几周"]
    count=0
    new_df= pd.DataFrame(columns=c)
    # 生成教务处要求新表格
    library_df=pd.read_csv("到馆详单_change.csv",iterator=True,low_memory=False)
    '''debug
    library_df=pd.read_csv("到馆详单_change.csv")
    df=library_df[library_df["学号"]==2014757104625]
    print(df.head())
    for index, row in df.iterrows():
        stu=row['学号'] #学号
        fajhh=stu_fajhh_dic[row['学号']] #方案计划号
        school=stu_school_dic[row['学号']] #院系
        major=stu_major_dic[row['学号']] #专业
        grade=row['年级'] #年级
        weekday=datetime(int(row["年"]),int(row["月"]),int(row["日"])).weekday()+1 #星期几
        print(row["标准时间"])
        print(cur_num(row["标准时间"]))
        lessonnum=timenum_dic[cur_num(row["标准时间"])] #课号
        print(lessonnum)
        try:
            termnum=term_num(int(row["年"]),int(row["月"]),int(row["日"])) # 学期对应编号
            term=Inverted_termnum_dic[termnum] #学期名称，包括寒暑假
            weeknum=calculate_weeknum(parse(dates[termnum]),datetime(int(row["年"]),int(row["月"]),int(row["日"]))) #该学期的第几周
            for lesson in add_dic[lessonnum]:
                new_row= pd.DataFrame([[stu,fajhh,school,major,grade,term,weekday,"第"+str(lesson)+"节",weeknum]],columns=c)
                new_df=new_df.append(new_row,ignore_index=True)
                for checklesson in check_dic[lessonnum]:
                    if(check_curriculum(stu,term,weeknum,weekday,checklesson)==False):
                        new_row= pd.DataFrame([[stu,fajhh,school,major,grade,term,weekday,"第"+str(checklesson)+"节",weeknum]],columns=c)
                        new_df=new_df.append(new_row,ignore_index=True)
        except Exception:
            count+=1
            print("count="+str(count))
            print("------")

    '''
    chunkSize=5000
    loop=True
    num=0
    while loop:
        try:
            chunk=library_df.get_chunk(chunkSize)
            for index, row in chunk.iterrows():
                print(index)
                stu=row['学号'] #学号
                fajhh=stu_fajhh_dic[row['学号']] #方案计划号
                school=stu_school_dic[row['学号']] #院系
                major=stu_major_dic[row['学号']] #专业
                grade=row['年级'] #年级
                weekday=datetime(int(row["年"]),int(row["月"]),int(row["日"])).weekday()+1 #星期几
                lessonnum=timenum_dic[cur_num(row["标准时间"])] #课号
                try:
                    termnum=term_num(int(row["年"]),int(row["月"]),int(row["日"])) # 学期对应编号
                    term=Inverted_termnum_dic[termnum] #学期名称，包括寒暑假
                    weeknum=calculate_weeknum(parse(dates[termnum]),datetime(int(row["年"]),int(row["月"]),int(row["日"]))) #该学期的第几周
                    for lesson in add_dic[lessonnum]:
                        new_row= pd.DataFrame([[stu,fajhh,school,major,grade,term,weekday,"第"+str(lesson)+"节",weeknum]],columns=c)
                        new_df=new_df.append(new_row,ignore_index=True)
                    for checklesson in check_dic[lessonnum]:
                        if(check_curriculum(stu,term,weeknum,weekday,checklesson)==False):
                            new_row= pd.DataFrame([[stu,fajhh,school,major,grade,term,weekday,"第"+str(checklesson)+"节",weeknum]],columns=c)
                            new_df=new_df.append(new_row,ignore_index=True)
                except Exception:
                    count+=1
                    print("count="+str(count))
                    print("------")
                    #new_df.to_csv("wrong.csv",index=False,encoding="UTF_8_sig")
            num+=1
            filename="./temp"+str(num)+".csv"
            print(filename)
            new_df.to_csv(filename,index=False,encoding="UTF_8_sig")
            del chunk
            gc.collect()
        except StopIteration:
            loop=False
            print("迭代停止")
    new_df.drop_duplicates(inplace=True)    #去重
    new_df.to_csv("./图书馆.csv",index=False,encoding="UTF_8_sig")

if __name__ == "__main__":
    #curriculum("./to_file")
    #compute_major()
    generate_newformat()
    #a=cur_num("8:31:00")
    #print(a)
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
