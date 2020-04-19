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

# 学生-方案计划号字典
stu_fajhh_dic=open_pkl("stu_fajhh.pkl")
# 学号-学院字典
stu_school_dic=open_pkl("stu_school_dic.pkl")
# 学号-专业字典
stu_major_dic=open_pkl("stu_major_dic.pkl")

def generate_newformat():
    # 生成教务处要求新表格
    curri_df=pd.DataFrame(pd.read_excel("课程表.xlsx", engine='openpyxl'))
    del curri_df['上课周次']
    stu=curri_df['学号']
    major=[]
    school=[]
    
    for i in range(len(stu)):
        print(i)
        if(stu[i] in stu_school_dic.keys()):
            school.append(stu_school_dic[stu[i]])
        else: school.append("")
        if(stu[i] in stu_major_dic.keys()):
            major.append(stu_major_dic[stu[i]])
        else: major.append("")
    curri_df['院系'] = pd.Series(school)
    curri_df['专业']=pd.Series(major)
    curri_df.to_csv("./课程2.csv",index=False,encoding="UTF_8_sig")

if __name__ == "__main__":
    generate_newformat()

