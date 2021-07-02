import sys
import configparser


# 读取 .ini 配置文件
def get_ini_config(config_path, title, head):
    # 生成config对象
    cfg = configparser.ConfigParser()
    # 用config对象读取配置文件
    cfg.read(config_path)
    return cfg.get(title, head)


if __name__ == '__main__':
    get_ini_config(sys.path[0] + "config.ini", 'dbsybase', 'user')
