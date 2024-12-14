import json
from urllib.parse import quote, quote_plus

import requests
import hashlib

from dotenv import dotenv_values

from sql_util import find_no_gps_list, set_gps
from utils import get_env_path


def get_gps(addr):
    config = dotenv_values(get_env_path())
    # 服务地址
    host = "https://api.map.baidu.com"
    # 接口地址
    uri = "/geocoding/v3"
    # 此处填写你在控制台-应用管理-创建应用后获取的AK
    ak = config.get("AK")
    # 此处填写你在控制台-应用管理-创建应用时，校验方式选择sn校验后生成的SK
    sk = config.get("SK")
    # 设置您的请求参数
    params = {
        "address":    addr,
        "output":    "json",
        "ak":       ak,
    }
    # 拼接请求字符串
    paramsArr = []
    for key in params:
        paramsArr.append(key + "=" + params[key])

    queryStr = uri + "?" + "&".join(paramsArr)
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上您的SK
    rawStr = encodedStr + sk
    # 计算sn
    sn = hashlib.md5(quote_plus(rawStr).encode("utf8")).hexdigest()
    # 将sn参数添加到请求中
    queryStr = queryStr + "&sn=" + sn
    # 请注意，此处打印的url为非urlencode后的请求串
    # 如果将该请求串直接粘贴到浏览器中发起请求，由于浏览器会自动进行urlencode，会导致返回sn校验失败
    url = host + queryStr
    response = requests.get(url)
    if response:
        resp = response.json()
        if resp["status"] == 0:
            return resp["result"]
        else:
            return "{}"

def set_gps_for_rec():
    rec_list = find_no_gps_list()
    for record in rec_list:
        location = get_gps(record.location)
        print(f"record:{record.serial_id} , gps {location}")
        set_gps(record.serial_id, json.dumps(location))

