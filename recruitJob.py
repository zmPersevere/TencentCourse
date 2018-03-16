from bs4 import BeautifulSoup
import re,random,threading,requests,time

base_url = "https://www.zhipin.com/job_detail/?query="
https_ip_pool = []
http_ip_pool = []

def getJob(jobName,proxies):
    job_context = []
    for page in range(1,11):
        time.sleep(3)
        job_url = base_url + jobName + "&page=" + str(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.get(job_url,headers=headers).content
        soup = BeautifulSoup(response,"lxml")
        job_list = soup.find_all("div",class_="info-primary")
        for item in job_list:
            job_price = re.findall(r'\d+',item.find("span",class_="red").get_text())
            #获取平均工资
            aug_price = (int(job_price[0]) + int(job_price[1])) / 2
            #获取工作年限
            job_year = re.search('[0-9]-[0-9]+年', str(item.find_all("p")[1]))
            if job_year == None :
                job_year = "工作年限不限"
            else:
                job_year = job_year.group()
            if re.search(str(job_year),str(job_context)):
                for job_list in job_context:
                    if re.search(str(job_year),str(job_list)):
                        job_list[1] += aug_price
                        job_list[2] += 1
            else:
                job_context.append([str(job_year),aug_price,1])
    for item in job_context :
        item[1] = item[1]/item[2]
    print(jobName+":"+str(job_context))


def getIp():
    for page in range(20,21):
        print(page)
        url = 'http://www.xicidaili.com/nn/'+str(page)
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        proxies = {
            "http":"218.26.170.189:61202"
        }
        response = requests.get(url, headers=headers,proxies=proxies)
        soup = BeautifulSoup(response.content,"lxml")
        ip_tr_list = soup.find_all("tr",class_="odd")
        for item in ip_tr_list:
            td_list = item.find_all("td")
            can_ip = td_list[1].get_text()
            can_type = td_list[5].get_text()
            ip_port = td_list[2].get_text()
            if str(can_type) == "HTTPS" :
                complete_ip = str(can_ip) + ":" +ip_port
                https_ip_pool.append(complete_ip)
            if str(can_type) == "HTTP" :
                complete_ip = str(can_ip) + ":" +ip_port
                http_ip_pool.append(complete_ip)

# def test_proxies(jobName,proxies):
#     try:
#         job_url = base_url + jobName + "&page=" + str(1)
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
#         }
#         response = requests.get(job_url, headers=headers, proxies=proxies,timeout=1)
#         if response.status_code == 200:
#             with open("/Users/zhangming/proxies.txt","w") as f:
#                 f.write(proxies)
#     except:
#         print('请求过程错误' )
#         return False


if  __name__ == "__main__":
    getIp()
    proxy_https_ip = random.choice(https_ip_pool)
    proxy_http_ip = random.choice(http_ip_pool)
    proxies = {'https': proxy_https_ip, 'http': proxy_http_ip}
    #随机获取一个可用ip
    # for i in range(1,10000):
    #     print(https_ip_pool)

    #     threads = []
        # a = threading.Thread(test_proxies("java", proxies))
        # b = threading.Thread(test_proxies("java", proxies))
        # c = threading.Thread(test_proxies("java", proxies))
        # d = threading.Thread(test_proxies("java", proxies))
        # for thread in threads:
        #     print("14")
        #     thread.start
    #     print("1")
    #     thread.start
    # getJob("java", proxies)
    # proxies = {'https': "",'http': ""}
    threads = []
    java_thread = threading.Thread(getJob("java",proxies))
    python_thread = threading.Thread(getJob("python", proxies))
    php_thread = threading.Thread(getJob("php", proxies))
    c_thread = threading.Thread(getJob("c", proxies))
    threads.append(java_thread)
    threads.append(python_thread)
    threads.append(php_thread)
    threads.append(php_thread)   
    for thread in threads:
        thread.start

