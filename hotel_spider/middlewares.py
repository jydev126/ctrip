from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SeleniumMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed,
                                signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        self.driver = webdriver.Chrome(options=chrome_options)

    def spider_closed(self, spider):
        self.driver.quit()

    def process_request(self, request, spider):
        if "hotels" in request.url:
            spider.logger.info(f"使用Selenium处理请求: {request.url}")
            self.driver.get(request.url)

            # 等待页面加载
            spider.logger.info("等待页面加载...")

            try:
                # 使用显式等待，等待hotellistContainer元素出现
                wait = WebDriverWait(self.driver, 30)  # 最多等待30秒
                hotel_container = wait.until(
                    EC.presence_of_element_located(
                        (By.ID, "hotellistContainer"))
                )
                spider.logger.info("hotellistContainer已加载")

                # 再等待一段时间确保所有酒店卡片都加载完成
                time.sleep(5)

                # 滚动页面以加载更多内容
                for i in range(3):
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                    time.sleep(2)  # 等待新内容加载
                    spider.logger.info(f"页面滚动 {i+1}/3")
            except Exception as e:
                spider.logger.error(f"等待页面加载时出错: {e}")

            # 保存HTML用于调试
            body = self.driver.page_source
            with open("debug_hotel_page.html", "w", encoding="utf-8") as f:
                f.write(body)
                spider.logger.info("已保存HTML到debug_hotel_page.html用于调试")

            return HtmlResponse(
                url=request.url, body=body, encoding="utf-8", request=request
            )
        return None
