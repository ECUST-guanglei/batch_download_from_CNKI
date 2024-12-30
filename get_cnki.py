from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging
import sys

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("automation_log.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def random_sleep(min_seconds, max_seconds):
    """随机等待函数，用于模拟人类行为"""
    sleep_time = random.uniform(min_seconds, max_seconds)
    logging.info(f"等待 {sleep_time:.2f} 秒")
    time.sleep(sleep_time)

def main():
    # 获取用户输入的搜索关键词
    search_query = input("请输入要搜索的内容: ")
    logging.info(f"用户输入的搜索关键词: {search_query}")

    # 初始化浏览器选项
    chromedriver_path = "D:\\Program Files (x86)\\chromedriver.exe"  # 根据实际情况调整
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # 启动时窗口最大化

    # 初始化浏览器驱动
    try:
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        logging.info("Chrome 浏览器启动成功")
    except Exception as e:
        logging.error(f"Chrome 浏览器启动失败: {e}")
        return

    try:
        # 打开知网首页
        driver.get("https://www.cnki.net")
        logging.info("已打开知网首页")
        
        # 使用 WebDriverWait 等待搜索框加载完成
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "txt_SearchText")))
        logging.info("搜索框已定位")

        # 输入搜索关键词
        search_box.send_keys(search_query)
        logging.info(f"输入搜索关键词: {search_query}")
        random_sleep(0.5, 1.5)  # 模拟输入完成的等待
        search_box.send_keys(Keys.RETURN)
        logging.info("按下回车键进行搜索")

        # 等待搜索结果页面加载
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#perPageDiv")))
        logging.info("搜索结果页面已加载")
        random_sleep(0.5, 1.5)

        # 点击“学术期刊”按钮
        try:
            # 定位到“学术期刊”按钮，通过属性 name 和 classid
            journal_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[name='classify'][classid='YSTT4HG0']")))
            journal_button.click()
            logging.info("点击了“学术期刊”按钮")
            random_sleep(0.5, 1)  # 等待页面加载完成
        except Exception as e:
            logging.error(f"点击“学术期刊”按钮失败: {e}")
            driver.quit()
            return


        # 选择每页显示50条
        page_size_dropdown = driver.find_element(By.CSS_SELECTOR, "#perPageDiv")
        page_size_dropdown.click()
        logging.info("点击每页显示数量的下拉框")
        random_sleep(0.5, 1.0)
        page_size_50 = driver.find_element(By.CSS_SELECTOR, "li[data-val='50']")
        page_size_50.click()
        logging.info("选择每页显示50条")
        # 等待页面刷新
        wait.until(EC.staleness_of(page_size_50))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#selectCheckAll1")))
        logging.info("页面已刷新 显示50条记录")
        random_sleep(1, 2)

        # 获取总页数
        try:
            page_info_element = driver.find_element(By.CSS_SELECTOR, ".countPageMark")
            total_pages = int(page_info_element.get_attribute("data-pagenum"))
            logging.info(f"搜索结果总页数: {total_pages}")
        except Exception as e:
            logging.warning(f"无法获取总页数 默认设置为1页: {e}")
            total_pages = 1

        # 循环处理每一页
        for current_page in range(1, total_pages + 1):
            logging.info(f"正在处理第 {current_page} 页")
            try:
                # 点击“全选”按钮
                select_all_button = wait.until(EC.element_to_be_clickable((By.ID, "selectCheckAll1")))
                logging.info("已定位到全选按钮")
                driver.execute_script("arguments[0].scrollIntoView(true);", select_all_button)
                random_sleep(0.5, 1)
                select_all_button.click()
                logging.info(f"第 {current_page} 页全选成功")
                random_sleep(0.5, 1)

                # 如果不是最后一页，点击“下一页”
                if current_page < total_pages:
                    next_page_button = wait.until(EC.element_to_be_clickable((By.ID, "PageNext")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                    random_sleep(0.5, 1)
                    next_page_button.click()
                    logging.info("点击“下一页”按钮")
                    # 等待页面加载
                    wait.until(EC.presence_of_element_located((By.ID, "selectCheckAll1")))
                    logging.info("下一页已加载")
                    random_sleep(0.5, 1.5)
            except Exception as e:
                logging.error(f"在第 {current_page} 页操作时出现问题: {e}")
                break  # 退出循环或根据需求决定是否继续

        # 最后一页已经被选中，无需再次点击全选

        # 点击“批量下载”按钮
        try:
            batch_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.bulkdownload.export")))
            batch_download_button.click()
            logging.info("点击“批量下载”按钮成功")
            random_sleep(1, 3)
        except Exception as e:
            logging.error(f"无法点击“批量下载”按钮: {e}")
            driver.quit()
            return

        # 切换到弹出的下载窗口
        try:
            driver.switch_to.window(driver.window_handles[-1])
            logging.info("已切换到下载窗口")
            confirm_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-download-all")))
            confirm_download_button.click()
            logging.info("点击“确认下载”按钮，开始下载")
        except Exception as e:
            logging.error(f"在下载窗口操作时出现问题: {e}")
            driver.quit()
            return

        # 等待下载完成（根据实际情况调整）
        random_sleep(100, 120)

    except Exception as e:
        logging.error(f"脚本运行过程中出现未处理的异常: {e}")
    finally:
        # 关闭浏览器
        driver.quit()
        logging.info("浏览器已关闭，脚本结束")

if __name__ == "__main__":
    main()
