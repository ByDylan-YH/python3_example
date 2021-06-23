# 安装依赖
# pip install -i https://mirrors.aliyun.com/pypi/simple/ mysql-connector
import mysql.connector;

mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="By960122",  # 数据库密码
    database="bingo"
);

print(mydb);

# 使用 cursor() 方法创建一个游标对象 cursor
mycursor = mydb.cursor();
mycursor.execute("show databases");

for x in mycursor:
    print(x);

# 插入数据
sql = 'insert into partition_list (id, dt) values (%s, %s);';
val = [('1', '201901'), ('2', '201902'), ('3', '201903')];
mycursor.executemany(sql, val);
mydb.commit();  # 数据表内容有更新，必须使用到该语句
# 发生错误时回滚
# mydb.rollback();
print(mycursor.rowcount, ",Success");

# 查询数据
mycursor.execute("select * from partition_list;")
myresult = mycursor.fetchall();     # fetchall() 获取所有记录

for x in myresult:
    print(x);

mycursor.execute("select * from partition_list;")
myresult = mycursor.fetchone(); #只读取一条数据
print(myresult);

# 关闭数据库连接
mydb.close();

