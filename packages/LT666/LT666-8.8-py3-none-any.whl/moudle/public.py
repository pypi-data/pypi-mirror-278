import os
import time
import allure

from selenium.webdriver.common.by import By
from lutuo.moudle.basepage import BasePage
from lutuo.moudle.Log import Log
from lutuo.moudle.utils_luTuo import DriverTool, myTools


@allure.title('步骤')
def step(name):
    with allure.step(name):
        return None


@allure.title("用于自增系列")
def increment(userNumbers, user_name):
    for i in range(1, userNumbers):
        increment_param = user_name + str(i)
        return increment_param


# 元素定位对象层
class Public(BasePage):
    def __init__(self):
        super(Public, self).__init__()

    # 定位通用元素ID
    def find_element_ID(self, ID):
        return self.get_single_element(By.ID, "{}".format(ID))

    # 定位通用元素XPATH
    def find_element_XPATH(self, XPATH):
        return self.get_single_element(By.XPATH, "{}".format(XPATH))

    # 用户名
    def find_username(self):
        return self.get_single_element(By.ID, "Login15")

    # 找到密码
    def find_pwd(self):
        return self.get_single_element(By.ID, "Login18")

    # 找到登录按钮
    def find_login(self):
        return self.get_single_element(By.ID, "Login19")

    # 一级菜单
    def firstMenu(self, firstID):
        return self.get_single_element(By.ID, "{}".format(firstID))

    # 二级菜单
    def secondMenu(self, secondID):
        return self.get_single_element(By.ID, "{}".format(secondID))

    # 公司---------------------------------------------ByXPATH定位-----------------------------------------------
    def company_ByXPATH(self, company):
        return self.get_single_element(By.XPATH, '//*[@title="{}"]'.format(company))

    # 工厂
    def factory_ByXPATH(self, factory):
        return self.get_single_element(By.XPATH, '//*[@title="{}"][@class="node-txt ic_factory_name"]'.format(factory))

    # 工位
    def station_ByXPATH(self, station):
        return self.get_single_element(By.XPATH, '//*[@title="{}"][@class="node-txt ic_station_name"]'.format(station))

    # 车型
    def carType_ByXPATH(self, carType):
        return self.get_single_element(By.XPATH, '//*[@title="{}"][@class="node-txt ic_cartype_name"]'.format(carType))

    # 零件
    def part_ByXPATH(self, part):
        return self.get_single_element(By.XPATH, '//*[@title="{}"][@class="node-txt ic_part_name"]'.format(part))

    # 测点---------------------------------------------ByXPATH定位-----------------------------------------------
    def measurePoint_ByXPATH(self, measurePoint):
        return self.get_single_element(By.XPATH,
                                       '//*[@title="{}"][@class="node-txt ic_point_name"]'.format(measurePoint))

    # 公司。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。ByID_Index定位。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
    def company_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 工厂
    def factory_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 工位
    def station_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 车型
    def carType_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 零件
    def part_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 测点。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。ByID_Index定位。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
    def measurePoint_ByID_Index(self):
        return self.get_elements(By.ID, 'BaseTreeData11')

    # 日期条件
    def dateButton(self):
        return self.get_single_element(By.ID, 'TopSearchContentItem05')

    # 清空时间按钮
    def dateDeleteButton(self):
        return self.get_single_element(By.XPATH, '//*[@id="TopSearchContentItem07"]/div/i[2]')

    # 开始时间
    def StartTime(self):
        return self.get_single_element(By.ID, 'T')

    # 结束时间
    def EndTime(self):
        return self.get_single_element(By.ID, 'o')

    # 时间确定按钮
    def dateConfirm(self):
        return self.get_single_element(By.XPATH, '/html/body/div[2]/div[2]/button[2]/span')

    # 班次按钮
    def classes(self):
        return self.get_single_element(By.ID, 'TopSearchContentItem10')

    # 选择一个班次
    def chooseClasses(self, classeID):
        return self.get_single_element(By.ID, '{}'.format(classeID))

    # 起止车身号按钮
    def carBodyNum(self):
        return self.get_single_element(By.ID, 'TopSearchContentItem18')

    # 开始车身输入框
    def StartCarBodyNumTextbox(self):
        return self.get_single_element(By.ID, 'topSearch1')

    # 开始车身号, 只需输入想要查询的车身号名字
    def StartCarBodyNum(self, StartCarBodyNum):
        return self.get_single_element(By.XPATH, '//*[contains(text(),"{}")]'.format(StartCarBodyNum))

    # 结束车身输入框
    def EndCarBodyNumTextbox(self):
        return self.get_single_element(By.ID, 'topSearch2')

    # 结束车身号, 只需输入想要查询的车身号名字
    def EndCarBodyNum(self, EndCarBodyNum):
        return self.get_elements(By.XPATH, '//*[contains(text(),"{}")]'.format(EndCarBodyNum))

    # 最近
    def recently(self):
        return self.get_single_element(By.ID, 'TopSearchContentItem26')

    # 搜索按钮
    def searchButton(self):
        return self.get_single_element(By.ID, 'TopSearchContentItem29')

    # 搜索内容文本框
    def searchTextbox(self):
        return self.get_single_element(By.ID, 'BaseTreeData04')

    # 文本框搜索按钮
    def searchContentButton(self):
        return self.get_single_element(By.ID, 'BaseTreeData05')

    # 快速展开
    def fastExpand(self):
        return self.get_single_element(By.ID, 'BaseTreeData07')

    # 选择层级第几级别
    def chooseLevel(self, level):
        return self.get_single_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[{}]/span'.format(level))


# 元素具体操作层
class PublicHandle:
    def __init__(self):
        self.handle = Public()

    # 点击定位通用元素
    def click_find_element_ID(self, ID):
        self.handle.click_element(self.handle.find_element_ID(ID))

    # 点击定位通用元素
    def click_find_element_XPATH(self, XPATH):
        self.handle.click_element(self.handle.find_element_XPATH(XPATH))

    # 输入用户名
    def input_user(self, username):
        self.handle.input_text(self.handle.find_username(), username)

    def input_pwd(self, password):
        self.handle.input_text(self.handle.find_pwd(), password)

    def click_button(self):
        self.handle.click_element(self.handle.find_login())

    # 一级菜单
    def click_firstMenu(self, firstID):
        self.handle.click_element(self.handle.firstMenu(firstID))

    # 二级菜单
    def click_secondMenu(self, secondID):
        self.handle.click_element(self.handle.secondMenu(secondID))

    # 公司-----------------------------------------------------_ByXPATH----------------------------------------------
    def click_company_ByXPATH(self, company):
        self.handle.click_element(self.handle.company_ByXPATH(company))

    # 工厂
    def click_factory_ByXPATH(self, factory):
        self.handle.click_element(self.handle.factory_ByXPATH(factory))

    # 工位
    def click_station_ByXPATH(self, station):
        self.handle.click_element(self.handle.station_ByXPATH(station))

    # 车型
    def click_carType_ByXPATH(self, carType):
        self.handle.click_element(self.handle.carType_ByXPATH(carType))

    # 零件
    def click_part_ByXPATH(self, part):
        self.handle.click_element(self.handle.part_ByXPATH(part))

    # 测点-----------------------------------------------------_ByXPATH----------------------------------------------
    def click_measurePoint_ByXPATH(self, measurePoint):
        self.handle.click_element(self.handle.measurePoint_ByXPATH(measurePoint))

    # 公司。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。ByID_Index。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
    def click_company_ByID_Index(self, index_num1):
        self.handle.click_element(self.handle.company_ByID_Index()[index_num1])

    # 工厂
    def click_factory_ByID_Index(self, index_num2):
        self.handle.click_element(self.handle.factory_ByID_Index()[index_num2])

    # 工位
    def click_station_ByID_Index(self, index_num3):
        self.handle.click_element(self.handle.station_ByID_Index()[index_num3])

    # 车型
    def click_carType_ByID_Index(self, index_num4):
        self.handle.click_element(self.handle.carType_ByID_Index()[index_num4])

    # 零件
    def click_part_ByID_Index(self, index_num5):
        self.handle.click_element(self.handle.part_ByID_Index()[index_num5])

    # 测点。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。ByID_Index。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
    def click_measurePoint_ByID_Index(self, index_num6):
        self.handle.click_element(self.handle.measurePoint_ByID_Index()[index_num6])

    # 点击日期按钮
    def click_dateButton(self):
        self.handle.click_element(self.handle.dateButton())

    # 清空时间按钮
    def click_dateDeleteButton(self):
        self.handle.click_element(self.handle.dateDeleteButton())

    # 开始时间
    def inputStartTime(self, Startime):
        self.handle.input_text(self.handle.StartTime(), Startime)

    # 结束时间
    def inputEndTime(self, EndTime):
        self.handle.input_text(self.handle.EndTime(), EndTime)

    # 时间确定按钮
    def click_dateConfirm(self):
        self.handle.click_element(self.handle.dateConfirm())

    # 班次
    def click_classes(self):
        self.handle.click_element(self.handle.classes())

    # 选择一个班次
    def click_chooseClasses(self, classeID):
        self.handle.click_element(self.handle.chooseClasses(classeID))

    # 点击起止车身号按钮
    def click_carBodyNum(self):
        self.handle.click_element(self.handle.carBodyNum())

    # 先点击输入框
    def click_StartCarBodyNumTextbox(self):
        self.handle.click_element(self.handle.StartCarBodyNumTextbox())

    # 开始车身输入数字2进行下一步
    def input_StartCarBodyNumTextbox(self):
        self.handle.input_text(self.handle.StartCarBodyNumTextbox(), 2)

    # 下拉选择一个开始车身号
    def click_chooseStartCarBodyNum(self, StartCarBodyNum):
        self.handle.click_element(self.handle.StartCarBodyNum(StartCarBodyNum))

    # 先点击结束车身输入框
    def click_EndCarBodyNumTextbox(self):
        self.handle.click_element(self.handle.EndCarBodyNumTextbox())

    # 结束车身
    def input_EndCarBodyNumTextbox(self):
        self.handle.input_text(self.handle.EndCarBodyNumTextbox(), 2)

    # 下拉选择一个结束车身号
    def click_chooseEndCarBodyNum(self, EndCarBodyNum):
        self.handle.click_element(self.handle.EndCarBodyNum(EndCarBodyNum)[1])

    # 最近
    def click_recently(self):
        self.handle.click_element(self.handle.recently())

    # 点击搜索按钮
    def click_searchButton(self):
        self.handle.click_element(self.handle.searchButton())

    # 输入搜索内容文本框
    def input_searchTextbox(self, content):
        self.handle.input_text(self.handle.searchTextbox(), content)

    # 文本框搜索按钮
    def click_searchContentButton(self):
        self.handle.click_element(self.handle.searchContentButton())

    # 快速展开
    def click_fastExpand(self):
        self.handle.click_element(self.handle.fastExpand())

    # 选择层级第几级别
    def click_chooseLevel(self, level):
        self.handle.click_element(self.handle.chooseLevel(level))


# 具体业务层
class PublicScene:
    def __init__(self):
        self.scene = PublicHandle()

    @allure.title("重新回到登录页登录")
    def returnToLoginPage(self, user):
        DriverTool.get_driver().get(r"http://172.17.102.14:9999")
        PublicScene().loginFirst(user)

    @allure.title("首页登录模块")  # 这里的密码都统一了，写死了，如果根据业务可设置成变量
    def loginFirst(self, user):
        Log().info("---------Start---------开始进入登录方法---------Start---------")
        step("输入用户名")
        self.scene.input_user(user)
        step("输入密码")
        self.scene.input_pwd('isv@1234')
        step("点击登录按钮")
        self.scene.click_button()
        Log().info("。。。。。。。。。End。。。。。。。。。登录方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("一级二级菜单模块,只需输入一级二级的菜单ID")
    def treeByID_menu(self, firstID, secondID):
        Log().info("---------Start---------开始进入一二级菜单方法---------Start---------")
        step("一级菜单")
        self.scene.click_firstMenu(firstID)
        myTools.move_to_seeAble_element(self.scene.handle.secondMenu(secondID))
        step("二级菜单")
        self.scene.click_secondMenu(secondID)
        Log().info("。。。。。。。。。End。。。。。。。。。一二级菜单方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到车型级别则调用此方法，只用输入各层级标题名称即可")
    def treeNameToCarType(self, company, factory, station, carType):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByXPATH(company)
        step("点击工厂")
        self.scene.click_factory_ByXPATH(factory)
        step(" 点击工位")
        self.scene.click_station_ByXPATH(station)
        step("点击车型")
        self.scene.click_carType_ByXPATH(carType)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到车型级别则调用此方法，只用输入各层级标题索引即可")
    def treeIndexToCarType(self, index_num1, index_num2, index_num3, index_num4):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByID_Index(index_num1)
        step("点击工厂")
        self.scene.click_factory_ByID_Index(index_num2)
        step(" 点击工位")
        self.scene.click_station_ByID_Index(index_num3)
        step("点击车型")
        self.scene.click_carType_ByID_Index(index_num4)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到零件级别则调用此方法, 只用输入各层级标题名称即可")
    def treeNameToPart(self, company, factory, station, carType, part):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByXPATH(company)
        step("点击工厂")
        self.scene.click_factory_ByXPATH(factory)
        step(" 点击工位")
        self.scene.click_station_ByXPATH(station)
        step("点击车型")
        self.scene.click_carType_ByXPATH(carType)
        step("点击零件")
        self.scene.click_part_ByXPATH(part)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到零件级别则调用此方法, 只用输入各层级标题索引即可")
    def treeIndexToPart(self, index_num1, index_num2, index_num3, index_num4, index_num5):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByID_Index(index_num1)
        step("点击工厂")
        self.scene.click_factory_ByID_Index(index_num2)
        step(" 点击工位")
        self.scene.click_station_ByID_Index(index_num3)
        step("点击车型")
        self.scene.click_carType_ByID_Index(index_num4)
        step("点击零件")
        self.scene.click_part_ByID_Index(index_num5)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到测点级别则调用此方法， 只用输入各层级标题名称即可")
    def treeNameToMeasurePoint(self, company, factory, station, carType, part, measurePoint):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByXPATH(company)
        step("点击工厂")
        self.scene.click_factory_ByXPATH(factory)
        step(" 点击工位")
        self.scene.click_station_ByXPATH(station)
        step("点击车型")
        self.scene.click_carType_ByXPATH(carType)
        step("点击零件")
        self.scene.click_part_ByXPATH(part)
        step("点击测点")
        self.scene.click_measurePoint_ByXPATH(measurePoint)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("列表树形结构模块，到测点级别则调用此方法， 只用输入各层级标题索引即可")
    def treeIndexToMeasurePoint(self, index_num1, index_num2, index_num3, index_num4, index_num5, index_num6):
        Log().info("---------Start---------开始进入列表树形结构方法---------Start---------")
        step("点击公司")
        self.scene.click_company_ByID_Index(index_num1)
        step("点击工厂")
        self.scene.click_factory_ByID_Index(index_num2)
        step(" 点击工位")
        self.scene.click_station_ByID_Index(index_num3)
        step("点击车型")
        self.scene.click_carType_ByID_Index(index_num4)
        step("点击零件")
        self.scene.click_part_ByID_Index(index_num5)
        step("点击测点")
        self.scene.click_measurePoint_ByID_Index(index_num6)
        Log().info("。。。。。。。。。End。。。。。。。。。列表树形结构方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("顶部筛选条件模块,只需输入筛选条件：开始结束时间，班次，起止车身号，四个参数")
    def topSearch(self, Startime, EndTime, classeID, StartCarBodyNum, EndCarBodyNum):
        Log().info("---------Start---------开始进入顶部筛选条件模块方法---------Start---------")
        step("点击日期按钮")
        self.scene.click_dateButton()
        step("点击清空日期按钮")
        self.scene.click_dateDeleteButton()
        step("输入开始日期")
        self.scene.inputStartTime(Startime)
        step("输入结束日期")
        self.scene.inputEndTime(EndTime)
        time.sleep(1)
        step("点击日期确定")
        self.scene.click_dateConfirm()
        step("点击搜索按钮")
        self.scene.click_searchButton()
        step("点击班次按钮")
        self.scene.click_classes()
        step("选择一个班次")
        self.scene.click_chooseClasses(classeID)
        step("点击搜索")
        self.scene.click_searchButton()
        step("先点击起止车身按钮")
        self.scene.click_carBodyNum()
        step("点击开始输入框")
        self.scene.click_StartCarBodyNumTextbox()
        step("输入框输入2，出现下拉选择")
        self.scene.input_StartCarBodyNumTextbox()
        step("选择开始车身号")
        self.scene.click_chooseStartCarBodyNum(StartCarBodyNum)
        step("点击结束输入框")
        self.scene.click_EndCarBodyNumTextbox()
        step("输入结束车身输入框2")
        self.scene.input_EndCarBodyNumTextbox()
        time.sleep(0.5)
        step("选择下拉结束车身号")
        self.scene.click_chooseEndCarBodyNum(EndCarBodyNum)
        step("点击搜索按钮")
        self.scene.click_searchButton()
        step("选择最近按钮")
        self.scene.click_recently()
        step("点击搜索按钮")
        self.scene.click_searchButton()
        Log().info("。。。。。。。。。End。。。。。。。。。顶部筛选条件模块方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("搜索内容，快速展开模块，只需输入内容，以及层级数：第一级：1 第二级：2 第三级：3 第四级：4")
    def searchAndExpand(self, content, level):
        Log().info("----------Start--------开始进入搜索内容，快速展开模块方法---------Start---------")
        step("输入内容")
        self.scene.input_searchTextbox(content)
        step("点击搜索按钮")
        self.scene.click_searchContentButton()
        step("点击快速展开")
        self.scene.click_fastExpand()
        step("选择层级")
        self.scene.click_chooseLevel(level)
        Log().info("。。。。。。。。。End。。。。。。。。。搜索内容，快速展开模块方法结束。。。。。。。。。End。。。。。。。。。")

    @allure.title("上传文件,只需输入input的XPATH，和文件名称")
    def uploadFile(self, XPATH, fileName):
        Log().info("---------Start---------开始进入上传文件方法---------Start---------")
        DriverTool.get_driver().find_element(By.XPATH, '{}'.format(XPATH)).send_keys(
            os.path.abspath(r".\upload\{}".format(fileName)))
        Log().info("。。。。。。。。。End。。。。。。。。。上传文件方法结束。。。。。。。。。End。。。。。。。。。")

    # 定位通用元素
    def click_ByID(self, ID):
        Log().info("---------Start---------开始进入ID元素定位方法---------Start---------")
        self.scene.click_find_element_ID(ID)
        Log().info("。。。。。。。。。End。。。。。。。。。元素ID定位方法结束。。。。。。。。。End。。。。。。。。。")

    # 定位通用元素
    def click_ByXPATH(self, XPATH):
        Log().info("---------Start---------开始进入XPATH元素定位方法---------Start---------")
        self.scene.click_find_element_XPATH(XPATH)
        Log().info("。。。。。。。。。End。。。。。。。。。XPATH元素定位方法结束。。。。。。。。。End。。。。。。。。。")
