from bs4 import BeautifulSoup
import requests,re,threading

base_url = "https://ke.qq.com/course/list/"
def getCourseNum(jobName):
    course_all_num = 0
    for page in range(1,35):
        job_url = base_url+str(jobName)+"?page="+str(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'referer': 'https:' + job_url
        }
        response = requests.get(job_url,headers=headers).content
        soup = BeautifulSoup(response,"lxml")
        course_li = soup.find_all("div",class_="item-line item-line--middle")
        if course_li == []:
            break
        else:
            course_page_num = 0
            for item in course_li:
                course_context = item.find("span",class_="line-cell item-user").get_text();
                course_num = re.search("[0-9]+",str(course_context)).group()
                course_page_num += int(course_num)
            course_all_num += course_page_num
    print(jobName +":" +str(course_all_num))



if  __name__ == "__main__":
    threads = []
    # getCourseNum("go")
    java = threading.Thread(getCourseNum("java"))
    python = threading.Thread(getCourseNum("python"))
    go = threading.Thread(getCourseNum("go"))
    c = threading.Thread(getCourseNum("c"))
    php = threading.Thread(getCourseNum("php"))
    threads.append(java)
    threads.append(python)
    threads.append(go)
    threads.append(c)
    threads.append(php)
    for thread in threads:
        thread.start