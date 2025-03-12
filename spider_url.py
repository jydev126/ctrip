from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os


def extract_hotel_info_with_selenium(url):
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # 设置窗口大小
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    try:
        # 初始化WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        print("等待页面加载...")

        # 使用显式等待，等待hotellistContainer元素出现
        wait = WebDriverWait(driver, 30)  # 最多等待30秒
        hotel_container = wait.until(
            EC.presence_of_element_located((By.ID, "hotellistContainer"))
        )

        # 再等待一段时间确保所有酒店卡片都加载完成
        print("等待酒店数据加载...")
        time.sleep(5)

        # 滚动页面以加载更多内容
        for i in range(3):  # 滚动几次以确保加载更多内容
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待新内容加载

        # 获取页面源码
        html_content = driver.page_source

        # 保存HTML用于调试
        with open("debug_hotel_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            print("已保存HTML到debug_hotel_page.html用于调试")

        # 关闭浏览器
        driver.quit()

        # 解析HTML并提取酒店信息
        soup = BeautifulSoup(html_content, "html.parser")

        # 找到hotellistContainer
        hotel_list_container = soup.find(id="hotellistContainer")
        if not hotel_list_container:
            print("没有找到hotellistContainer")
            return []

        # 找到所有的hotel-card
        hotel_cards = hotel_list_container.find_all(
            class_=lambda c: c and "hotel-card" in c
        )

        hotels_info = []
        processed_hotels = set()  # 用于去重

        for idx, card in enumerate(hotel_cards):
            # 找到hotel_hotelInfoWrap
            info_wrap = card.find(
                class_=lambda c: c and "hotel-card_hotelInfoWrap" in c
            )
            if not info_wrap:
                continue

            # 提取酒店名称
            hotel_name_elem = info_wrap.find(
                class_=lambda c: c and "card_hotelName" in c
            )
            if hotel_name_elem:
                # 找到所有包含xt-text的元素
                text_elems = hotel_name_elem.find_all(
                    class_=lambda c: c and "xt-text" in c
                )
                if text_elems:
                    hotel_name = text_elems[-1].get_text().strip()
                else:
                    hotel_name = "未找到酒店名称"
            else:
                hotel_name = "未找到酒店名称"

            # 提取酒店价格 - 更精确的定位
            price = "未找到价格"

            # 尝试方法1：直接查找card_strong类
            strong_price = info_wrap.find(class_=lambda c: c and "card_strong" in c)
            if strong_price:
                price = strong_price.get_text().strip()
            else:
                # 尝试方法2：查找包含价格的其他元素
                price_elements = info_wrap.find_all(
                    class_=lambda c: c and "card_price" in c
                )
                for elem in price_elements:
                    if elem.get_text().strip().isdigit():
                        price = elem.get_text().strip()
                        break

            # 对酒店调试输出
            print(f"调试 - 酒店{idx + 1}: {hotel_name}")
            price_debug = info_wrap.find_all(
                class_=lambda c: c and "price" in c.lower()
            )
            if price_debug:
                print(f"  找到价格相关元素: {len(price_debug)}个")
                for i, p_elem in enumerate(price_debug):
                    print(f"  - 元素{i + 1}类名: {p_elem.get('class')}")
                    print(f"    内容: {p_elem.get_text().strip()}")

            # 去重处理
            hotel_key = hotel_name
            if hotel_key not in processed_hotels:
                processed_hotels.add(hotel_key)
                hotels_info.append({"酒店名称": hotel_name, "价格": price})

        return hotels_info

    except Exception as e:
        print(f"使用Selenium时发生错误: {e}")
        import traceback

        traceback.print_exc()
        return []


def main():
    url = "https://m.ctrip.com/webapp/hotels/hotelsearch/list?__redirectback=1&city=4&countryid=0&atime=2025-03-15&days=3&isfromtaroinquire=1&fromLongRentTab=0"

    print("正在抓取酒店信息，这可能需要一点时间...")
    hotels_info = extract_hotel_info_with_selenium(url)

    if hotels_info:
        print(f"\n共找到 {len(hotels_info)} 家酒店:")
        for i, hotel in enumerate(hotels_info, 1):
            print(f"{i}. {hotel['酒店名称']} - ¥{hotel['价格']}")

        # 将结果保存到文件
        with open("hotels_info.txt", "w", encoding="utf-8") as f:
            f.write(f"共找到 {len(hotels_info)} 家酒店:\n")
            for i, hotel in enumerate(hotels_info, 1):
                f.write(f"{i}. {hotel['酒店名称']} - ¥{hotel['价格']}\n")
        print("\n酒店信息已保存到 hotels_info.txt 文件中")
    else:
        print("未找到任何酒店信息")


if __name__ == "__main__":
    main()
