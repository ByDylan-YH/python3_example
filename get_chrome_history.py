import os
import shutil
import sqlite3

# 大家要改成自己的路径
APP_DATA_PATH = os.environ["LOCALAPPDATA"]
DB_PATH = r'Google\Chrome\User Data\Default\History'

_full_path = os.path.join(APP_DATA_PATH, DB_PATH)
_tmp_file = os.path.join(os.environ['LOCALAPPDATA'], 'sqlite_file')
if os.path.exists(_tmp_file):
    os.remove(_tmp_file)
shutil.copyfile(_full_path, _tmp_file)

# 1.连接history_db
c = sqlite3.connect(_full_path)
cursor = c.cursor()

# 2.选取我们想要的网址和访问时间
try:
    select_statement = "SELECT url,datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime') AS tm FROM urls WHERE julianday('now') - julianday(tm) < 1 ORDER BY tm"
    cursor.execute(select_statement)
except sqlite3.OperationalError:
    print("[!] The database is locked! Please exit Chrome and run the script again.")
    quit()

# 3.将网址和访问时间存入 records.txt文件
results = cursor.fetchall()

# with open('D:\\WorkSpace\\PycharmProjects\\python_example\\skills\\chrom_records\\records.txt', 'w') as f:  # 改成自己的路径
for i in range(len(results)):
    print(results[i][1] + '\t' + results[i][0])
    # f.write(results[i][1] + '\t' + results[i][0] + '\n')
