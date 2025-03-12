import scrapy
from hotel_spider.items import HotelItem
from hotel_spider.config import DEFAULT_URL
from urllib.parse import urlencode
from datetime import datetime, timedelta


class HotelSpider(scrapy.Spider):
    name = "hotel"
    allowed_domains = ["ctrip.com"]

    def __init__(self, url=None, city=None, days=None, date=None, *args, **kwargs):
        super(HotelSpider, self).__init__(*args, **kwargs)

        if url:
            self.start_urls = [url]
        else:
            # 如果没有提供URL，使用参数构建URL或使用默认URL
            if city or days or date:
                from hotel_spider.config import URL_PARAMS
                params = URL_PARAMS.copy()

                if city:
                    params['city'] = city
                if days:
                    params['days'] = days

                # 设置入住日期
                if date:
                    params['atime'] = date
                else:
                    # 如果没有提供日期，设置为明天
                    tomorrow = datetime.now() + timedelta(days=1)
                    params['atime'] = tomorrow.strftime("%Y-%m-%d")

                # 构建URL
                base_url = "https://m.ctrip.com/webapp/hotels/hotelsearch/list"
                self.start_urls = [f"{base_url}?{urlencode(params)}"]
            else:
                self.start_urls = [DEFAULT_URL]

        self.logger.info(f"使用URL: {self.start_urls[0]}")

    def parse(self, response):
        self.logger.info("正在解析酒店列表页面")

        # 找到hotellistContainer
        hotel_list_container = response.css("#hotellistContainer")
        if not hotel_list_container:
            self.logger.warning("没有找到hotellistContainer")
            return

        # 找到所有的hotel-card
        hotel_cards = hotel_list_container.xpath(
            './/*[contains(@class, "hotel-card")]')
        self.logger.info(f"找到 {len(hotel_cards)} 个酒店卡片")
        processed_hotels = set()  # 用于去重

        for card in hotel_cards:
            # 提取酒店名称
            hotel_name_elems = card.xpath(
                './/*[contains(@class, "card_hotelName")]//*[contains(@class, "xt-text")]/text()'
            ).getall()
            if hotel_name_elems:
                hotel_name = hotel_name_elems[-1].strip()
            else:
                hotel_name = "未找到酒店名称"

            # 提取酒店价格
            price = "未找到价格"

            # 方法1：直接查找card_strong类
            strong_price = card.xpath(
                './/*[contains(@class, "card_strong")]/text()'
            ).get()
            if strong_price and strong_price.strip():
                price = strong_price.strip()
            else:
                # 方法2：查找包含价格的其他元素
                price_elements = card.xpath(
                    './/*[contains(@class, "card_price")]/text()'
                ).getall()
                for elem in price_elements:
                    if elem.strip().isdigit():
                        price = elem.strip()
                        break

            # 去重处理
            hotel_key = hotel_name
            if hotel_key not in processed_hotels:
                processed_hotels.add(hotel_key)
                item = HotelItem()
                item["hotel_name"] = hotel_name
                item["price"] = price
                yield item
