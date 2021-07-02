# python3
# author lizm
# datetime 2020-16-22 10:00:00
# -*- coding: utf-8 -*-
'''
    bi:http://10.25.103.21:8080/XYBI/decision
'''

from splinter.browser import Browser
import requests
from bs4 import BeautifulSoup
import datetime
import time
import sys
import logging
import configparser
from selenium import webdriver
import traceback
from time import sleep
from urllib import request, parse
import urllib
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger()
#set loghandler
file = logging.FileHandler(sys.path[0]+"\\bi_log"+time.strftime("%Y%m%d")+".log")
logger.addHandler(file)
#set formater
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file.setFormatter(formatter) 
#set log level
logger.setLevel(logging.NOTSET)

def dbconfig():
	#生成config对象
	cfg = configparser.ConfigParser()
	#用config对象读取配置文件
	path_ = sys.path[0]
	cfg.read(path_+"\\dbconfig.ini", encoding="utf-8-sig")
	bi_url = cfg.get("dblogin", "bi_url")
	userName = cfg.get("dblogin", "userName")
	pwd = cfg.get("dblogin", "pwd")
	mlmc = cfg.get("dblogin", "mlmc")
	mlmc_second = cfg.get("dblogin", "mlmc_second")
	bbmc = cfg.get("dblogin", "bbmc")
	return (bi_url,userName,pwd,mlmc,mlmc_second,bbmc)


# 前台开启浏览器模式
def openChrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    #关闭“chrome正受到自动测试软件的控制”
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 不自动关闭浏览器
    option.add_experimental_option("detach", True)
    # 打开chrome浏览器
    driver = webdriver.Chrome(chrome_options=option)
    return driver

#模拟登陆操作
def bi_login(count):
	logger.info(u"开始执行")
	print(time.strftime("%Y-%m-%d %H:%M:%S") + u" 开始执行")
	mlmc = dbconfig()[3]
	mlmc_second = dbconfig()[4]
	bbmc = dbconfig()[5]
	login_flag = False
	logger.info(u"打开浏览器")
	driver =  openChrome()
	logger.info(u"打开BI系统")
	driver.get(dbconfig()[0])
	driver.maximize_window() 
	#解析
	logger.info(u"获取用户名和密码的控件")
	account =driver.find_elements_by_tag_name('input')[0]
	account.send_keys(dbconfig()[1])
	pwd = driver.find_elements_by_tag_name('input')[1]
	pwd.send_keys(dbconfig()[2])
	#勾选自动登陆
	checkbox = driver.find_elements_by_xpath('//div[contains(@class, "bi-single") and contains(@class, "bi-basic-button") and contains(@class, "cursor-pointer") and contains(@class, "bi-multi-select-item") and contains(@class, "bi-flex-vertical-center-adapt-layout") and contains(@class, "v-middle h-left")]')[0]
	if checkbox is not None:
		checkbox.click()
	sleep(2)
	logger.info("点击登陆按钮")
	driver.find_element_by_class_name('login-button').click()
	logger.info(u"登陆BI")
	print(time.strftime("%Y-%m-%d %H:%M:%S") + u"登陆BI")
	sleep(10)
	try:
		logger.info(u"获取一级目录")
		bi_expanders = driver.find_elements_by_class_name('bi-expander')
		if bi_expanders is None:
			logger.info(u"登陆失败")
			print(time.strftime("%Y-%m-%d %H:%M:%S") + u" 登陆失败")
			login_flag = True
			driver.quit()
		else:
			logger.info(u"登陆成功")
			print(time.strftime("%Y-%m-%d %H:%M:%S") + u" 登陆成功")
			# 获取目录 - 财富管理部
			for bi_expander in bi_expanders:
				bi_text = bi_expander.find_elements_by_class_name('bi-text')[0]
				if(bi_text.text == mlmc):
					logger.info(u"点击一级目录:{0}".format(mlmc))
					bi_expander.click()
					break
			sleep(3)
			logger.info(u"获取二级目录:{0}".format(mlmc_second))
			ml_second_list = driver.find_elements_by_xpath('//div[contains(@class, "bi-expander") and contains(@class, "bi-vertical-layout")]')
			if ml_second_list is not None:
				for ml_second in ml_second_list:
					ml_second_text = ml_second.find_elements_by_class_name('bi-text')[0]
					if(ml_second_text.text == mlmc_second):
						logger.info(u"点击二级目录：{0}".format(mlmc_second))
						ml_second.click()
						break
			else:
				logger.info(u"获取二级目录异常")
				print(time.strftime("%Y-%m-%d %H:%M:%S") + u" 获取二级目录异常")
				login_flag = True
				driver.quit()

	except Exception as e:
		driver.quit()
		logger.info(u"登陆异常：%s" %e)
		print(time.strftime("%Y-%m-%d %H:%M:%S") + u" 登陆异常：%s" %e)
		sleep(5)
		bi_login(count)
		
		

if __name__ == "__main__":
	count = 1
	bi_login(count)
