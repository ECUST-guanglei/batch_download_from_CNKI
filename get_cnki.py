from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# 设置 ChromeDriver 的路径
chromedriver_path = "D:\\Program Files (x86)\\chromedriver.exe"

# 初始化浏览器
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 启动时窗口最大化
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# 打开知网页面
driver.get("https://www.cnki.net")  # 知网首页地址

# 模拟搜索操作

# 等待页面加载完成
time.sleep(random.uniform(5, 6))

search_box = driver.find_element(By.ID, "txt_SearchText")  # 定位搜索框
search_box.send_keys("盾构 结泥饼")  # 输入关键词
time.sleep(random.uniform(0, 1))  # 等待输入完成
search_box.send_keys(Keys.RETURN)  # 模拟按下回车键

time.sleep(random.uniform(4, 6))

# 选择单页显示数量
page_size = driver.find_element(By.CSS_SELECTOR, "#perPageDiv")  # 定位单页显示数量的下拉框
page_size.click()  # 点击下拉框
time.sleep(random.uniform(0, 1))  # 等待下拉框展开
page_size_50 = driver.find_element(By.CSS_SELECTOR, "li[data-val='50']")  # 选择单页显示50条
page_size_50.click()  # 点击选择
time.sleep(random.uniform(1, 2))  # 等待页面刷新完成

# 定义全选、翻页和下载的循环操作
for _ in range(2):  # 循环
    try:
        # 点击“全选”按钮
        select_all_button = driver.find_element(By.CSS_SELECTOR, "#selectCheckAll1")  # 根据页面按钮的CSS选择器定位
        select_all_button.click()
        print("全选成功")
        time.sleep(random.uniform(1, 2))   # 等待全选操作完成

        # 点击“下一页”按钮
        next_page_button = driver.find_element(By.CSS_SELECTOR, "#PageNext")  # 定位“下一页”按钮
        next_page_button.click()
        print("下一页成功")
        time.sleep(random.uniform(1, 2))  # 等待页面加载完成
    except Exception as e:
        print("操作出现问题：", e)
        break

# 点击“全选”按钮
select_all_button = driver.find_element(By.CSS_SELECTOR, "#selectCheckAll1")  # 全选按钮的实际CSS选择器
select_all_button.click()
print("全选成功")
time.sleep(random.uniform(1, 2))   # 等待全选操作完成

# 点击“批量下载”按钮
try:
    batch_download_button = driver.find_element(By.CSS_SELECTOR,  "li.bulkdownload.export")  # 批量下载按钮的实际CSS选择器
    batch_download_button.click()
    print("批量下载按钮点击成功")
    time.sleep(random.uniform(1,3))  # 等待操作完成
except Exception as e:
    print("下载按钮未找到或点击失败：", e)

# 跳转到弹出的新窗口
driver.switch_to.window(driver.window_handles[-1])
confirm_download_button = driver.find_element(By.CSS_SELECTOR, "#btn-download-all")  # 确认下载按钮的实际CSS选择器
confirm_download_button.click()
print("确认下载按钮已点击,开始下载")

# 等待
time.sleep(10)

# 关闭浏览器
driver.quit()
