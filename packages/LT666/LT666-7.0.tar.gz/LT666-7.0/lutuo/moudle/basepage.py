import os
import time
import allure
import configparser
import uiautomation

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from lutuo.moudle.Log import Log
from lutuo.moudle.utils_luTuo import DriverTool

root_dir = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件所在目录的上一级目录
configPath = os.path.join(root_dir, r"config.ini")
path = os.path.abspath(configPath)
cf = configparser.ConfigParser()
cf.read(path, encoding="UTF-8")  # 拼接得到config.ini文件的路径，直接使用


class BasePage:

    def __init__(self):
        self.driver = DriverTool.get_driver()
        self.web_or_exe = cf.get("Data", "web_or_exe")
        self.web_url = cf.get("Data", "web_url")
        self.qt_exe = cf.get("Data", "QT_exe")
        self.softName = cf.get("Data", "softName")
        if self.web_or_exe == "web":  # 如果 Ture 则进行纯web的ui自动化，下面输入需要访问的地址即可，反之进行应用程序（exe)的ui自动化
            Log().info('\033[32m进入访问地址：{}\033[0m'.format(self.web_url))
            self.driver.get(self.web_url)
        else:
            Log().info('\033[32m进入QT 应用程序：{}\033[0m'.format(self.softName))

    @allure.title("QT定位按钮元素")
    def qt_getElementButton(self, AutomationId, **kwargs):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m开始定位元素\033[0m')
            element = uiautomation.ButtonControl(AutomationId="{}".format(AutomationId), **kwargs)
            return element
        except Exception as e:
            Log().error("\033[1;31;40m find_element_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 \033[0m")

    @allure.title("QT点击按钮")
    def qt_clickElementButton(self, element):
        Log().info('\033[32m点击元素\033[0m')
        if element:
            element.Click()
            time.sleep(0.3)
        else:
            Log().error("\033[1;34m click_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(element))

    @allure.title("QT定位文本框元素")
    def qt_getElementText(self, AutomationId, **kwargs):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m开始定位元素\033[0m')
            element = uiautomation.TextControl(AutomationId="{}".format(AutomationId), **kwargs)
            return element
        except Exception as e:
            Log().error("\033[1;31;40m find_element_failed *》*》*》*》*》*》*》*》*》*》*》*》*\033[0m")

    @allure.title("QT双击元素")
    def qt_doubleClickElement(self, element):
        Log().info('\033[32m双击元素\033[0m')
        if element:
            element.DoubleClick()
            time.sleep(0.3)
        else:
            Log().error("\033[1;34m click_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(element))

    @allure.title("QT定位编辑框")
    def qt_getElementEdit(self, AutomationId, **kwargs):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m开始定位元素：\033[0m')
            element = uiautomation.EditControl(AutomationId="{}".format(AutomationId), **kwargs)
            return element
        except Exception as e:
            Log().error("\033[1;31;40m find_element_failed *》*》*》*》*》*》*》*》*》*》*》*》*》\033[0m")

    @allure.title("QT编辑框输入值")
    def qt_inputEdit(self, element, data):
        Log().info('\033[32m输入文本值: {}\033[0m'.format(data))
        if element:
            element.Click()
            element.SendKeys("{}".format(data))
            time.sleep(0.3)
        else:
            Log().error("\033[1;34m input_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(data))

    @allure.title("定位单个元素")
    def get_single_element(self, style, value):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m开始定位元素：{}\033[0m'.format(value))
            element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(by=style, value=value))
            # 定位的元素高亮显示
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "background:red;border:2px solid cyan;")
            return element
        except Exception as e:
            Log().error("\033[1;31;40m find_element_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(value))
            return self.driver.get_screenshot_as_file(
                os.path.abspath("../Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "定位单个元素失败")))

    @allure.title("定位多个元素")
    def get_elements(self, style, value):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m开始定位多个元素：{}\033[0m'.format(value))
            elements = WebDriverWait(self.driver, 10).until(lambda x: x.find_elements(by=style, value=value))
            return elements

        except Exception as e:
            Log().error("\033[1;34m find_element_failed  *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(value))
            return self.driver.get_screenshot_as_file(
                os.path.abspath("../Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "定位多个元素失败")))

    @allure.title("输入值")
    def input_text(self, element, data):
        Log().info('\033[32m输入文本值: {}\033[0m'.format(data))
        if element:
            # 定位的元素高亮显示取消
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            element.clear()
            element.send_keys(data)
            time.sleep(0.3)

        else:
            Log().error("\033[1;34m input_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(data))
            return self.driver.get_screenshot_as_file(os.path.abspath("../Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "输入值失败")))

    @allure.title("切入到iframe中")
    def into_iframe(self, iframe_element):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m切换到iframe中:{}\033[0m'.format(iframe_element))
            self.driver.switch_to.frame(iframe_element)
        except Exception as e:
            Log().error("\033[1;34m 切入iframe失败  *》*》*》*》*》*》*》*》*》*》*》*》*》\033[0m")

    @allure.title("退出iframe嵌套")
    def out_iframe(self):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m退出iframe嵌套\033[0m')
            self.driver.switch_to.default_content()
        except Exception as e:
            Log().error("\033[1;34m 退出iframe嵌套失败  *》*》*》*》*》*》*》*》*》*》*》*》*》\033[0m")

    @allure.title("select下拉选择")
    def select_ele(self, e, index):
        # noinspection PyBroadException
        try:
            Log().info('\033[32m select下拉选择: {} {}\033[0m'.format(e, index))
            ele = Select(e)
            ele.select_by_index(index)
            return ele
        except Exception as e:
            Log().error("\033[1;34m select下拉选择失败  *》*》*》*》*》*》*》*》*》*》*》*》*》\033[0m")

    @allure.title("点击元素")
    def click_element(self, element):
        Log().info('\033[32m点击元素\033[0m')
        if element:
            # 定位的元素高亮显示取消
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.3)
        else:
            Log().error("\033[1;34m click_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(element))
            return self.driver.get_screenshot_as_file(os.path.abspath("../Screenshot/{}{}.png".format(time.strftime('%Y-%m-%d %H-%M-%S'), "点击元素失败")))

    @allure.title("清空文本")
    def clear_text(self, element):
        Log().info('\033[32m清空文本\033[0m')
        if element:
            # 定位的元素高亮显示取消
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            element.clear()
        else:
            Log().error("\033[1;34m clear_failed *》*》*》*》*》*》*》*》*》*》*》*》*》 {} \033[0m".format(element))
