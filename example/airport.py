# coding=utf-8
# 导入requests库
import requests;
from bs4 import BeautifulSoup;
import re;
import mysql.connector;
import time;
import functools;

mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="By960122",  # 数据库密码
    database="bingo"
);

# 给请求指定一个请求头来模拟chrome浏览器,地址栏中输入  about:version
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'};
# 网址
addr = 'http://airport.anseo.cn';


# 计时器
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        t0 = time.time();
        func(*args, **kwds);
        t1 = time.time();
        logger.info('%s 执行耗时 %0.3f s, 约 %s 分钟' % (func.__name__, t1 - t0, round((t1 - t0) / 60)))

    return wrapper;


# 获取所有国家
def get_region(addr):
    res = requests.get(addr, headers=headers);
    html = res.content;
    html_doc = str(html, 'utf8');
    # 使用自带的html.parser解析,获取首页
    homepage = BeautifulSoup(html_doc, 'html.parser');
    # print(homepage);
    # 获取所有国家
    return homepage.find('div', id='regions-list-c').find_all('a');


# 获取每个国家有多少页
def get_pages(addr):
    req = requests.get(url=addr);
    html = req.content;
    html_doc = str(html, 'utf8');
    bf = BeautifulSoup(html_doc, 'html.parser');
    try:
        texts = bf.find('div', class_="page-control").find_all('a');
        lastpage_addr = texts[len(texts) - 1].get('href');
        # print(lastpage_addr);
        page = int(re.compile(r"\d+").findall(lastpage_addr)[0]);
    except Exception as e:
        page = 1;
    return page;


# 获取每一页的机场信息
def get_airport(addr):
    req = requests.get(url=addr);
    html = req.content;
    html_doc = str(html, 'utf8');
    bf = BeautifulSoup(html_doc, 'html.parser');
    try:
        # 机场信息全在td标签内
        texts = bf.find_all('td');
        # print(len(texts));  # 120   4个一组
        airport_list = [];
        detail_list = [];
        # 获取所有标签的内容,存入列表,此时已区分不出国家
        for text in texts:
            # print(text);
            # print(text.get_text().strip().replace("\t", "").replace("\n", "|"));
            detail_list.append(text.get_text().strip().replace("\t", "").replace("\n", "|"));
            # print(text.a.string);
            # print('\n');

        # 按网站格式,每4个切分为一组,分别代表国家,机场,三字码,四字码
        for i in range(0, len(detail_list), 4):
            airport_dict = {};
            airport_dict['city'], airport_dict['airport'], airport_dict['three_character_code'], airport_dict[
                'four_character_code'] = detail_list[i:i + 4];
            airport_list.append(airport_dict);
    except Exception as e:
        pass;
    return airport_list;


def segmentation_name(name):
    name1 = '';
    if not '|' in name:
        aa = list(name);
        aa.insert(0, '|');
        name1 = ''.join(aa);
    else:
        name1 = name;
    result = {};
    result['chinese_name'], result['english_name'] = name1.split('|');
    # print('%s : %s' % (result['chinese_name'], result['english_name']));
    return result;


# 写入数据库
def write_mysql(region, airportdetail_list):
    sql = 'insert into airport values (%s,%s,%s,%s,%s,%s,%s,%s);';
    region_english_rule = re.compile(r'[(](.*?)[)]', re.S);
    insert_list = [];
    for airport_detail in airportdetail_list:
        detail_list = [];
        # print(airport_detail);
        city = segmentation_name(airport_detail['city']);
        airport = segmentation_name(airport_detail['airport']);
        detail_list.append(''.join(re.sub(region_english_rule, '',region)));
        detail_list.append(''.join(re.findall(region_english_rule, region)));
        detail_list.append(city['chinese_name']);
        detail_list.append(city['english_name']);
        detail_list.append(airport['chinese_name']);
        detail_list.append(airport['english_name']);
        detail_list.append(airport_detail['three_character_code']);
        detail_list.append(airport_detail['four_character_code']);
        insert_list.append(detail_list);
    # print(insert_list);
    mycursor = mydb.cursor();
    mycursor.executemany(sql, insert_list);
    mydb.commit();
    # print(mycursor.rowcount, ",Success");
    print('成功写入数据库: %s 行' % mycursor.rowcount);


# 主方法
@timer
def main():
    mycursor = mydb.cursor();
    mycursor.execute("truncate table airport;");
    # 获取所有国家
    regionslist = get_region(addr);
    region_size = len(regionslist);
    print('共有: %d 个国家' % region_size);
    # 遍历每一个国家,第一层获取有多少页
    for region in regionslist:
        # print(region.get('href') + " : " + region.get('title'));
        try:
            chapter = addr + region.get('href');
            pages = get_pages(chapter);
            print('%s 有 %d 页' % (region.get('title'), pages));
            # 第二层遍历每一页拿到机场信息
            for index in range(1, pages + 1):
                page_addr = chapter + "__page-" + str(index);
                print(region.get('title') + " : " + page_addr);
                airportdetail_list = get_airport(page_addr);
                print(airportdetail_list);
                write_mysql(region.get('title'), airportdetail_list);
        except Exception as e:
            print(e);
        region_size -= 1;


if __name__ == '__main__':
    # addr = 'http://airport.anseo.cn/c-thailand__page-1';
    # get_airport(addr);
    # airportdetail_list = [];
    # write_mysql('洪都拉斯（Honduras）', airportdetail_list);
    # city = '北京|Beijing';
    # segmentation_name(city);
    # region = '中国(China)';
    # p1 = re.compile(r'[(](.*?)[)]', re.S);
    # print(type(''.join(re.findall(p1, region))));
    # print(re.sub(p1, '',region));
    main();
