import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', **{'family': 'Microsoft YaHei, SimHei'}) 
plt.rcParams['axes.unicode_minus'] = False 

all_df=pd.DataFrame(pd.read_csv("combined_debug.csv"))
Fajhh=2443
Grade=2014
Termnum=2

fajhh_list = list(all_df['方案计划号'].unique())
for Fajhh in fajhh_list:
    for Grade in range(2012,2020):
        for Termnum in range(0,20,2):
            try:
                select=all_df.loc[(all_df['方案计划号']==Fajhh) & (all_df['年级']==Grade) &
                                  (all_df['学期号']==Termnum)]

                data=[]
                for i in range(1,8):
                    week=select.loc[all_df['星期']==i]
                    week_tmp=[]
                    for index,row in week.iterrows():
                        week_tmp.append([row["课程数"],row["图书馆次数"]])
                    data.append(week_tmp)


                timetable=["第一节","第二节","第三节","第四节",
                            "第五节","第六节","第七节","第八节","第九节",
                            "第十节","第十节","第十一节","第十二节","第十三节"]

                fig=plt.figure(figsize=(20,10))#,facecolor='gray')
                weekdays=["周一","周二","周三","周四","周五","周六","周日"]
                for i in range(1,8):
                    ax0=fig.add_subplot(7,1,i)
                    df = pd.DataFrame(data[i-1], columns=['课程次数','图书馆次数'])
                    df.plot(kind='bar',ax =ax0,grid = False,colormap='Set3',stacked=True,legend=(i==8))
                    plt.xticks(())
                    plt.ylabel(weekdays[i-1],rotation="horizontal")

                ax7=fig.add_subplot(7,1,7)
                df = pd.DataFrame(data[6], columns=['课程次数','图书馆次数'])
                df.plot(kind='bar',ax =ax0,grid = False,colormap='Set3',stacked=True)
                plt.xticks(range(len(timetable)),timetable)
                plt.ylabel(weekdays[i-1],rotation="horizontal")
                #plt.show()
                filename=str(Fajhh)+"-"+str(Grade)+"-"+str(Termnum)+".png"
                print(filename)
                plt.savefig(filename)
                plt.clf()
            except:
                a=1

'''
fig, axes =plt.subplots(7, 1)
df = pd.DataFrame(data[0], columns=['课程次数','图书馆次数'])
df.plot(kind='bar',ax = axes[0],grid = False,colormap='Set3',stacked=True)
for i in range(1,7):
    df = pd.DataFrame(data[i], columns=['课程次数','图书馆次数'])
    df.plot(kind='bar',ax = axes[i],grid =False,colormap='Set3',stacked=True,legend=False)
    plt.xlabel("时间段")
    plt.ylabel("次数")
plt.xticks(range(len(timetable)),timetable)
plt.show()
plt.savefig("A.png")
plt.clf()
'''

'''
timetable=["开馆前","第一节","第二节","第三节","第四节",
           "中午","第五节","第六节","第七节","第八节","第九节",
           "晚上","第十节","第十节","第十一节","闭馆后"]
'''