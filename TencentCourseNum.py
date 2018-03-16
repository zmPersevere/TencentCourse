from bs4 import BeautifulSoup
import requests,re,threading

base_url = "https://ke.qq.com/course/list?mt=1001&st=2002&tt="


def getCourseNum():
    job_name_count = 0
    for tt in range(3005,3020):
        job_name_count = job_name_count+1
        course_all_num = 0
        tt_url = base_url+str(tt)+"&task_filter=0000000&&page="
        for page in range(1,35):
            job_url = tt_url+str(page)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                'referer': 'https:' + job_url
            }
            response = requests.get(job_url,headers=headers).content
            soup = BeautifulSoup(response,"lxml")
            jobName_list = soup.find_all("dd")
            jobName = jobName_list[job_name_count].find("a")["title"]
            # jobName = soup.find("a",href_="/course/list?mt=1001&st=2002&tt="+str(tt)).get_text()
            courese_all = soup.find("div",class_="market-bd market-bd-6 course-list course-card-list-multi-wrap")
            course_li = courese_all.find_all("div",class_="item-line item-line--middle")
            if course_li == []:
                break
            else:
                course_page_num = 0
                for item in course_li:
                    course_context = item.find("span",class_="line-cell item-user").get_text()
                    course_num = re.search("[0-9]+",str(course_context)).group()
                    course_page_num += int(course_num)
                course_all_num += course_page_num
        print(jobName +":" +str(course_all_num))



if  __name__ == "__main__":
    getCourseNum()
