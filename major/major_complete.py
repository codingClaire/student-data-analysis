import pandas as pd
import datetime
import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from matplotlib.dates import datestr2num, DateFormatter
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

def openfile(excelFile):
    df = pd.DataFrame(pd.read_excel(excelFile))
    return df


def fajhh_student_diction(df, grade_year):
    df_year = df[df['开课学期'] == grade_year]
    df_year = df_year[['学号', '方案计划号']]
    df_year.reset_index(inplace=True)
    del df_year['index']
    grouped = df_year['学号'].groupby(df_year['方案计划号'])
    uniquestu = grouped.unique()
    fajhh_stu_tuple = list(uniquestu.items())
    fajhh_stu_dict = {}
    for fajhh, stu_num in fajhh_stu_tuple:
        fajhh_stu_dict[fajhh] = list(stu_num)
    return fajhh_stu_dict


def save_pkl(pklname, save_num):
    with open(pklname, "wb") as fp:
        pickle.dump(save_num, fp, protocol=pickle.HIGHEST_PROTOCOL)


def open_pkl(pklname):
    with open(pklname, 'rb') as f:
        datadict = pickle.load(f)
        return datadict


def add_2_list_remove_duplication(list1, list2):
    # 两个list累加并去重
    list1.extend(list2)
    return list(np.unique(list1))


def add_2_dic_value_list(dic1, dic2):
    # 合并两个字典，字典的value是列表，合并列表时去重list
    keys = add_2_list_remove_duplication(list(dic1.keys()), list(dic2.keys()))
    new_dic = {}
    for key in keys:
        if(key in dic1.keys() and key in dic2.keys()):
            new_dic[key] = add_2_list_remove_duplication(dic1[key], dic2[key])
        elif(key in dic1.keys()):
            new_dic[key] = dic1[key]
        else:
            new_dic[key] = dic2[key]
    return new_dic


def get_year_fajhh_stu_dic_pkl():
    df_stu_14_to_16 = openfile(r"14-16_change.xls")
    df_stu_17_to_19 = openfile(r"17-19_change.xls")
    grade_year_list = add_2_list_remove_duplication(
        list(df_stu_14_to_16['开课学期']), list(df_stu_17_to_19['开课学期']))
    year_fajhh_stu = {}
    for grade_year in grade_year_list:
        ret_dic1 = fajhh_student_diction(df_stu_14_to_16, grade_year)
        ret_dic2 = fajhh_student_diction(df_stu_17_to_19, grade_year)
        year_fajhh_stu[grade_year] = add_2_dic_value_list(ret_dic1, ret_dic2)
    save_pkl("year_fajhh_stu.pkl", year_fajhh_stu)

def get_stu_fajhh_dic_pkl(pklname):
    year_fajhh_stu=open_pkl(pklname)
    stu_fajhh={}
    for year,fajhh_stu in year_fajhh_stu.items():
        for fajhh,stu_list in fajhh_stu.items():
            for stu in stu_list:
                stu_fajhh[stu]=fajhh
    save_pkl("stu_fajhh.pkl", stu_fajhh)
    return stu_fajhh

def stu_book_diction(df):
    df = df[['学号', '图书分类']]
    grouped = df['图书分类'].groupby(df['学号'])
    stu_book_dic = {}
    for name, group in grouped:
        stu_num = group.value_counts()
        stu_book_dic[name] = stu_num.to_dict()
    save_pkl("stu_book.pkl", stu_book_dic)
    return stu_book_dic


def get_stu_book_df():
    df_book = openfile("借书详单_change.xls")
    book_categories = add_2_list_remove_duplication(list(df_book['图书分类']), [])
    book_categories = list(filter(lambda n: n >= chr(
        65) and n <= chr(90), book_categories))  # 筛选A-Z
    stu_book_dic = stu_book_diction(df_book)
    stu_book_df = pd.DataFrame(stu_book_dic).T
    stu_book_df = stu_book_df[book_categories]
    stu_book_df = stu_book_df.fillna(0)
    return stu_book_df


def get_TSNE(df):
    tsne = TSNE()
    tsne.fit_transform(df)  # 进行数据降维
    tsne = pd.DataFrame(tsne.embedding_, index=df.index)  # 转换数据格式
    return tsne

def get_Kmeans(df):
    k = 10
    iteration = 500
    model = KMeans(n_clusters = k, n_jobs = 4, max_iter = iteration) #并发数4
    model.fit(df)
    return model

def classification_result(model,original_df,outputfile):
    #category_num = pd.Series(model.labels_).value_counts() #统计各个类别的数目
    #center = pd.DataFrame(model.cluster_centers_) #找出聚类中心
    r = pd.concat([original_df, pd.Series(model.labels_, index = original_df.index)], axis = 1)  
    r.columns = list(original_df.columns) + [u'聚类类别'] #重命名表头
    r.to_excel(outputfile) #保存结果
    return r

def visualization(tsne_data,model,stu_fajhh_dic):
    #聚类后的可视化图片
    colors=["#476A2A","#7851B8","#BD3430","#4A2D4E","#875525",
            "#A83683","#4E655E","#853541","#3A3120","#535D8E"]
    plt.figure(figsize=(20,20))
    plt.xlim(tsne_data.iloc[:,0].min(),tsne_data.iloc[:,0].max()+1)
    plt.ylim(tsne_data.iloc[:,1].min(),tsne_data.iloc[:,1].max()+1)
    plt.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False #正常显示负号
    stu_list=list(tsne_data.index)
    for i in range(tsne_data.iloc[:,0].size):
        if(stu_list[i] in stu_fajhh_dic.keys()):
            plt.text(tsne_data.iloc[i,0],tsne_data.iloc[i,1],str(stu_fajhh_dic[stu_list[i]]),
                color=colors[tsne_data.iloc[i,2]],
                fontdict={'weight':'bold','size':6})
    plt.xlabel("t-SNE feature 0")
    plt.ylabel("t-SNE feature 1")
    plt.show()


def get_key_from_value(dict,v):
    print(list(dict.keys())[list(dict.values()).index(v)])

if __name__ == "__main__":
    stu_book_df = get_stu_book_df()
    stu_book_tsne_df = get_TSNE(stu_book_df)
    kmeans_model=get_Kmeans(stu_book_tsne_df)
    stu_book_tsne_df =classification_result(kmeans_model,stu_book_tsne_df,"book_classification_result.xls")
    # 学生和方案计划号的字典
    #get_year_fajhh_stu_dic_pkl()
    #get_stu_fajhh_dic_pkl("year_fajhh_stu.pkl")
    stu_fajhh=open_pkl("stu_fajhh.pkl")
    for k,v in stu_fajhh.items():
        print(k)
        print(v)
    visualization(stu_book_tsne_df,kmeans_model,stu_fajhh)
    
