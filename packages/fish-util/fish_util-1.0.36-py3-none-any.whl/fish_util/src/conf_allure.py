# 浏览器驱动
import logging

import allure
import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def browser():
    print("开始浏览器")
    # 01 用例前置操作
    # global driver
    # selenium提供的浏览器的无头模式（在后台运行的）, --headless
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()

    # 02 用例执行，返回driver
    # yield driver

    # 03 用例后置，关闭浏览器
    # driver.quit()


# 日志封装：1
# 日志的模块封装？
# hookwrapper=True 参数允许该函数包装 pytest 钩子，并在调用钩子之前和之后执行代码
# tryfirst=True 参数指定该钩子应在其他钩子之前执行
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     out = yield
#     report = out.get_result()
#     if report.when == 'call':
#         logging.info(f"用例ID：{report.nodeid}")
#         logging.info(f"测试结果：{report.outcome}")
#         logging.info(f"故障表示：{report.longrepr}")
#         logging.info(f"异常：{call.excinfo}")
#         logging.info(f"用例耗时：{report.duration}")
#         logging.info("**************************************")

# 日志封装：2
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    report = out.get_result()
    if report.when == "call":
        # 需要安装pip install pytest-allure-adaptor
        allure.attach(f"用例ID：{report.nodeid}", name="用例ID")
        allure.attach(f"测试结果：{report.outcome}", name="测试结果")
        allure.attach(f"故障表示：{report.longrepr}", name="故障表示")
        allure.attach(f"异常：{call.excinfo}", name="异常")
        allure.attach(f"用例耗时：{report.duration}", name="用例耗时")
        # 获取用例call执行结果为失败的情况
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            print("测试失败")
            # 添加allure报告截图
            # with allure.step("添加失败截图......"):
                # 使用allure自带的添加附件的方法,三个参数分别为：源文件、文件名、文件类型
                # allure.attach(driver.get_screenshot_as_png(),
                #               "失败截图", allure.attachment_type.PNG)
        else:
            print("测试成功")
            # 添加allure报告截图
            # with allure.step("添加成功截图......"):
                # 使用allure自带的添加附件的方法,三个参数分别为：源文件、文件名、文件类型
                # allure.attach(driver.get_screenshot_as_png(),
                #               "成功截图", allure.attachment_type.PNG)