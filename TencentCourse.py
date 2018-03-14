from bs4 import BeautifulSoup
import json
import lxml
import requests

base_url = "https://ke.qq.com/course/list?mt="

agency_list = [] #机构列表
a_list = [] #机构课程数据列表
agency_sum_list = []



#获取所有机构
def getAgency():
    for mt in range(1001,1002):
        mt_url = base_url + str(mt)
        for page in range(1,34):
            dest_url = mt_url + "&page=" + str(page)
            response = requests.get(dest_url)
            soup = BeautifulSoup(response.content,'lxml')
            coures_market = soup.find('div',attrs={"class":"market-bd market-bd-6 course-list course-card-list-multi-wrap"})
            if coures_market:
                coures_list = coures_market.find_all("li",class_= "course-card-item")
                for item in coures_list:
                    agency_href = item.find("a",class_="item-source-link")
                    a_list.append(agency_href)
            else:
                print("no market")
    for item in a_list:
        agency_name = item["href"]
        if agency_name not in agency_list:
            agency_list.append(agency_name)
            print(agency_name)
            getAgencySumIncome(agencyName=agency_name)



def getAgencySumIncome(agencyName):
    agency_url = "https:"+agencyName+"/cgi-bin/agency_new/get_courses?count=30&page=0&category=-1&preview=0"
    headers = {
        'authorith' : 'dongnao.ke.qq.com' , 'referer' : 'https:'+agencyName
    }
    response = requests.get(agency_url,headers=headers)
    content = response.content
    json_content = str(content,'utf-8')
    coures_object = json.loads(json_content)
    coures_items = coures_object['result']['items']
    agency_price_sum = 0
    agencyCname = ""
    for cource_item in coures_items:
        cource_apply_num = cource_item['apply_num']
        coures_prince = cource_item['price']/100
        cource_sum_price = cource_apply_num * coures_prince
        agency_price_sum += cource_sum_price
        agencyCname = cource_item['agency_name']
    agency = (agencyCname,agency_price_sum)
    agency_sum_list.append(agency)




if __name__ == "__main__":
    getAgency()
    agency_sum_list = sorted(agency_sum_list,key=lambda  x:x[1],reverse=True)
    print(agency_sum_list)