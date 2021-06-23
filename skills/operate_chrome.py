# coding=utf8

from selenium import webdriver


# 前台开启浏览器模式
def openChrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    # 关闭“chrome正受到自动测试软件的控制”
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('disable-infobars')
    # 不自动关闭浏览器
    option.add_experimental_option("detach", True)
    # adblock插件的路径：版本不支持crx
    option.add_extension('D:\\WorkSpace\\PycharmProjects\\python_example\\adblock.crx')
    # 使用自己的数据路径，防止data::窗口出现
    option.add_argument("--user-data-dir=C:/Users/BYDylan/AppData/Local/Google/Chrome/User Data/Default")
    # 打开chrome浏览器
    driver =webdriver.Chrome(executable_path="D:\\WorkSpace\\PycharmProjects\\python_example\\chromedriver.exe",chrome_options=option)
    return driver

if __name__ == '__main__':
    driver = openChrome()
    driver.get("www.baidu.com")
    driver.maximize_window()