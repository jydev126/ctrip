import json
import os
from datetime import datetime


class HotelSpiderPipeline:
    def open_spider(self, spider):
        # 创建save目录
        self.save_dir = "save"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # 生成时间戳后缀
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 设置文件路径
        self.json_file = os.path.join(
            self.save_dir, f"hotels_info_{self.timestamp}.json")
        self.txt_file = os.path.join(
            self.save_dir, f"hotels_info_{self.timestamp}.txt")

        # 打开JSON文件
        self.file = open(self.json_file, "w", encoding="utf-8")
        self.items = []
        spider.logger.info(f"打开输出文件: {self.json_file}")

    def close_spider(self, spider):
        # 写入JSON
        json.dump(self.items, self.file, ensure_ascii=False, indent=4)
        self.file.close()
        spider.logger.info(f"已将{len(self.items)}条酒店信息写入JSON文件")

        # 写入TXT
        with open(self.txt_file, "w", encoding="utf-8") as f:
            f.write(f"抓取时间: {self.timestamp}\n")
            f.write(f"共找到 {len(self.items)} 家酒店:\n")
            for i, hotel in enumerate(self.items, 1):
                f.write(f"{i}. {hotel['hotel_name']} - ¥{hotel['price']}\n")
        spider.logger.info("已将酒店信息写入TXT文件")

        print(f"\n共找到 {len(self.items)} 家酒店:")
        for i, hotel in enumerate(self.items, 1):
            print(f"{i}. {hotel['hotel_name']} - ¥{hotel['price']}")
        print(f"\n酒店信息已保存到:")
        print(f"- {self.json_file}")
        print(f"- {self.txt_file}")

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
