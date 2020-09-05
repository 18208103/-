import csv
import numpy as np
import re
import pandas as pd


pd.set_option('display.max_columns', None)  # 显示所有的列
pd.set_option('display.max_rows', None)  # 显示所有的行

# 把薪资成千/月的形式
def standard_salary(salary):
    if '-' in salary:  # 针对1-2万/月或者10-20万/年的情况，即有数据范围的数据，包含-
        low_salary = re.findall(re.compile('(\d*\.?\d+)'), salary)[0]
        high_salary = re.findall(re.compile('(\d?\.?\d+)'), salary)[1]
        # print(low_salary)
        # print(high_salary)
        if u'万' in salary and u'年' in salary:  # 单位统一成千/月的形式
            low_salary = float(low_salary) / 12 * 10
            high_salary = float(high_salary) / 12 * 10
        elif u'万' in salary and u'月' in salary:
            low_salary = float(low_salary) * 10
            high_salary = float(high_salary) * 10
    else:  # 针对20万以上/年和100元/天这种情况，不包含-，取最低工资，没有最高工资
        low_salary = re.findall(re.compile('(\d*\.?\d+)'), salary)[0]
        high_salary = ""
        if u'万' in salary and u'年' in salary:  # 单位统一成千/月的形式
            low_salary = float(low_salary) / 12 * 10
        elif u'万' in salary and u'月' in salary:
            low_salary = float(low_salary) * 10
        elif u'元' in salary and u'天' in salary:
            low_salary = float(low_salary) / 1000 * 21  # 每月工作日21天
    return low_salary, high_salary

# 将薪资拆分为最高薪资与最低薪资
def split_salary(salary):
    low_salary = []  # 最低薪资
    high_salary = []  # 最高薪资

    ans = 1
    # 把薪资成千/月的形式
    for x in salary:
        print("====split_salary====%d" % ans)
        ans = ans + 1
        if str(x) == "nan":  # 如果待遇这栏不为空，计算最低最高待遇
            low_salary.append("")
            high_salary.append("")
        else:
            getsalary = standard_salary(x)
            low_salary.append(getsalary[0])
            high_salary.append(getsalary[1])

    print(low_salary)
    print(high_salary)

    return low_salary, high_salary


 # 将“地区-区域”转化为“地区”
def workarea_format(workarea):
    new_workarea = []
    ans = 1
    for x in workarea:
        print("====workarea_format====%d" % ans)
        ans = ans + 1
        area = (x.split('-',1))[0]
        new_workarea.append(area)

    return new_workarea

# 工作经验、学历、招生人数的信息有一些错乱，需要调整，并把招生人数的信息精简
def column_adjustment(background, education, recruiters_number):

    # 列出所有学历信息
    all_education = ['初中及以下', '高中', '中技', '中专', '大专', '本科', '硕士', '博士', '无学历要求']

    ans = 1
    for x in range(len(background)):
        print("====column_adjustment====%d" % ans)
        ans = ans + 1

        # 获取原信息
        bg = background[x]
        ed = education[x]
        # print(bg)
        # print(ed)
        if str(ed) != "nan":
            if ed.find(u'招') != -1:
                recruiters_number[x] = ed
                education[x] = ""

        if str(bg) != "nan":
            if bg.find(u'招') != -1:
                recruiters_number[x] = bg
                education[x] = ""
                background[x] = ""
            elif bg in all_education:
                education[x] = bg
                background[x] = ""

        # 化简招聘人数信息，去除招/人字样
        if str(recruiters_number[x]) != "nan" and str(recruiters_number) != "":
            # print("11")
            recruiters_number[x] = recruiters_number[x].lstrip("招")
            recruiters_number[x] = recruiters_number[x].rstrip("人")
            # print(recruiters_number[x])

    return background, education, recruiters_number

# 删除一些缺失数据的行，例如地点缺失，薪资缺失，以及地点为“异地招聘”的行，并将经验缺失的数据用无需经验填补，学历缺失的用初中及以下填补
def delete_fill_data(df):
    low_salary = df['low_salary'].tolist()  # 单独提取出最低薪资的一列
    high_salary = df['high_salary'].tolist()  # 单独提取出最高薪资的一列
    workarea = df['workarea'].tolist()  # 单独提取出地址的一列
    background = df['background'].tolist()  # 单独提取出工作经验的一列
    education = df['education'].tolist()  # 单独提取出学历要求的一列
    company_type = df['company_type'].tolist()  # 单独提取出公司类型的一列

    index = []  #用于记录需要删除的行
    ans = 1
    for x in range(len(workarea)):
        print("====delete_fill_data====%d" % ans)
        ans = ans + 1

        if str(workarea[x]) == "nan" or workarea[x] == "" or workarea[x] == "异地招聘" or str(low_salary[x]) == "nan" or low_salary[x] == "" or str(high_salary[x]) == "nan" or high_salary[x] == "" or str(company_type[x]) == "nan" or company_type[x] == "":
            index.append(x)
        else:
            if str(background[x]) == "nan" or background[x] == "":     # 填补经验缺失值
                background[x] = "无需经验"
            if str(education[x]) == "nan" or education[x] == "":  # 填补学历要求缺失值
                education[x] = "初中及以下"

    # 替换信息
    df['background'] = background
    df['education'] = education
    print(index)    #输出要删除的行
    # 删除行
    new_df = df.drop(index)

    return new_df

if __name__ == '__main__':

    with open('前程无忧网招聘信息.csv', 'r', encoding='UTF-8') as file:
        # reader = csv.reader(file)
        # print(type(reader))
        # 查看所有信息
        # for row in reader:
        #      print(row)

        # 带参数名的一整列
        # salary = [row[3] for row in reader]  # 工资那一列信息
        # print(salary)

        # reader1 = csv.DictReader(file)
        # # # 指定属性的列
        # salary1 = [row['salary'] for row in reader1]

        df = pd.read_csv(file)  # 读取csv
        print(type(df))

        # 提取原信息
        salary = df['salary'].tolist()  # 单独提取出薪资的一列
        workarea = df['workarea'].tolist()  # 单独提取出地址的一列
        background = df['background'].tolist()   # 单独提取出工作经验的一列
        education = df['education'].tolist()     # 单独提取出学历要求的一列
        recruiters_number = df['recruiters_number'].tolist()     # 单独提取出招聘人数的一列

        # 输出信息确认
        print('共有%s条数据' % len(salary))
        print(str(salary[1]))
        print(type(str(salary[1])))
        # print(type(salary[0]))


        # 将薪资拆分为最高薪资与最低薪资
        new_salary = split_salary(salary)

        # 将拆分的薪资信息存入df中
        df['low_salary'] = new_salary[0]  # 增加新的列low_salary
        df['high_salary'] = new_salary[1]  # 增加新的列high_salary
        # print(df['low_salary'])
        # print(df['high_salary'])
        df.drop('salary', axis=1, inplace=True)  # 去除原来的薪资信息，删除列，则要增加参数axis=1，在原DataFrame上进行操作，需要加上inplace=True，等价于在操作完再赋值给本身

        # 将“地区-区域”转化为“地区”
        new_workarea = workarea_format(workarea)
        print(new_workarea)
        df['workarea'] = new_workarea  # 替换列workarea

        # 工作经验、学历、招生人数的信息有一些错乱，需要调整，并把招生人数的信息精简
        new_adj = column_adjustment(background, education, recruiters_number)
        new_background = new_adj[0]
        new_education = new_adj[1]
        new_recruiters_number = new_adj[2]
        print(new_background)
        print(new_education)
        print(new_recruiters_number)
        df['background'] = new_background   # 更新信息
        df['education'] = new_education
        df['recruiters_number'] = new_recruiters_number

        # print("=========")
        # print((df['education'].isna()==True).tolist())

        # index = df[df['background'] == ""].index  # 获取索引
        # index.append(df['background'].isna().index)
        # index1 = df[df['education'] == ""].index  # 获取索引
        # index1.append(df['education'].isna().index)
        # index2 = df[df['recruiters_number'] == ""].index  # 获取索引
        # print(index)
        # print(index1)
        # print(index2)

        # 删除一些缺失数据的行，例如地点缺失，薪资缺失，以及地点为“异地招聘”的行，并将经验缺失的数据用无需经验填补，学历缺失的用初中及以下填补
        new_df = delete_fill_data(df)

        # 查看缺失值数据个数
        print(new_df.isnull().sum())

        # 将清洗后的数据保存到新的csv文件
        new_df.to_csv('前程无忧网招聘信息_清洗.csv', index=None, header=True, encoding='utf_8_sig')
