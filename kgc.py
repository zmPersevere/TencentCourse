from bs4 import BeautifulSoup
import requests
import re


base_url = 'http://www.kgc.cn/list/230-'
course_all_list = []

#获取课程
def getCourse(page):
    print(page)
    response = requests.get(base_url+str(page)+"-6-9-9-0.shtml")
    soup = BeautifulSoup(response.content,'lxml')
    course_ul = soup.find("ul",class_="fix list-ul")
    course_li = course_ul.find_all("li",class_="course_detail")
    for item in course_li:
        #获取课程名称
        course_name = item.find("a",class_="yui3-u course-title-a")["alt"]
        #获取学习人数
        course_num = re.search("[0-9]+", str(item.find("span", class_="course-pepo"))).group()
        course_all_list.append((course_name,int(course_num)))

if  __name__ == "__main__":
    for page in range(1,64):
        getCourse(page)

    course_all_list = sorted(course_all_list,key=lambda x:x[1],reverse=True)
    print(course_all_list)