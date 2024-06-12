import configparser
import json
import os
import subprocess
import warnings
import cv2
import emoji
import time
import allure
import psutil
import pyautogui
import pymongo
import pymysql
import urllib.request
import sqlite3
import redis
import uiautomation

from PIL import Image
from io import BytesIO
from pywinauto.application import Application
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from lutuo.moudle.Log import Log


@allure.feature("浏览器驱动")
class DriverTool:
    root_dir = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件所在目录的上一级目录
    configPath = os.path.join(root_dir, r".\config\config.ini")
    path = os.path.abspath(configPath)
    cf = configparser.ConfigParser()
    cf.read(path, encoding='utf-8')  # 拼接得到config.ini文件的路径，直接使用
    web_or_exe = cf.get("Data", "web_or_exe")
    app_exe = cf.get("Data", "app_exe")
    QT_exe = cf.get("Data", "QT_exe")
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
    elif web_or_exe == "app":  # 如果 是app 进行web-electron框架的应用程序自动化测试
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
                cls.driver.implicitly_wait(10)

            return cls.driver
    elif web_or_exe == "qt":
        options = None
        driver = None

        @classmethod
        def get_driver(cls):
            if not cls.driver:
                # 忽略UserWarning警告
                warnings.filterwarnings('ignore', category=UserWarning, message="Revert")
                # 启动应用程序
                cls.driver = Application().start(os.path.abspath(cls.QT_exe))
            return cls.driver


@allure.feature("项目中使用的所有方法")
class myTools:

    @classmethod
    @allure.title("QT断言 文本内容")
    def qt_assert_text(cls, AutomationId, **kwargs):
        Log().info("\033[32m获取文本内容\033[0m")
        text = uiautomation.TextControl(AutomationId='{}'.format(AutomationId), **kwargs).Name
        print('获取文本内容为: ', text)
        return text

    @classmethod
    @allure.title("QT鼠标左键拖拽")
    def qt_mouseLeftDrag(cls, x1, y1, x2, y2):
        Log().info("\033[32m QT鼠标左键拖拽：{},{},{},{}\033[0m".format(x1, y1, x2, y2))
        uiautomation.PressMouse(x1, y1)
        uiautomation.MoveTo(x2, y2)
        uiautomation.ReleaseMouse()
        time.sleep(0.3)

    @classmethod
    @allure.title("QT鼠标右键拖拽")
    def qt_mouseRightDrag(cls, x1, y1, x2, y2):
        Log().info("\033[32m QT鼠标右键拖拽：{},{},{},{}\033[0m".format(x1, y1, x2, y2))
        uiautomation.RightDragDrop(x1, y1, x2, y2)

    @classmethod
    @allure.title("鼠标双击具体坐标")
    def mouseDoubleClickPosition(cls, x, y):
        Log().info("\033[32m 双击坐标点 ：{},{}\033[0m".format(x, y))
        pyautogui.doubleClick(x, y)

    @classmethod
    @allure.title("鼠标单击具体坐标")
    def mouseClickPosition(cls, x, y):
        Log().info("\033[32m 单击坐标点：{},{}\033[0m".format(x, y))
        pyautogui.click(x, y)

    @classmethod
    @allure.title("具体元素鼠标拖拽")
    def elementDragDrop(cls, element, x_offset, y_offset):
        Log().info("\033[32m 鼠标点击按住拖拽 ：{},{}\033[0m".format(x_offset, y_offset))
        # 使用ActionChains来模拟点击并拖动操作
        actions = ActionChains(DriverTool.get_driver())
        actions.click_and_hold(element).perform()  # 点击并按住元素
        # 执行拖动，这里的x和y是相对于当前位置的偏移量
        actions.move_by_offset(x_offset, y_offset).release().perform()  # 拖动并释放元素

    @classmethod
    @allure.title("鼠标滚轮缩放")
    def mouseZoom(cls, x1, y1, z):
        Log().info("\033[32m 按住坐标位置滚轮缩放：{},{},{}\033[0m".format(x1, y1, z))
        # 起始位置
        pyautogui.moveTo(x1, y1)
        myTools.step("按住ctrl键")
        pyautogui.keyDown("ctrl")
        pyautogui.scroll(z)
        time.sleep(0.5)
        pyautogui.keyUp("ctrl")

    @classmethod
    @allure.title("鼠标左键拖拽画框")
    def mouseLeftDrag(cls, x1, y1, x2, y2):
        Log().info("\033[32m 鼠标左键画框：{},{},{},{}\033[0m".format(x1, y1, x2, y2))
        # 起始位置
        pyautogui.moveTo(x1, y1)
        time.sleep(0.5)
        # 按下鼠标左键
        pyautogui.mouseDown()
        # 移动到结束点
        pyautogui.moveTo(x2, y2)
        time.sleep(0.5)
        # 释放鼠标左键完成选择
        pyautogui.mouseUp()

    @classmethod
    @allure.title("鼠标右键拖拽移动")
    def mouseRightDrag(cls, x1, y1, x2, y2):
        Log().info("\033[32m鼠标右键拖拽移动 ：{},{},{},{}\033[0m".format(x1, y1, x2, y2))
        # 起始位置
        pyautogui.moveTo(x1, y1)
        time.sleep(0.5)
        # 右键点击以启动拖拽
        pyautogui.mouseDown(button='right')
        time.sleep(0.5)
        # 拖拽到目标位置
        pyautogui.dragTo(x2, y2, duration=1, button='right')
        time.sleep(0.5)
        # 释放鼠标右键
        pyautogui.mouseUp(x2, y2, button='right')

    @classmethod
    @allure.title("读取配置文件方法")
    def readConfig(cls, content):
        root_dir = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件所在目录的上一级目录
        configPath = os.path.join(root_dir, r".\config\config.ini")
        path = os.path.abspath(configPath)
        cf = configparser.ConfigParser()
        cf.read(path, encoding='utf-8')  # 拼接得到config.ini文件的路径，直接使用
        return cf.get("Data", content)

    @classmethod
    @allure.title("对比两张图相似度")
    def prepare_image(cls, region, picName):
        Log().info("\033[32m 对比两张图相似度：{},{}\033[0m".format(region, picName))
        # 获取当前窗口的完整屏幕截图
        screenshot_png = DriverTool.get_driver().get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot_png))
        # 根据指定的region裁剪屏幕截图 前两个值要大于模板，后两个要小于模板
        left, upper, right, lower = region
        box = (left, upper, right, lower)
        # 保存要验证的目标图片
        screenshot.crop(box).save("../upload/{}.png".format(picName), "PNG")
        # 模板图像的加载
        template = cv2.imread("../upload/{}Temp.png".format(picName), cv2.IMREAD_COLOR)
        # 要验证的截图加载
        match_area = cv2.imread("../upload/{}.png".format(picName), cv2.IMREAD_COLOR)
        # 计算匹配区域的相似度
        similarity = cv2.matchTemplate(match_area, template, cv2.TM_CCOEFF_NORMED)[0][0]
        # 断言相似度是否大于阈值
        print("两张图片相似度值：", similarity)
        return similarity

    @classmethod
    @allure.title("单个元素定位")
    def find_element(cls, style, value):
        Log().info("\033[32m定位单个元素\033[0m")
        element = DriverTool.get_driver().find_element(style, value)
        # 定位的元素高亮显示
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
        return element

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
    @allure.title('关闭QT应用程序')
    def close_QtDriver(cls):
        Log().info("\033[32m关闭QT程序: 测试工具低代码开发平台\033[0m")

        # 例如，通过进程名获取PID
        def get_pid_by_name(process_name):
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process_name:
                    return proc.pid
            return None

        # 使用函数获取进程PID
        pid = get_pid_by_name('{}'.format(myTools.readConfig("process")))
        subprocess.run(['taskkill', '/f', '/pid', str(pid)])

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
        element.clear()
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        ActionChains(DriverTool.get_driver()).double_click(element).perform()
        element.send_keys(content)

    @classmethod
    @allure.title('模拟鼠标悬浮')
    def mouse_hover(cls, style, value):
        Log().info("\033[32m模拟鼠标悬浮\033[0m")
        element = DriverTool.get_driver().find_element(style, value)
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        # 获取元素的中心点坐标
        x, y = element.location['x'] + element.size['width'] / 2, element.location['y'] + element.size['height'] / 2
        # 移动鼠标到元素的中心
        pyautogui.moveTo(x, y, duration=0.25)

    @classmethod
    @allure.title('获取中心点坐标')
    def get_center_point(cls, style, value, content):
        Log().info("\033[32m模拟鼠标悬浮\033[0m")
        element = DriverTool.get_driver().find_element(style, value)
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        # 获取元素的中心点坐标
        x, y = element.location['x'] + element.size['width'] / 2, element.location['y'] + element.size['height'] / 2
        print("{}中心点坐标为：".format(content), x, y)

    @classmethod
    @allure.title('模拟鼠标点击元素')
    def mouse_click(cls, style, value):
        Log().info("\033[32m模拟鼠标点击\033[0m")
        element = DriverTool.get_driver().find_element(style, value)
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
        DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        ActionChains(DriverTool.get_driver()).click(element).perform()

    @classmethod
    @allure.title("获取元素个数")
    def get_elements_number(cls, value):
        Log().info("\033[32m获取元素个数\033[0m")
        ele = DriverTool().get_driver().find_elements(By.XPATH, "{}".format(value))
        print("元素个数: ", len(ele))
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
        eleTxt = DriverTool.get_driver().find_element(style, '{}'.format(value)).text
        print("列表文本：", eleTxt)
        return eleTxt

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
            tips = wait_obj.until(lambda x: x.find_element(by=style, value=value)).text
            print('获取断言内容为: ', tips)
            return tips
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
            alter_msg = wait_obj.until(lambda x: x.find_element(By.CLASS_NAME, 'message message-success')).text
            print('获取弹窗信息为: ', alter_msg)
            return alter_msg

        except Exception as e:
            Log().error("\033[1;31;40m get_alert_failed \033[0m")
            return DriverTool.get_driver().get_screenshot_as_file(
                os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "获取弹窗信息失败")))

    @classmethod
    @allure.title('获取弹窗信息/html/body/div[3]')
    def get_alter_msg_exe(cls):
        # noinspection PyBroadException
        try:
            Log().info("\033[32m获取弹窗信息\033[0m")
            wait_obj = WebDriverWait(DriverTool.get_driver(), 2)
            alter_msg = wait_obj.until(lambda x: x.find_element(By.XPATH, '//*[@class="tip"]')).text
            print('获取弹窗信息为: ', alter_msg)
            return alter_msg

        except Exception as e:
            Log().error("\033[1;31;40m get_alert_failed \033[0m")
            return DriverTool.get_driver().get_screenshot_as_file(
                os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "获取弹窗信息失败")))

    @classmethod
    @allure.title("获取当前页面标题")
    def get_title(cls):
        Log().info("\033[32m获取当前页面的title\033[0m")
        return DriverTool.get_driver().title

    # 如果需要，可以调整截图区域坐标
    @classmethod
    @allure.title("截图操作")
    def screen_shot(cls):
        Log().info("\033[32m截图操作\033[0m")
        s = DriverTool.get_driver().get_screenshot_as_file(
            os.path.abspath("./Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "特意截图")))
        return s

    @classmethod
    @allure.title("输入值")
    def input_text(cls, style, value, content):
        Log().info("\033[32m输入值: {}\033[0m".format(content))
        element = DriverTool.get_driver().find_element(style, value)
        if element:
            element.clear()
            DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid "
                                                                                                                "cyan;")
            DriverTool.get_driver().execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
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
    @allure.title("用于自增系列")
    def increment(cls, param_name):
        with open(r"..\response\response.py", "r", encoding="utf-8") as f:
            i = f.read()
            increment_param = param_name + str(i)
            i = int(i) + 1
        with open(r"..\response\response.py", "w", encoding="utf-8") as f:
            f.write(str(i))
        return increment_param

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
                emoji.emojize(":smile:", language='alias', variant="emoji_type"),
                emoji.emojize(":smile:", language='alias', variant="emoji_type"), r["value"]))

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
            print("\033[32m√^_^√\033[0m")
            assert r.status_code == expect
        else:
            print("\033[31m Errors_code: {} \033[0m".format(r.json()["Errors"][0]["Code"]))
            assert r.json()["Errors"][0]["Code"] == expect

    @classmethod
    @allure.title("用于数据文件url转换读取")
    def get_pic_http(cls, port, url):  # 这里的端口号根据项目来决定 可写为传参19798
        httpUrl = "".join(["http://", "127.0.0.1", ":", "{}".format(port), "{}".format(url)])
        f = urllib.request.urlopen(httpUrl)
        return f

    @classmethod
    @allure.title("Restful接口测试拼接url")
    def joint(cls, url):
        http_ip_port = myTools.readConfig("Data", "http_ip_port")
        r = "".join([http_ip_port, url])
        return r
