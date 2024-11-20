import base64
import json
import time

from loguru import logger
from playwright.sync_api import sync_playwright

from models import RecordDetail, BirdRecord
from sql_util import SqlUtils

BASE_URL = "https://www.birdreport.cn"


# 爬取明细
def save_detail_page(context, url, serial_id):
    page = context.new_page()
    page.goto(f"{BASE_URL}{url}")
    logger.info(f"进入页面：{BASE_URL}{url}")
    # 根据css找到明细表格 ，有概论在进入这个页面触发验证码反爬，所以手动输入验证码就行了
    page.wait_for_selector("div.layui-table-body > table.layui-table > tbody tr")
    elements = page.query_selector_all("div.layui-table-body > table.layui-table > tbody tr")
    # 遍历表格明细，保存进数据库
    for handle in elements:
        td_list = handle.query_selector_all("td")
        record = RecordDetail()
        for td in td_list:
            data_field = td.get_attribute("data-field")
            data_content = td.text_content()
            record.set_value(data_field, data_content)
        record.record_no = serial_id
        SqlUtils.insert_detail(record)
    page.close()



def save_data():
    with sync_playwright() as playwright:
        # 关闭无头模式，爬取过快的话会触发验证码，所以这里直接gui运行，手动过验证码
        browser = playwright.chromium.launch(headless=False)
        # open_page(browser)
        save_detail(browser)

def open_page(browser):
    page = browser.new_page()
    query = get_query()
    url = f"https://www.birdreport.cn/home/search/report.html?search={query}"
    page.goto(url)
    save_record(browser, page)

# 查询条件base64
def get_query():
    obj = {
        "taxonid": "",
        "startTime": "2024-11-01",
        "endTime": "2024-11-30",
        "province": "江西省",
        "city": "",
        "district": "",
        "pointname": "",
        "username": "",
        "serial_id": "",
        "ctime": "",
        "version": "CH4",
        "state": "",
        "mode": 0,
        "outside_type": 0
    }
    string = json.dumps(obj)
    return base64.b64encode(string.encode()).decode()

# 保存观鸟记录
def save_record( browser, page):
    page_handle = page.query_selector("span.layui-laypage-curr")
    if page_handle:
        page_idx = page_handle.text_content()
        print(f"当前页数：{page_idx}")

    # 确定表格位置
    page.wait_for_selector("div.layui-table-body > table.layui-table > tbody tr")
    elements = page.query_selector_all("div.layui-table-body > table.layui-table > tbody tr")
    # 开始爬取
    for handle in elements:
        td_list = handle.query_selector_all("td")
        record = BirdRecord()

        # 保存字段信息
        for td in td_list:
            data_field = td.get_attribute("data-field")
            data_content = td.text_content()
            record.set_value(data_field, data_content)

        # 获取明细页面连接
        url_handle = handle.query_selector("td[data-field='serial_id'] a")
        if url_handle:
            url = url_handle.get_attribute("href")
            record.url = url

        bird_record = SqlUtils.find_record(record.serial_id)
        if bird_record is None:
            SqlUtils.insert_record(record)
            logger.info(f"编号 {record.serial_id} 保存成功")
            if record.url is not None and len(record.url) > 0:
                time.sleep(2)

    # 本页保存结束，进入下一页保存
    if can_next(page):
        page.click("a.layui-laypage-next")
        time.sleep(2)
        save_record(browser, page)

# 判断还有没有下一页，下一页按钮不包含 layui-disabled 这个class 就是还有
def can_next(page):
    handle = page.query_selector("a.layui-laypage-next")
    if handle:
        class_name = handle.get_attribute("class")
        return not "layui-disabled" in class_name
    return False

# 保存明细
def save_detail( browser):
    context = browser.new_context()
    page = context.new_page()
    # 打开一个页面，防止关闭明细页面时同时关闭浏览器。造成资源浪费
    page.goto("https://bing.com")
    record_list = SqlUtils.find_not_done_records()
    if len(record_list) > 0:
        # 遍历未爬取明细的记录循环爬取
        for record in record_list:
            try:
                SqlUtils.delete_detail(record.serial_id)
                url = record.url
                if url is not None and len(url) > 0:
                    save_detail_page(context, url, record.serial_id)
                SqlUtils.set_done(record.serial_id)
                logger.info(f"编号 {record.serial_id} 数据搞定")
                # 爬取完停5秒，降低触发爬虫机制几率
                time.sleep(5)
            except Exception as e:
                print(e)
                logger.error(f"编号 {record.serial_id} 数据爬取出错", e)


if __name__ == "__main__":
    save_data()

