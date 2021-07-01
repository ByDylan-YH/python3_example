import pymysql
from faker import Faker

# faker 插入测试数据
conn = pymysql.connect(host="114.215.129.166", port=3306, user="nice", password="", db="flask201",
                       charset="utf8")

cursor = conn.cursor()
sql1 = "drop table if exists faker_user"
sql2 = """
create table faker_user(
pid int primary key auto_increment,
username varchar(20),
password varchar(20),
address varchar(35) 
)
"""
cursor.execute(sql1)
cursor.execute(sql2)
fake = Faker("zh-CN")
for i in range(20):
    sql = """insert into faker_user(username,password,address) 
    values('%s','%s','%s')""" % (fake.name(), fake.password(special_chars=False), fake.address())
    print('姓名:' + fake.name() + '|密码:' + fake.password(special_chars=False) + '|地址:' + fake.address())
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
