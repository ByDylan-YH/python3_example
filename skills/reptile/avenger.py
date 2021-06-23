# coding=utf-8

import os;
import requests;
import codecs;
from bs4 import BeautifulSoup;

# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'};

server = 'https://movie.douban.com/subject/26100958/comments';
# 定义存储位置
global save_path;
save_path = os.getcwd() + "\\doc\\" + '复仇者联盟4短评_差评.txt';
global page_max;
# 好评
page_max = 252;  # 500 短评论，后面就看不到了，不知道是否豆瓣有意而为之给隐藏了,哈哈哈原来是没登录导致的。
global comments;
comments = '';


# 获取短评内容
def get_comments(page):
    req = requests.get(url=page, headers=headers);  # 这里必须要写请求头
    html = req.content;
    html_doc = str(html, 'utf-8');
    bf = BeautifulSoup(html_doc, 'html.parser');
    # comment = bf.find_all(class_="short");
    comment = bf.find_all('span', class_="short");
    # print("爬取内容: ", comment);
    for short in comment:
        global comments;
        comments = comments + short.text;  # 会把头尾去掉 span class="short"


# 写入文件
def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code)as f:
        f.write(content);


# 主方法
def main():
    for i in range(0, page_max):
        try:
            page = server + '?start=' + str(i * 20) + '&limit=20&sort=new_score&status=P&percent_type=l';
            get_comments(page);
            write_txt(save_path, comments, 'utf8');
            print(comments);
        except Exception as e:
            print(e);


if __name__ == '__main__':
    main();
