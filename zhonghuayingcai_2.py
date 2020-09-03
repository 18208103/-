# 引入库
import requests
from bs4 import BeautifulSoup
import time
import re
import csv
import json

# 爬取中华英才网的职位信息
def reptilesZhongHua():
    # 网站的user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    # 利用for循环翻页
    for i in range(1,170):
        # requests请求网站
        link = "http://campus.chinahr.com/qz/P" + str(i) + "/?job_type=10&"
        r = requests.get(link, headers=headers, timeout=20)

        # 用BeautifulSoup解析网页
        soup = BeautifulSoup(r.text, "lxml")

        # 用BeautifulSoup找到信息
        salary_list = soup.find_all('strong', class_='job-salary')  # 工资
        city_list = soup.find_all('span', class_="job-city Fellip")  # 城市
        top_list = soup.find_all('div', class_="top-area")  # 名称和公司
        company_list = soup.find_all('span', class_="company-name")  # 公司
        job_info = soup.find_all('div', class_='job-info')  # 城市，学历和人数
        bottom_list = soup.find_all('div', class_="bottom-area")  # 网申时间
        type_list = soup.find_all('span', class_='industry-name')  # 类别

        # print(salary_list,city_list,top_list,job_info,type_list)

        # for循环每一个工作
        for x in range(len(top_list)):
            # 用strip()来提取信息,去除字符串两边的空格
            salary = salary_list[x].text.strip()  # 工资
            city = city_list[x].text.strip()  # 城市
            top = top_list[x].text.strip()  # 名称和公司
            company = company_list[x].text.strip()   #公司
            job_and_company = top.split('\n', 1)  # 分开名称和公司
            bottom = bottom_list[x].text.strip()  # 网申时间名词和时间
            # print(bottom)
            online_application_time = bottom.split('\n') #分开网申时间名词和时间
            job_information = job_info[x].text.strip()  # 城市，学历和人数
            city_to_people = job_information.split('\n')  # 分开城市，学历和人数
            type = type_list[x].text.strip()  # 职位类别

            # print(city_to_people)

            # 插入字典
            data = {"job": job_and_company[0],
                   "company": company,
                   "salary": salary,
                   "city": city,
                   "type": type,
                    "time":online_application_time[1]}

            # print("=====1=====")
            # print(data)

            # 用for循环分开城市，学历和人数
            for ans in range(3, 5):

                # 用re正则表达式
                first = re.compile(r' ')  # compile构造去掉空格的正则
                time_for_sub = first.sub('', city_to_people[ans])  # 把空格替换为没有，等于去掉空格
                another = re.compile(r'/')  # compile构造去掉/的正则
                the_middle_info = another.sub('', time_for_sub)  # 把/替换为空格，等于去掉/
                more = re.compile(r'\r')  # compile构造去掉\r的正则
                the_final_info = more.sub('', the_middle_info)  # 把/替换为空格，等于去掉\r

                # 得到学历并插入字典
                if ans == 3:
                    data['background'] = the_final_info

                # 得到人数并插入字典
                if ans == 4:
                    data['people'] = the_final_info

            # print("=====2=====")
            #输出信息确认
            print(data)
            #存入csv文件
            add_csv(data)

        # 每爬取5页休息三秒，模拟真人
        if i % 5 == 0:
            print("第%s页爬取完毕，休息三秒" % (i))
            print('the %s page is finished,rest for three seconds' % (i))
            time.sleep(3)

        # 每爬取1页休息一秒，模拟真人
        else:
            print("第%s页爬取完毕，休息一秒" % (i))
            print('the %s page is finished,rest for one second' % (i))
            time.sleep(1)


# 爬取前程无忧网的职位信息
def reptilesQianCheng():
    # 网站的user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    # 利用for循环翻页
    for i in range(1,3):
        # requests请求网站
        link = "https://search.51job.com/list/000000,000000,0000,00,9,99,+,1," + str(i) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        r = requests.get(link, headers=headers, timeout=20)

        # 用BeautifulSoup解析网页
        soup = BeautifulSoup(r.text, "lxml")

        titles = soup.select("body")
        print(titles)
        # 用BeautifulSoup找到信息
        # job_list = json.loads(soup.find('script', {'type': 'text/javascript'}).get_text())
  # 职位名称
        # job_list = soup.find_all('span', class_='jname at')  # 职位名称
        # time_list = soup.find_all('span', class_='time')  # 发布时间
        # salary_list = soup.find_all('span', class_='sal')  # 工资
        # city_experience_education_people_list = soup.find_all('span', class_="d at")  # 城市 工作经验 学历 人数
        # company_list = soup.find_all('a', class_="cname at")  # 公司
        # company_message_info = soup.find_all('p', class_='dc at')  # 公司类型 公司规模
        # type_list = soup.find_all('p', class_="int at")  # 职位类别

        # print(job_list)
        # print(time_list)
        # print(city_experience_education_people_list)
        # print(company_message_info)

        # # for循环每一个工作
        # for x in range(len(job_list)):
        #     # 用strip()来提取信息,去除字符串两边的空格
        #     job = job_list[x].text.strip()  # 职位名称
        #     date = time_list[x].text.strip()  # 发布时间
        #     salary = salary_list[x].text.strip()  # 工资
        #     company = company_list[x].text.strip()   #公司
        #     # job_and_company = top.split('\n', 1)  # 分开名称和公司
        #     # bottom = bottom_list[x].text.strip()  # 网申时间名词和时间
        #     # # print(bottom)
        #     # online_application_time = bottom.split('\n') #分开网申时间名词和时间
        #     # job_information = job_info[x].text.strip()  # 城市，学历和人数
        #     # city_to_people = job_information.split('\n')  # 分开城市，学历和人数
        #     type = type_list[x].text.strip()  # 类别

            # print(city_to_people)

            # 插入字典
            # data = {"job": job,
            #        "company": company,
            #        "salary": salary,
            #        "city": city,
            #        "type": type,
            #         "time":online_application_time[1]}

            # print("=====1=====")
            # print(data)

            # # 用for循环分开城市，学历和人数
            # for ans in range(3, 5):
            #
            #     # 用re正则表达式
            #     first = re.compile(r' ')  # compile构造去掉空格的正则
            #     time_for_sub = first.sub('', city_to_people[ans])  # 把空格替换为没有，等于去掉空格
            #     another = re.compile(r'/')  # compile构造去掉/的正则
            #     the_middle_info = another.sub('', time_for_sub)  # 把/替换为空格，等于去掉/
            #     more = re.compile(r'\r')  # compile构造去掉\r的正则
            #     the_final_info = more.sub('', the_middle_info)  # 把/替换为空格，等于去掉\r
            #
            #     # 得到学历并插入字典
            #     if ans == 3:
            #         data['background'] = the_final_info
            #
            #     # 得到人数并插入字典
            #     if ans == 4:
            #         data['people'] = the_final_info
            #
            # # print("=====2=====")
            # #输出信息确认
            # print(data)
            # #存入csv文件
            # add_csv(data)

        # 每爬取5页休息三秒，模拟真人
        if i % 5 == 0:
            print("第%s页爬取完毕，休息三秒" % (i))
            print('the %s page is finished,rest for three seconds' % (i))
            time.sleep(3)

        # 每爬取1页休息一秒，模拟真人
        else:
            print("第%s页爬取完毕，休息一秒" % (i))
            print('the %s page is finished,rest for one second' % (i))
            time.sleep(1)

def create_csv():
    csv_head = ['job', 'company', 'salary', 'city', 'type', 'time', 'background','people']
    with open('中华英才网招聘信息.csv', 'w',newline="",encoding='utf-8') as f:
        csv_write = csv.DictWriter(f, fieldnames=csv_head)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        #csv_write.writerow(csv_head)
        csv_write.writeheader()

def add_csv(data):
    path = "中华英才网招聘信息.csv"
    with open(path, 'a+',newline="") as fd:
        w = csv.DictWriter(fd, data.keys())
        w.writerow(data)

def main():

    # 创建csv文件
    create_csv()

    # 爬取中华英才网的职位信息
    reptilesZhongHua()
    #
    # # 爬取前程无忧网的职位信息
    # reptilesQianCheng()

if __name__ == '__main__':
    main()

