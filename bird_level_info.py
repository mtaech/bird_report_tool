import json

import requests

from sql_util import save_animal_info


# 获取鸟类等级信息
def get_bird_level_info(page_no):
    url = "http://www.especies.cn/v1/col/checklist/specieslist/page"
    # 每页100条
    data = {
        "ckListId": "001",
        "size": 100,
        "number": page_no,
        "sortType": "asc",
        "fields": ["infrasp", "species"]
    }
    # header 必要
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": "e7843921-602f-4ed1-9e8e-04672132ebe9",
        "Referer": "http://www.especies.cn/specialTopic/details/e184c17f-61b8-4d88-a2ca-8bd50b44d9ea",
        "Cookie": "JSESSIONID=5285343DEB7EE56A9805563204E58881",
        "Connection":"keep-alive"
    }
    response = requests.post(url, json=data,headers=headers)

    data_dict = json.loads(response.text)
    data_contents  = data_dict['data']['content']
    # //保存数据
    save_animal_info(data_contents)
    # 还有下一页时递归查询
    if not data_dict['data']['last']:
        page_no = page_no + 1
        get_bird_level_info(page_no)



if __name__ == '__main__':
    get_bird_level_info(0)