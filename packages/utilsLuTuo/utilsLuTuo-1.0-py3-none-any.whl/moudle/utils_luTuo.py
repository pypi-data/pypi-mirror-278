import configparser
import json
import os
import emoji
import time
import allure
import pymongo
import pymysql
import logging
import urllib.request
import sqlite3
import redis

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

root_dir = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件所在目录的上一级目录
configPath = os.path.join(root_dir, r"../../config/config.ini")
path = os.path.abspath(configPath)
cf = configparser.ConfigParser()
cf.read(path, encoding='utf-8')  # 拼接得到config.ini文件的路径，直接使用


@allure.feature("浏览器驱动")
class DriverTool:
    web_or_exe = cf.get("Data", "web_or_exe")
    app_exe = cf.get("Data", "app_exe")
    # 如果 是web 则进行纯web网页版自动化测试，否则进行web-electron框架的应用程序自动化测试
    if web_or_exe == "web":
        chrome_options = None
        driver = None

        @classmethod
        def get_driver(cls):

            if not cls.driver:  # 谷歌驱动+要进入的web页面
                cls.chrome_options = webdriver.ChromeOptions()
                myTools.step("忽略证书提示")
                cls.chrome_options.add_argument('--ignore-certificate-errors')
                myTools.step('忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 提示')
                cls.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                myTools.step('忽略 DevTools listening on ws://127.0.0.1... 提示')
                cls.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                cls.driver = webdriver.Chrome(executable_path=os.environ['chromedriver'], options=cls.chrome_options)
                myTools.step("窗口最大化")
                cls.driver.maximize_window()
                myTools.step("隐式等待")
                cls.driver.implicitly_wait(20)
                # 如果网络等原因加载等问题，可进入浏览器先刷新界面
                # cls._driver.refresh()
            return cls.driver
    else:  # 如果 是app 进行web-electron框架的应用程序自动化测试
        options = None
        driver = None

        @classmethod
        def get_driver(cls):
            if not cls.driver:
                cls.options = webdriver.ChromeOptions()
                myTools.step("忽略证书提示")
                cls.options.add_argument('--ignore-certificate-errors')
                cls.options.add_argument('--headless')
                myTools.step('忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 提示')
                cls.options.add_experimental_option('excludeSwitches', ['enable-automation'])
                myTools.step('忽略 DevTools listening on ws://127.0.0.1... 提示')
                cls.options.add_experimental_option('excludeSwitches', ['enable-logging'])
                myTools.step("exe的路径")
                cls.options.binary_location = os.path.abspath(cls.app_exe)
                cls.driver = webdriver.Chrome(executable_path="chromedriver_app", options=cls.options)
                myTools.step("隐式等待")
                cls.driver.implicitly_wait(20)

            return cls.driver


@allure.feature("项目中使用的所有方法")
class myTools:
    @classmethod
    @allure.title("单个元素定位")
    def find_element(cls, style, value):
        Log().info("\033[32m定位单个元素\033[0m")
        return DriverTool.get_driver().find_element(style, value)

    @classmethod
    @allure.title("多个元素定位")
    def find_elements(cls, style, value):
        Log().info("\033[32m定位多个元素\033[0m")
        return DriverTool.get_driver().find_elements(style, value)

    @classmethod
    @allure.title('关闭浏览器')
    def close_driver(cls):
        Log().info("\033[32m关闭浏览器\033[0m")
        if DriverTool.driver:
            DriverTool.driver.quit()
            DriverTool.driver = None

    @classmethod
    @allure.title('刷新浏览器')
    def refresh_action(cls):
        Log().info("\033[32m刷新浏览器\033[0m")
        DriverTool.get_driver().refresh()

    @classmethod
    @allure.title('模拟鼠标双击选中文本，然后输入内容')
    def mouse_action_select_input(cls, style, value, content):
        Log().info("\033[32m模拟鼠标双击输入内容: {}\033[0m".format(content))
        element = DriverTool.get_driver().find_element(style, value)
        ActionChains(DriverTool.get_driver()).double_click(element).perform()
        element.send_keys(content)

    @classmethod
    @allure.title("元素个数")
    def get_elements_number(cls, value):
        Log().info("\033[32m获取元素个数\033[0m")
        ele = DriverTool().get_driver().find_elements(By.XPATH, "{}".format(value))
        return len(ele)

    @classmethod
    @allure.title("获取多个元素中其中一个文本")
    def get_elements_single_text(cls, style, value, i):
        Log().info("\033[32m获取多个元素中其中一个文本\033[0m")
        ele = DriverTool.get_driver().find_elements(style, '{}'.format(value))[i]
        return ele.text

    @classmethod
    @allure.title("获取多个元素列表文本")
    def get_elements_list_text(cls, style, value):
        Log().info("\033[32m获取多个元素列表文本\033[0m")
        ele = DriverTool.get_driver().find_element(style, '{}'.format(value))
        return ele.text

    @classmethod
    @allure.title('数据驱动读取内容')
    def get_json_data(cls, file_path):
        cls.step("打开文件")
        file = open(file_path, encoding='utf-8')
        cls.step("读取文件")
        content = file.read()
        cls.step("将字符串还原成原始的列表或者字典")
        content_list = json.loads(content)
        data_list = []
        for item in content_list:
            data = tuple(item.values())
            data_list.append(data)
        return data_list

    @classmethod
    @allure.title('文件写的操作')
    def file_write(cls, file_path, handle, content):
        Log().info("\033[32m文件写的操作:{}\033[0m".format(content))
        with open(file_path, "{}".format(handle), encoding="utf-8") as f:
            if handle is "w":  # 只写 覆盖原有内容
                f.write(content)
            elif handle is "a":  # 在原有内容 后面追加
                f.write("{}{}".format(content, "\n"))

    @classmethod
    @allure.title('文件读的操作')
    def file_read(cls, file_path):
        Log().info("\033[32m文件读的操作\033[0m")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    @allure.title('获取断言内容')
    def get_assert_text(cls, style, value):
        # noinspection PyBroadException
        try:
            Log().info("\033[32m获取断言内容\033[0m")
            wait_obj = WebDriverWait(DriverTool.get_driver(), 5)
            tips = wait_obj.until(lambda x: x.find_element(by=style, value=value))
            return tips.text
        except Exception as e:
            Log().error("\033[1;31;40m get_assert_failed: {}\033[0m".format(value))
            return DriverTool.get_driver().get_screenshot_as_file(
                os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "获取断言内容失败")))

    @classmethod
    @allure.title('获取弹窗信息')
    def get_alter_msg(cls):
        # noinspection PyBroadException
        try:
            Log().info("\033[32m获取弹窗信息\033[0m")
            wait_obj = WebDriverWait(DriverTool.get_driver(), 2)
            alter_msg = wait_obj.until(lambda x: x.find_element(By.CLASS_NAME, 'el-message__content'))
            return alter_msg.text

        except Exception as e:
            Log().error("\033[1;31;40m get_alert_failed \033[0m")
            return DriverTool.get_driver().get_screenshot_as_file(
                os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "获取弹窗信息失败")))

    @classmethod
    @allure.title("获取当前页面标题")
    def get_title(cls):
        Log().info("\033[32m获取当前页面的title\033[0m")
        return DriverTool.get_driver().title

    @classmethod
    @allure.title("截图操作")
    def screen_shot(cls):
        Log().info("\033[32m截图操作\033[0m")
        return DriverTool.get_driver().get_screenshot_as_file(
            os.path.abspath("./Screenshot/{}-{}.png".format(time.strftime('%Y-%m-%d %Hh%Mmin%Ss'), "特意截图")))

    @classmethod
    @allure.title("输入值")
    def input_text(cls, style, value, content):
        Log().info("\033[32m输入值: {}\033[0m".format(content))
        element = DriverTool.get_driver().find_element(style, value)
        if element:
            element.clear()
            element.send_keys(content)
            time.sleep(0.5)
        else:
            Log().error("\033[1;34m input_failed:{}\033[0m".format(content))
            return DriverTool.get_driver().get_screenshot_as_file(
                os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "输入值失败")))

    @classmethod
    @allure.title("实现滚动条")
    def handler_scroll(cls, scrollHeight):
        Log().info("\033[32m实现滚动条\033[0m")
        # 这是实现滚动条拖动的js语句，scrollHeight拖动的数值 按实际情况填写(0:顶部 , 100000:底部)
        js = 'var q=document.documentElement.scrollTop={}'.format(scrollHeight)

        driver = DriverTool.get_driver()

        driver.execute_script(js)

    @classmethod
    @allure.title("操作步骤")
    def step(cls, name, *args):
        with allure.step(name):
            return None

    @classmethod
    @allure.title('切换页面操作句柄')
    def switch_operation_handle(cls, num):
        Log().info("\033[32m切换页面操作句柄:{}\033[0m".format(num))
        # noinspection PyBroadException
        try:
            driver = DriverTool.get_driver()
            driver.switch_to.window(driver.window_handles[num])
        except Exception as e:
            Log().error("\033[1;34m 切换操作句柄失败\033[0m")

    @classmethod
    @allure.title('获取操作句柄个数')
    def get_window_handles_num(cls):
        Log().info("\033[32m获取操作句柄个数\033[0m")
        # noinspection PyBroadException
        try:
            num = len(DriverTool.get_driver().window_handles)
            print("操作句柄个数: ", num)
            return num
        except Exception as e:
            Log().error("\033[1;34m 获取操作句柄个数失败\033[0m")

    @classmethod
    @allure.title('别的元素遮住')
    def receive_the_click(cls, element):
        # noinspection PyBroadException
        try:
            DriverTool.get_driver().execute_script("arguments[0].click();", element)
        except Exception as e:
            Log().error("\033[1;34m 点击失败\033[0m")

    @classmethod
    @allure.title("拖动到可见的元素去")
    def move_to_seeAble_element(cls, element):
        # noinspection PyBroadException
        try:
            Log().info("\033[32m拖动到可见的元素去\033[0m")
            DriverTool.get_driver().execute_script("arguments[0].scrollIntoView();", element)
        except Exception as e:
            Log().error("\033[1;34m 拖动到可见元素失败\033[0m")

    @classmethod
    @allure.title("连接mysql数据库操作相关数据")
    def connect_mysql_database(cls, database, sql_operate):
        Log().info("\033[32m连接mysql数据库操作相关数据\033[0m")
        cls.step("连接mysql数据库，获取操作句柄")
        con = pymysql.Connect(host='127.0.0.1', user="isv", password="isv@1234", database=database, port=3306)
        cur = con.cursor()
        cls.step("执行sql语句")
        cur.execute(sql_operate)
        cls.step("修改提交生效")
        con.commit()
        cls.step("打印sql执行后的结果")
        data = cur.fetchall()
        cls.step("关闭操作句柄")
        cur.close()
        cls.step("关闭数据库")
        con.close()
        return data

    @classmethod
    @allure.title("连接MongoDB数据库操作相关数据")
    def connect_MongoDB_database(cls, host, port, database, form, method, value=None, condition=None):
        Log().info("\033[32m连接MongoDB数据库操作相关数据\033[0m")
        cls.step("连接MongoDB数据库，获取操作句柄")
        client = pymongo.MongoClient(host=host, port=port)
        db = client[database]
        cls.step("如果需要用户名密码则输入")
        # db.authenticate('username', 'password')
        cls.step("form为表名字")
        collections = db[form]
        cls.step("查询操作")
        if method == "get":
            data = collections.find()
            for i in data:
                print(i)
            return data
        # 添加数据操作 value:添加的数据键值对
        elif method == "add":
            data = collections.insert_one(value)
            return data
        # 更新数据操作  form表名字, value更新后的数据, condition 筛选条件
        elif method == "update":
            data = collections.update_one(form, value, condition)
            return data
        # 删除数据操作form表名字, condition 筛选条件
        elif method == "delete":
            data = collections.delete_one(form, condition)
            return data
        # 关闭数据库
        client.close()

    @classmethod
    @allure.title("连接SQLite数据库操作相关数据")
    def connect_SQLite_database(cls, database, sql_operate):
        Log().info("\033[32m连接SQLite数据库操作相关数据\033[0m")
        cls.step("连接SQLite数据库，获取操作句柄")
        con = sqlite3.connect(database)
        cur = con.cursor()
        cls.step("执行sql语句")
        cur.execute(sql_operate)
        cls.step("修改提交生效")
        con.commit()
        cls.step("打印sql执行后的结果")
        data = cur.fetchall()
        cls.step("关闭操作句柄")
        cur.close()
        cls.step("关闭数据库")
        con.close()
        return data

    @classmethod
    @allure.title("连接redis数据库操作相关数据")
    def connect_redis_database(cls, host, password, method, keyName, where, refvalue=None, value=None):
        Log().info("\033[32m连接redis数据库操作相关数据\033[0m")
        cls.step("连接redis数据库，获取操作句柄")
        r = redis.Redis(host=host, port=6379, db=0, password=password)
        cls.step("新增")
        if method == "add":
            insert = r.linsert(keyName, where, refvalue, value)
            return insert
        # 删除键
        elif method == "delete":
            d = r.delete(keyName)
            return d
        # 设置键值对
        if method == "set":
            s = r.set(keyName, value)
            return s
        # 获取键值对
        if method == "get":
            v = r.get(keyName)
            return v

    @classmethod
    @allure.title("RPC断言工具带表情")
    def a_emoji(cls, r, expect):
        if r["retval"] != 0:
            print("\033[31m接口或返回数据可能有问题{}{}错误码:{} 返回值:{}\033[0m".format(
                emoji.emojize(":cry:", language='alias', variant="emoji_type"),
                emoji.emojize(":cry:", language='alias', variant="emoji_type"), r["retval"], r["value"]))
            assert r["retval"] == expect

        else:
            print("\033[32m接口通过需校验数据准确性{}{}返回值:{}\033[0m".format(
                emoji.emojize(":thumbsup:", language='alias', variant="emoji_type"),
                emoji.emojize(":thumbsup:", language='alias', variant="emoji_type"), r["value"]))

    @classmethod
    @allure.title("断言工具 RPC")
    def a_rpc(cls, r, expect):
        if r["retval"] == 0:
            print("\033[32m√准确性√\033[0m", r["value"])
            assert r["retval"] == expect

        else:
            print("\033[31m错误码:{} \033[0m".format(r["retval"]))
            assert r["retval"] == expect

    @classmethod
    @allure.title("断言工具 http")
    def a_http(cls, r, expect):
        if "Errors" not in r.json():
            print("\033[32m{}{}{}\033[0m".format(emoji.emojize(":thumbsup:", language='alias', variant="emoji_type"),
                                                 emoji.emojize(":thumbsup:", language='alias', variant="emoji_type"),
                                                 r.json()["Data"]))
            assert r.status_code == expect
        else:
            print("\033[31m Errors_code: {} \033[0m".format(r.json()["Errors"][0]["Code"]))
            assert r.json()["Errors"][0]["Code"] == expect

    @classmethod
    @allure.title("用于数据文件url转换读取")
    def get_pic_http(cls, url):  # 这里的端口号根据项目来决定 可写为传参
        http_ip_port = cf.get("Data", "http_ip_port")
        httpUrl = "".join([http_ip_port, url])
        f = urllib.request.urlopen(httpUrl)
        return f


    @classmethod
    @allure.title("Restful接口测试拼接url")
    def joint_url(cls, url):
        http_ip_port = cf.get("Data", "http_ip_port")
        r = "".join([http_ip_port, url])
        return r


# 获取本地路径
path = os.path.dirname(os.path.realpath(__file__))
# log_path是存放日志的路径
log_path = os.path.join(path, 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log:
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, './%s.log' % time.strftime('%Y-%m-%d'))
        self.logger = logging.getLogger('ISV_LuTuo')
        self.logger.setLevel(logging.INFO)
        # 日志输出格式
        self.formatter = logging.Formatter("\033[1;33m%(asctime)s|%(levelname)s|%(message)s\033[0m")

    def __console(self, level, message):
        # 创建一个fileHander，用于写入本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输入到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 避免日志重复
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        # 关闭打开文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
