import re
import requests
from bs4 import BeautifulSoup

base_url = "http://www.kgc.cn"
index_url = 'http://www.kgc.cn/list/230-1-6-9-9-0.shtml'
course_category = []

def courseCategory():
    response = requests.get(index_url)
    soup = BeautifulSoup(response.content,"lxml")
    category_div = soup.find_all("div",class_="new-courseHref")[1]
    category_list = category_div.find_all("a",class_="")
    for item in category_list:
        courseCategory_url = item["href"]#分类url
        courseCategory_name = item.get_text()
        getCategoryNum(courseCategory_name,courseCategory_url)


def getCategoryNum(courseCategory_name,category_url):
    course_all_num = 0
    for page in range(1,10):
        response = requests.get(base_url+category_url.replace("1",str(page)))
        soup = BeautifulSoup(response.content,"lxml")
        course_ul = soup.find("ul",class_="fix list-ul")
        if course_ul.find("span").get_text() == "没有找到数据." :
            break
        course_list = course_ul.find_all("li",class_="course_detail")
        course_page_num = 0
        for item in course_list:
            course_num = int(item.find("span",class_="course-pepo").get_text())
            course_page_num += course_num
        course_all_num += course_page_num
    course_category.append((courseCategory_name, course_all_num))




if  __name__ == "__main__":
    courseCategory()
    course_category = sorted(course_category,key=lambda x:x[1],reverse=True)
    print(course_category)
