# pip3 install mysql-connector-python --allow-external mysql-connector-python
import mysql.connector


def query_mysql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def insert_mysql(sql, data=None):
    cursor = conn.cursor()
    if data is not None:
        cursor.executemany(sql, data)
    else:
        cursor.execute(sql)
    conn.commit()
    return cursor.rowcount


if __name__ == '__main__':
    # config = configparser.ConfigParser()
    # config.read('C:\\Workspace\\PycharmProjects\\python3_example\\xyzq\\jryqyj\\properties.ini')
    # conn = mysql.connector.connect(user=config.get('database', 'jdbc.username'),
    #                                password=config.get('database', 'jdbc.password'),
    #                                database=config.get('database', 'jdbc.database'))
    connect = mysql.connector.connect(user='root', password='By9216446o6', database='by_dylan')
    query_mysql('select issr from t_risk_monit_issr_info;')
    query_mysql("truncate table t_yj_news_middle;")
    # 批量插入,data 为list(tuple) 类型 [(),()]
    data = [(1, 2, 3), ('a', 'b', 'c')]
    insert_result = insert_mysql("insert into t_yj_news_middle(title,url,keywords) values (%s,%s,%s);", data)
