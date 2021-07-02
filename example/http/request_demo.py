import json
import codecs
import logging
import requests

LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# 获取 session_id
def get_session_id(username, password):
    url = "http://59.77.233.195/xingye2.0/Login/XyLogincheck.php"
    # 这种接口居然不需要设置 header
    # headers = {"Content-Type": "multipart/form-data; boundary=WebAppBoundary"}
    body = {}
    body['username'] = username
    body['password'] = password
    logging.info("请求 body: %s", body)
    ret = requests.post(url, data=body)
    result = ret.json()
    logging.info("结果: %s", result)
    if result['resultCode'] == 200:
        return result['data']
    else:
        logging.info("获取 session_id 失败: %s", result['message'])


# 查询_预警新闻
def query_yj_news(session_id, **kwargs):
    """
    :param session_id: session_id
    :param kwargs:
    searchsource:限选（1:门户网站,5:搜索引擎）
    searchkeyword:预警对象,模糊匹配
    searchpolar:限选(0:中性,1:正面,2:负面,3: 正面和负面）,默认为负面
    startdate:日期范围的开始时间,yyyy-mm-dd格式,默认检索1个月内的所有新闻
    enddate:日期范围的结束时间yyyy-mm-dd格式
    searchnum:返回条数,默认10
    :return: 结果
    """
    url = "http://59.77.233.195/xingye2.0/Report/XyRiskNew_ajax.php?"
    parms = []
    for parm_name, parm_value in items:
        parms.append("%s=%s" % (parm_name, parm_value))
    for parm in parms:
        if parms.index(parm) == 0:
            url = url + parm
        else:
            url = url + "&" + parm
    logging.info("拼接参数后url: %s", url)
    headers = {"Cookie": "%s" % session_id}
    logging.info("预警新闻请求headers: %s", headers)
    ret = requests.post(url, data=None, headers=headers)
    # ret = requests.request("POST", url, headers=headers)
    result = ret.json()
    logging.info("完整结果: %s", result)
    if result['resultCode'] == 200:
        logging.info("请求返回 message: %s", result['message'])
        return result['data']
    else:
        logging.info("获取 预警对象 失败: %s", result['message'])


if __name__ == '__main__':
    # session_id = "PHPSESSID=r0hb7ovluo9meij7eugr574156"
    session_id = get_session_id(username="xyzjjWarningnews", password="Fzuir@232056")
    logging.info("返回 session_id: %s", session_id)

    yjxw_result = query_yj_news(session_id, startdate="2021-05-01", searchkeyword="厦门至恒融兴", searchnum=3)
    logging.info("获取到预警新闻:\n %s", yjxw_result)
