import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyecharts.charts import Geo
from pyecharts.charts import Map
from collections import Counter
from bs4 import BeautifulSoup
import re
# from wordcloud import WordCloud
from PIL import Image
from pyecharts import options as opts #引入配置项入口

import os
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts.charts import Grid
from pyecharts.charts import Line
from pyecharts.charts import Page
from pyecharts.charts import WordCloud
import jieba
import jieba.analyse
from pyecharts import options as opts
from pyecharts.globals import SymbolType,ThemeType

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False

# 风格
themes = ThemeType.DARK

# 中间大标题
def title():
    big_title = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="热门需求职位信息可视化",
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#FFFFFF',
                                                                              border_radius=True, border_color="white"),
                                      pos_top=0)))
    return big_title

# 主要数据展示

def data_show1():
    size = (Pie(init_opts=opts.InitOpts(theme=themes)).
                set_global_opts(title_opts=opts.TitleOpts(title="总数据量", pos_left='center', pos_top='center',
                                                          title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
    return size

def data_show2(df):
    # 查找有多少各数据
    data_size = df.name.count()
    print(data_size)
    df1 = pd.read_csv('清洗后数据.csv')
    data_size1 = df1.name.count()
    print(data_size1)
    size1 = (Pie(init_opts=opts.InitOpts(theme=themes)).
             set_global_opts(title_opts=opts.TitleOpts(title=str(data_size + data_size1),
                                                       pos_top='15%', pos_left='center',
                                                       item_gap=1,
                                                       title_textstyle_opts=opts.TextStyleOpts(
                                                           color="#00FFFF",
                                                           font_size=30),
                                                       )))
    return size1

def data_show3():
    area = (Pie(init_opts=opts.InitOpts(theme=themes)).
            set_global_opts(title_opts=opts.TitleOpts(title="岗位数量最多的城市", pos_left='center', pos_top='center',
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
    return area

def data_show4(df):
    workarea = df.groupby('workarea', as_index=False)['name'].count().sort_values('name', ascending=False)
    first_workarea = (workarea.workarea.tolist())[0]      # 找到岗位数量最多的城市
    print(first_workarea)
    area1 = (Pie(init_opts=opts.InitOpts(theme=themes)).
                    set_global_opts(title_opts=opts.TitleOpts(title=first_workarea,
                                                              pos_top='15%', pos_left='center',
                                                              item_gap=1,
                                                              title_textstyle_opts=opts.TextStyleOpts(color="#FF00FF",font_size=30),
                                                              )))
    return area1

# 岗位中各类型企业占比图
def company_type_chart(df):
    kd = df.company_type.value_counts()
    results = [[k, str(v)] for k, v in dict(kd).items()]
    c = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .add("岗位中各类型企业类型", results)
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                             title_opts=opts.TitleOpts(
                                 title="岗位中各类型企业占比图",
                                 title_link='./chart/company_type_chart.html',
                                 title_target='blank',
                                 pos_left='left',
                                ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            # .render("./chart/company_type_chart.html")
    )
    return c

# 岗位各公司规模占比图
def company_size_chart(df):
    kd = df.company_size.value_counts()
    results = [[k, str(v)] for k, v in dict(kd).items()]
    c = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .add("岗位中各公司规模", results,  rosetype="radius", ) #  rosetype="radius" 南丁格尔玫瑰图
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                             title_opts=opts.TitleOpts(
                                 title="岗位各公司规模占比图",
                                 title_link='./chart/company_size_chart.html',
                                 title_target='blank',
                                 pos_left='left',
                             ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            # .render("./chart/company_size_chart.html")
    )

    return c


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
        Geo(init_opts=opts.InitOpts(theme=themes))
            .add_schema(maptype="china")
            .add("", data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(),
                title_opts=opts.TitleOpts(title="岗位城市分布图",
                                          title_link='./chart/workarea_chart.html',
                                          title_target='blank',
                                          pos_left='left',
                                          ),
                # 多功能组件
                toolbox_opts=opts.ToolboxOpts(is_show=True),
             )
    )
    # geo.render("./chart/workarea_chart.html")
    return geo

# 岗位工作经验要求占比图
def background_chart(df):
        kd = df.background.value_counts()
        results = [[k, str(v)] for k, v in dict(kd).items()]
        c = (
            Pie(init_opts=opts.InitOpts(theme=themes))
                .add("岗位工作经验要求", results, rosetype="radius", ) #  rosetype="radius" 南丁格尔玫瑰图
                .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                                 title_opts=opts.TitleOpts(title="岗位工作经验要求占比图",
                                                           title_link='./chart/background_chart.html',
                                                           title_target='blank',
                                                           pos_left='left',
                                                           ),
                                 # 多功能组件
                                 toolbox_opts=opts.ToolboxOpts(is_show=True),
                                 )
                .set_series_opts(tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
            ))
                # .render("./chart/background_chart.html")
        )
        return c


# 岗位各学历要求占比图
def education_chart(df):
    kd = df.education.value_counts()
    results = [[k, str(v)] for k, v in dict(kd).items()]
    c = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .add("岗位各学历要求", results, )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                             title_opts=opts.TitleOpts(title="岗位各学历要求占比图",
                                                       title_link='./chart/education_chart.html',
                                                       title_target='blank',
                                                       pos_left='left',
                                                       ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            # .render("./chart/education_chart.html")
    )
    return c

# 岗位领域统计
def field_chart(df):
    kd = df.field.value_counts()
    print(kd)
    results = [[k, str(v)] for k, v in dict(kd).items()]
    c = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .add("岗位领域", results, )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                             title_opts=opts.TitleOpts(title="岗位领域统计",
                                                       title_link='./chart/field_chart.html',
                                                       title_target='blank',
                                                       pos_left='left',
                                                       ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)",
        ))
            # .render("./chart/field_chart.html")
    )
    return c



# 岗位需求量排名前20地区的平均薪资水平状况
def workarea_salary_chart(df):
    # 转换类型为浮点型
    df.low_salary, df.high_salary = df.low_salary.astype(float), df.high_salary.astype(float)
    # 分别求各地区平均最高薪资, 平均最低薪资
    salary = df.groupby('workarea', as_index=False)[['low_salary', 'high_salary']].mean()  # 分别求各地区的岗位数量,并降序排列
    print(salary)
    workarea = df.groupby('workarea', as_index=False)['name'].count().sort_values('name', ascending=False)
    print(workarea)
    workarea = pd.merge(workarea, salary, how='left', on='workarea')  # 合并数据表
    print(workarea)
    workarea = workarea.head(20)  # 用前20名进行绘图

    grid = Grid()
    bar = Bar()
    grid.theme = themes
    line = Line()
    line1 = Line()

    bar.add_xaxis(workarea.workarea.tolist())
    bar.add_yaxis("岗位需求量", workarea.name.tolist())
    bar.set_global_opts(title_opts=opts.TitleOpts(title="岗位需求量排名前20地区的平均薪资水平状况",
                                                  title_link='./chart/workarea_salary_chart.html',
                                                  title_target='blank',
                                                  pos_left='left',
                                                  ),
                       tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross", is_show=True), # 交叉指向工具
                        legend_opts = opts.LegendOpts( pos_left="80%", orient="vertical", pos_top="3%" ),
                       )
    # bar.set_series_opts(is_show=True, position='rightTop')
    print((workarea.name).tolist())
    print((round(workarea.high_salary * 1000)).tolist())
    # 在bar上增加Y轴，在line图上选择对应的轴向
    line.add_xaxis(workarea.workarea.tolist())
    line.add_yaxis("平均最高薪资", (round(workarea.high_salary * 1000)).tolist(), yaxis_index = 0)
    line1.add_xaxis(workarea.workarea.tolist())
    line1.add_yaxis("平均最低薪资", (round(workarea.low_salary * 1000)).tolist(), yaxis_index = 0)
    # 把line添加到bar上
    bar.overlap(line)
    bar.overlap(line1)
    # 这里如果不需要grid也可以，直接设置bar的格式，然后显示bar即可
    #bar.render_notebook()
    grid.add(chart = bar, grid_opts = opts.GridOpts(),is_control_axis_index = True)
    # grid.render("./chart/workarea_salary_chart.html")
    return grid



# 各学历对应的平均工资水平(单位:千/月)
def education_salary_chart(df):
    # 计算平均薪资
    salary_education = df.groupby('education', as_index=False)[['low_salary', 'high_salary']].mean()
    salary_education['salary'] = round(salary_education.low_salary.add(salary_education.high_salary).div(2), 2)
    salary_education = salary_education.sort_values('salary', ascending=True)

    print(salary_education.education.tolist())
    print(salary_education.salary.tolist())

    c = (
        Bar(init_opts=opts.InitOpts(theme=themes))
            .add_xaxis(salary_education.education.tolist())
            .add_yaxis("", salary_education.salary.tolist())
            # .reversal_axis()  # 翻转XY轴
            # 数据标签显示
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position = "top"))
            .set_global_opts(yaxis_opts=opts.AxisOpts(name="平均薪资(单位:千/月)", axislabel_opts=opts.LabelOpts(color='white'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             xaxis_opts=opts.AxisOpts(name="学历", axislabel_opts=opts.LabelOpts(color='white'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             tooltip_opts=opts.TooltipOpts(
                                 trigger="item",    # 数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
                             ),
                             title_opts=opts.TitleOpts(
                                 # 主标题文本
                                title="各学历对应的平均薪资水平(单位:千/月)",
                                # 主标题跳转 URL 链接
                                title_link='./chart/education_salary_chart.html',
                                 # 主标题跳转链接方式
                                 # 默认值是: blank
                                 # 可选参数: 'self', 'blank'
                                 # 'self' 当前窗口打开; 'blank' 新窗口打开
                                 title_target='blank',
                                 # title 组件离容器左侧的距离
                                 # left 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比
                                 # 也可以是 'left', 'center', 'right','top', 'middle', 'bottom'
                                 # 如果 left 的值为'left', 'center', 'right'，组件会根据相应的位置自动对齐。
                                 pos_left='left',
                             ),
                            # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),

                             )
            # .render("./chart/education_salary_chart.html")
    )
    return c

# 各工作经验对应的平均薪资水平(单位:千/月)
def background_salary_chart(df):
    # 求出各工作经验对应的平均最高与平均最低薪资
    salary_background = df.groupby('background', as_index=False)[['low_salary', 'high_salary']].mean()
    # 求平均薪资
    salary_background['salary'] = round((salary_background.low_salary.add(salary_background.high_salary)).div(2), 2)
    # 转换列, 得到想要的顺序
    salary_background.loc[0], salary_background.loc[6] = salary_background.loc[6], salary_background.loc[0]

    c = (
        Bar(init_opts=opts.InitOpts(theme=themes))
            .add_xaxis(salary_background.background.tolist())
            .add_yaxis("", salary_background.salary.tolist())
            .reversal_axis()  # 翻转XY轴
            # 数据标签显示
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True,position = "right"))
            .set_global_opts(yaxis_opts=opts.AxisOpts(name="平均薪资(单位:千/月)", axislabel_opts=opts.LabelOpts(color='white'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             xaxis_opts=opts.AxisOpts(name="经验", axislabel_opts=opts.LabelOpts(color='white'),
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#d48265')),
                             tooltip_opts=opts.TooltipOpts(
                                 trigger="item",    # 数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
                             ),
                             title_opts=opts.TitleOpts(
                                 # 主标题文本
                                title="各工作经验对应的平均薪资水平(单位:千/月)",
                                # 主标题跳转 URL 链接
                                title_link='./chart/background_salary_chart.html',
                                 # 主标题跳转链接方式
                                 # 默认值是: blank
                                 # 可选参数: 'self', 'blank'
                                 # 'self' 当前窗口打开; 'blank' 新窗口打开
                                 title_target='blank',
                                 # title 组件离容器左侧的距离
                                 # left 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比
                                 # 也可以是 'left', 'center', 'right','top', 'middle', 'bottom'
                                 # 如果 left 的值为'left', 'center', 'right'，组件会根据相应的位置自动对齐。
                                 pos_left='left',
                             ),
                            # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),

                             )
            # .render("./chart/background_salary_chart.html")
    )
    return c



#融资饼图
def setrose():
    df = pd.read_csv('金融阶段.csv')
    # 除去无用数据
    df = df[~df['financeStage'].str.contains('financeStage')]

    result = pd.value_counts(df['financeStage'])
    resulted = dict(result)
    ed = list(resulted.keys())
    edvalues = list(resulted.values())
    edvaluesint = []
    for i in edvalues:
        edvaluesint.append(int(i))

    c = (
        Pie(init_opts=opts.InitOpts(theme=themes))
            .add(
            "",
            [list(z) for z in zip(ed, edvaluesint)],
            radius=["30%", "75%"],
            center=["50%", "50%"],
            rosetype="area",  # 选择南丁格尔图类型，area：所有扇区圆心角相同，仅通过半径展现数据大小
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="金融阶段饼图",
                                      title_link='./chart/financeStage.html',
                                      title_target='blank',
                                      pos_left='left',
                                      ),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="85%", orient="vertical", pos_top="50%"
            ),
            # 多功能组件
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    # c.render('./chart/financeStage.html')
    # c.render_notebook()
    return c

#技能词云
def setword1():
    df = pd.read_csv('要求技能.csv')
    needs = []
    for i in df['thirdType']:
        needs.append(i)

    set_need = str(needs).replace('|', " ")

    # 设置停止词，删除无关的词
    stopwords = [ '内容', '销售', '助理', '其他', '商务', '产品', '经理', '售后', '职能', '职位', '视觉', '主管', '管理', '项目',
                 '运营','广告投放','广告','编辑','顾问','客服','视频','保险','业务','清算','音频','电话','大客户','代表','网店','抖音','主播',
                 '行政','专员','看看','技术','总监','前台','用户','普工','操作工','企业','理财','软件','全栈','招聘','在线','新媒体','媒体','审核'
                  ,'出纳','市场推广','拓展','文案','市场','营销','推广','售前','人事','技术支持','渠道','市场营销','项目管理','项目经理','媒介','客户'
                  ,'财务','客户经理','培训']
    jieba_need = jieba.analyse.extract_tags(set_need, topK=80, withWeight=True)
    jieba_result = []
    for i in jieba_need:
        if i[0] not in stopwords:
            jieba_result.append(i)

    c = (
        WordCloud(init_opts=opts.InitOpts(theme=themes))
            .add("", jieba_result, word_size_range=[20, 100], shape=SymbolType.RECT)
            .set_global_opts(title_opts=opts.TitleOpts(title="技能词云",
                                                       title_link='./chart/skill.html',
                                                       title_target='blank',
                                                       pos_left='left',
                                                       ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
    )
    # c.render('./chart/skill.html')
    # c.render_notebook()
    return c



#福利词云
def setword2():
    df = pd.read_csv('福利待遇.csv')
    needs = []
    for i in df['positionAdvantage']:
        needs.append(i)

    set_need = str(needs).replace(',', " ").replace('、', " ").replace('/', " ").replace('"'," ")\
        .replace(';', " ").replace('&amp', " ").replace('n', " ").replace('ice', "nice")

    # 设置停止词，删除无关的词
    stopwords = ['互联网', '大型', '公司的', '+', '综合', '管理', '行业', '提供', '统招', '提供', '来一起玩吗', '独角兽', '补充', '无责', '想搞钱的你就来', '世界',
                 '看看' ]
    jieba_need = jieba.analyse.extract_tags(set_need, topK=80, withWeight=True)
    jieba_result = []
    for i in jieba_need:
        if i[0] not in stopwords:
            jieba_result.append(i)

    c = (
        WordCloud(init_opts=opts.InitOpts(theme=themes))
            .add("", jieba_result, word_size_range=[20, 100], shape=SymbolType.RECT)
            .set_global_opts(title_opts=opts.TitleOpts(title="福利待遇词云",
                                                       title_link='./chart/positionAdvantage.html',
                                                       title_target='blank',
                                                       pos_left='left',
                                                       ),
                             # 多功能组件
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             )
    )
    # c.render('./chart/positionAdvantage.html')
    # c.render_notebook()
    return c


if __name__ == '__main__':
    with open('前程无忧网招聘信息_清洗2.csv', 'r', encoding='UTF-8') as file:

        df = pd.read_csv(file)  # 读取csv

        # # 生成html
        # company_type_chart(df)    # 岗位中各类型企业占比图
        # company_size_chart(df)    # 岗位各公司规模占比图
        # background_chart(df)  # 岗位工作经验要求占比图
        # workarea_chart(df)  # 岗位各地区需求量
        # education_chart(df)     # 岗位各学历要求占比图
        # workarea_salary_chart(df)  # 岗位需求量排名前20地区的薪资水平状况
        # education_salary_chart(df)  # 各学历对应的平均工资水平(单位:千/月)
        # background_salary_chart(df)  # 各工作经验对应的平均薪资水平(单位:千/月)
        # field_chart(df)     # 企业领域统计
        # # data_show(df)       # 主要数据展示
        # #
        # setword1()
        # setword2()
        # setrose()

        # page = Page(layout=Page.DraggablePageLayout)
        # page.add(title(), data_show1(), data_show2(df), data_show3(), data_show4(df), company_type_chart(df), company_size_chart(df), background_chart(df), workarea_chart(df), education_chart(df), workarea_salary_chart(df), education_salary_chart(df), background_salary_chart(df), field_chart(df),  setword1(), setword2(), setrose())
        # page.render("test.html")
        # 格式化Page
        Page.save_resize_html("test.html",
                          cfg_file="chart_config.json",
                          dest="report.html",)

    with open("report.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'lxml')
        body = html_bf.find("body")
        body["style"] = "background-color:#333333;"     # 改变背景色
        html_new = str(html_bf)
        # print(html_bf)
        html.seek(0, 0)
        # file.seek()
        # 方法标准格式是：file.seek(offset, whence)
        # offset：开始的偏移量，也就是代表需要移动偏移的字节数
        # whence：给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。whence值为空没设置时会默认为0。
        html.truncate()     # 用于截断文件
        html.write(html_new)
        html.close()


