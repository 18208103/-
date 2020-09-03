import pandas
import requests
from lxml import etree
import json
import re
import time

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.48 Safari/537.36 Edg/85.0.564.23'
}


# 爬取一整页
# page_index决定是否写列名，存储文件方式
def get_onepage(url, page_index):
    res = requests.get(url, headers=header)
    print(res)

    # 用XPATH选择出所需标签
    selector = etree.HTML(res.text)
    result = selector.xpath('//script[@type="text/javascript"]/text()')

    # 提取出JSON
    js_str = re.search('\{.*}', str(result[0]))  # 字符串类型
    js_dict = json.loads(js_str.group())  # 字典类型
    job = js_dict['engine_search_result']  # list类型,job[0]为dict类型

    dict_job = {}   # 存储所有信息
    job_name = []   # 职位名称
    company_name = []   # 公司名称
    workarea_text = []  # 地区
    providesalary_text = []     # 薪资
    background = []   # 工作经验要求
    education = []  # 学历要求
    recruiters_number = []  # 招聘人数
    companytype_text = []   # 公司性质
    companysize_text = []   # 公司规模
    companyind_text = []    #  公司类别/工作领域
    issuedate = []   # 发布时间

    for i in range(len(job)):
        job_name.append(job[i]['job_name'])
        company_name.append(job[i]['company_name'])
        workarea_text.append(job[i]['workarea_text'])
        providesalary_text.append(job[i]['providesalary_text'])
        attribute_text = job[i]['attribute_text']
        # print(attribute_text,len(attribute_text))
        background.append(attribute_text[1])

        # 有的数据没有学历要求或经验要求
        if len(attribute_text) == 4:
            education.append(attribute_text[2])
            recruiters_number.append(attribute_text[3])
        elif len(attribute_text) == 3:
            education.append('')
            recruiters_number.append(attribute_text[2])
        else:
            education.append('')
            recruiters_number.append('')

        companytype_text.append(job[i]['companytype_text'])
        companysize_text.append(job[i]['companysize_text'])
        companyind_text.append(job[i]['companyind_text'])
        issuedate.append(job[i]['updatedate'])

    dict_job['name'] = job_name
    dict_job['company'] = company_name
    dict_job['workarea'] = workarea_text
    dict_job['salary'] = providesalary_text
    dict_job['background'] = background
    dict_job['education'] = education
    dict_job['recruiters_number'] = recruiters_number
    dict_job['company_type'] = companytype_text
    dict_job['company_size'] = companysize_text
    dict_job['field'] = companyind_text
    dict_job['issuedate'] = issuedate

    df = pandas.DataFrame(dict_job)
    print(df)
    if page_index == 1:
        df.to_csv('前程无忧网招聘信息.csv', index=None, header=True, encoding='utf_8_sig')
    else:
        df.to_csv('前程无忧网招聘信息.csv', mode='a', index=None, header=False, encoding='utf_8_sig')

    # 每爬取5页休息三秒，模拟真人
    if page_index % 5 == 0:
        print("第%s页爬取完毕，休息三秒" % (page_index))
        time.sleep(3)

    # 每爬取1页休息一秒，模拟真人
    else:
        print("第%s页爬取完毕，休息一秒" % (page_index))
        time.sleep(1)


if __name__ == '__main__':
    for p in range(1, 2000):
        url = "https://search.51job.com/list/000000,000000,0000,00,9,99,+,1," + str(p) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        get_onepage(url, p)

