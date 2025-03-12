from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_spider(url=None, city=None, days=None, date=None):
    """
    运行爬虫的函数

    Args:
        url (str, optional): 完整的URL
        city (str, optional): 城市代码，例如：4代表重庆
        days (str, optional): 入住天数
        date (str, optional): 入住日期，格式为YYYY-MM-DD
    """
    print("开始爬取酒店信息...")
    process = CrawlerProcess(get_project_settings())

    # 传递参数给爬虫
    process.crawl("hotel",
                  url=url,
                  city=city,
                  days=days,
                  date=date)

    process.start()
    print("爬取完成！")


def main():
    # 示例：直接传入参数
    # 方式1：使用完整URL
    # run_spider(url="https://m.ctrip.com/webapp/hotels/hotelsearch/list?__redirectback=1&city=1&countryid=0&atime=2025-03-15&days=2&isfromtaroinquire=1&fromLongRentTab=0")

    # 方式2：使用城市代码、天数和日期
    run_spider(city="4", days="5", date="2025-04-01")

    # 方式3：只指定城市和天数，日期默认为明天
    # run_spider(city="4", days="5")

    # 方式4：使用默认配置
    # run_spider()


if __name__ == "__main__":
    main()
