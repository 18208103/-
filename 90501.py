import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyecharts.charts import Geo
from pyecharts.charts import Map
from collections import Counter
import re
from wordcloud import WordCloud
from PIL import Image
from pyecharts import options as opts #引入配置项入口

import os
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Bar


plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


# 岗位中各类型企业所占比例
def company_type_show(df):

    # 查看表格某列中有多少个不同值的快捷方法，并计算每个不同值有在该列中有多少重复值
    company_type_count = df.company_type.value_counts()
    #设置中文字体
    font = {'family': 'SimHei'}
    matplotlib.rc('font', **font)
    fig = plt.figure(figsize = (8, 8))      # 设置窗口大小
    #绘制饼图, 参数pctdistance表示饼图内部字体离中心距离, labeldistance则是label的距离, radius指饼图的半径
    patches, l_text, p_text = plt.pie(company_type_count, autopct = '%.2f%%', pctdistance = 0.6, labels = company_type_count.index, labeldistance=1.1, radius = 1)
    # l_text是饼图对着文字大小，p_text是饼图内文字大小
    m, n = 0.02, 0.028
    for t in l_text[7: 11]:
        t.set_y(m)
        m += 0.1
    for p in p_text[7: 11]:
        p.set_y(n)
        n += 0.1
    plt.title('岗位中各类型企业所占比例', fontsize=24)
    plt.show()


# 岗位中各类型企业所占比例
def company_type_chart(df):
    kd = df.company_type.value_counts()
    results = [[k, str(v)] for k, v in dict(kd).items()]
    c = (
        Pie()
            .add("岗位中各类型企业所占比例", results)
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False), )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            .render("./chart/company_type_chart.html")
    )


# 岗位各公司规模总数分布条形图
def company_size_show(df):
    company_size_count = df.company_size.value_counts()
    print(company_size_count)
    index, bar_width = np.arange(len(company_size_count)), 0.6
    fig = plt.figure(figsize=(8, 6))
    # 绘制水平方向的条形图，tick_label：条形的标签名称
    plt.barh(index * (-1) + bar_width, company_size_count, tick_label=company_size_count.index, height=bar_width)
    # 添加数据标签
    # enumerate()函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在for循环当中
    for x, y in enumerate(company_size_count):
        # print(x,y)
        plt.text(y + 0.1, x * (-1) + bar_width, '%s' % y, va='center')  # va:水平对齐方式
    plt.title('岗位各公司规模总数分布条形图', fontsize=24)
    plt.show()


# 岗位城市分布图
def workarea_chart(df):
    # 统计各地区出现次数, 并转换为元组的形式
    data = Counter(df.workarea).most_common()
    print(data)
    # 生成地理坐标图
    # geo = Geo("岗位各地区需求量", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
    # attr, value = geo.cast(data)
    # print(attr)
    # print(value)
    # 添加数据点
    # # type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
    # geo.add('', attr, value, type="effectScatter", visual_range=[0, 100], visual_text_color='#fff', symbol_size=5, is_visualmap=True, is_piecewise=True)
    # geo.show_config()
    # geo.render()
    geo = (
        Geo()
            .add_schema(maptype="china")
            .add("", data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="岗位城市分布图"),
        )
    )
    geo.render("./chart/workarea_chart.html")


# 岗位工作经验要求
def background_chart(df):
        kd = df.background.value_counts()
        results = [[k, str(v)] for k, v in dict(kd).items()]
        c = (
            Pie()
                .add("岗位工作经验要求", results, rosetype="radius", )
                .set_global_opts(legend_opts=opts.LegendOpts(is_show=False), )
                .set_series_opts(tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
            ))
                .render("./chart/background_chart.html")
        )


# 岗位各学历要求所占比例
def education_chart(df):
    kd = df.education.value_counts()
    results = [[k, str(v)] for k, v in dict(kd).items()]
    # html_path = os.path.join(create_or_get_directory(os.path.join('report', 'single')), 'experience_pie_chart.html')
    c = (
        Pie()
            .add("岗位各学历要求所占比例", results, )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False), )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            .render("./chart/education_chart.html")
    )


# 岗位各学历要求所占比例、岗位工作经验要求
def education_background_show(df):
    fig, ax = plt.subplots(1, 2, figsize=(18, 8))# 返回一个包含figure和axes对象的元组, 把父图分成1*2个子图
    education_count = df.education.value_counts()
    background_count = df.background.value_counts()
    patches, l_text, p_text = ax[0].pie(education_count, autopct='%.2f%%', labels=education_count.index)
    m = -0.01
    for t in l_text[6:]:
        t.set_y(m)
        m += 0.1
        print(t)
    for p in p_text[6:]:
        p.set_y(m)
        m += 0.1
    ax[0].set_title('岗位各学历要求所占比例', fontsize=24)
    index, bar_width = np.arange(len(background_count)), 0.6
    ax[1].barh(index * (-1) + bar_width, background_count, tick_label=background_count.index, height=bar_width)
    ax[1].set_title('岗位工作经验要求', fontsize=24)
    # 添加数据标签
    for x, y in enumerate(background_count):
        # print(x,y)
        plt.text(y + 0.1, x * (-1) + bar_width, '%s' % y, va='center')  # va:水平对齐方式
    plt.show()


# 岗位需求量排名前20地区的薪资水平状况
def workarea_salary_show(df):
    fig = plt.figure(figsize=(9, 7))
    # 转换类型为浮点型
    df.low_salary, df.high_salary = df.low_salary.astype(float), df.high_salary.astype(float)
    # 分别求各地区平均最高薪资, 平均最低薪资
    salary = df.groupby('workarea', as_index=False)[['low_salary', 'high_salary']].mean()  # 分别求各地区的岗位数量,并降序排列
    print(salary)
    workarea = df.groupby('workarea', as_index=False)['name'].count().sort_values('name',ascending=False)
    print(workarea)
    workarea = pd.merge(workarea, salary, how='left', on='workarea') # 合并数据表
    print(workarea)
    workarea = workarea.head(20) # 用前20名进行绘图
    plt.bar(workarea.workarea, workarea.name, width=0.8, alpha=0.8)     # alpha：透明度，值越小越透明  '‐‐' 破折线  '‐.' 点划线
    plt.plot(workarea.workarea, workarea.high_salary * 1000, '--', color='g', alpha=0.9, label='平均最高薪资')
    plt.plot(workarea.workarea, workarea.low_salary * 1000, '-.', color='r', alpha=0.9, label='平均最低薪资')
    # 添加数据标签
    for x, y in enumerate(workarea.high_salary * 1000):
        plt.text(x, y, '%.0f' % y, ha='left', va='bottom')
    for x, y in enumerate(workarea.low_salary * 1000):
        plt.text(x, y, '%.0f' % y, ha='right', va='bottom')
    for x, y in enumerate(workarea.name):
        plt.text(x, y, '%s' % y, ha='center', va='bottom')
    plt.legend()    # 给图加上图例
    plt.title('岗位需求量排名前20地区的薪资水平状况', fontsize=20)
    plt.show()


# 各工作经验对应的平均薪资水平(单位:千/月)
def background_salary_show(df):
    # 求出各工作经验对应的平均最高与平均最低薪资
    salary_background = df.groupby('background', as_index=False)[['low_salary', 'high_salary']].mean()
    # 求平均薪资
    salary_background['salary'] = (salary_background.low_salary.add(salary_background.high_salary)).div(2)
    # 转换列, 得到想要的顺序
    salary_background.loc[0], salary_background.loc[6] = salary_background.loc[6], salary_background.loc[0]
    # 绘制条形图
    plt.barh(salary_background.background, salary_background.salary, height=0.6)
    for x, y in enumerate(salary_background.salary):
        plt.text(y + 0.1, x, '%.2f' % y, va='center')
    plt.title('各工作经验对应的平均薪资水平(单位:千/月)', fontsize=20)
    plt.show()
    # plt.savefig("background_salary_show")


# 各学历对应的平均工资水平(单位:千/月)
def education_salary_show(df):
    # 计算平均薪资
    salary_education = df.groupby('education', as_index=False)[['low_salary', 'high_salary']].mean()
    salary_education['salary'] = round(salary_education.low_salary.add(salary_education.high_salary).div(2),2)
    salary_education = salary_education.sort_values('salary', ascending=True)
    # 绘制柱形图
    plt.bar(salary_education.education, salary_education.salary, width=0.6)
    for x, y in enumerate(salary_education.salary):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom')
        # 标签位置
        # ha有三个选择：right, center, left
        # va有四个选择：'top', 'bottom', 'center', 'baseline'
    plt.title('各学历对应的平均工资水平(单位:千/月)', fontsize=20)
    plt.show()



# 各学历对应的平均工资水平(单位:千/月)
def education_salary_chart(df):
    # 计算平均薪资
    salary_education = df.groupby('education', as_index=False)[['low_salary', 'high_salary']].mean()
    salary_education['salary'] = round(salary_education.low_salary.add(salary_education.high_salary).div(2), 2)
    salary_education = salary_education.sort_values('salary', ascending=True)

    print(salary_education.education.tolist())
    print(salary_education.salary.tolist())

    c = (
        Bar()
            .add_xaxis(salary_education.education.tolist())
            .add_yaxis("", salary_education.salary.tolist())
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(yaxis_opts=opts.AxisOpts(name="平均薪资(单位:千/月)", axislabel_opts=opts.LabelOpts(color='red'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             xaxis_opts=opts.AxisOpts(name="学历", axislabel_opts=opts.LabelOpts(color='red'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             tooltip_opts=opts.TooltipOpts(
                                 trigger="item",
                             ),
                             )
            .render("./chart/education_salary_chart.html")
    )


# 岗位所属各领域关键词
def field_show(df):
    field = df.field;
    print(field)
    word = "".join(field);

    # 图片模板和字体
    image = np.array(Image.open('1.png'))    #  mask=image 加入WordCloud
    # 显示中文的关键步骤
    font = r'./fonts/simhei.ttf'

    # 去掉英文，保留中文
    resultword = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\。\@\#\\\&\*\%\-]", " ", word)
    # 现在去掉了中文和标点符号
    print(resultword);

    # 关键一步
    my_wordcloud = WordCloud(font_path=font, scale=4, background_color='white',max_words=100, max_font_size=60, random_state=20).generate(resultword)
    # 显示生成的词云
    plt.imshow(my_wordcloud)
    plt.axis("off")  # 去除边框
    plt.show()



if __name__ == '__main__':
    with open('前程无忧网招聘信息_清洗2.csv', 'r', encoding='UTF-8') as file:

        df = pd.read_csv(file)  # 读取csv

        # company_type_show(df)   # 岗位中各类型企业所占比例
        # company_size_show(df)   # 岗位各公司规模总数分布条形图
        # education_background_show(df)   # 岗位各学历要求所占比例、岗位工作经验要求
        # workarea_salary_show(df)     # 岗位需求量排名前20地区的薪资水平状况
        # background_salary_show(df)  # 各工作经验对应的平均薪资水平(单位:千/月)
        # education_salary_show(df)   # 各学历对应的平均工资水平(单位:千/月)
        # field_show(df)    # 岗位所属各领域关键词
        #
        # # 生成html
        # company_type_chart(df)    # 岗位中各类型企业所占比例
        # background_chart(df)  # 岗位工作经验要求
        # workarea_chart(df)  # 岗位各地区需求量
        # education_chart(df)     # 岗位各学历要求所占比例
        education_salary_chart(df)  # 各学历对应的平均工资水平(单位:千/月)




