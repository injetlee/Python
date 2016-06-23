import requests
from openpyxl import Workbook

def get_json(url, page, lang_name):
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i['companyShortName'])
        info.append(i['companyName'])
        info.append(i['salary'])
        info.append(i['city'])
        info.append(i['education'])
        info_list.append(info)
    return info_list


def main():
    lang_name = input('职位名：')
    page = 1
    url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    info_result = []
    while page < 31:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        page += 1
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    for row in info_result:
        ws1.append(row)
    wb.save('职位信息.xlsx')

if __name__ == '__main__':
    main()
