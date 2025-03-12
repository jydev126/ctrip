BOT_NAME = "hotel_spider"

SPIDER_MODULES = ["hotel_spider.spiders"]
NEWSPIDER_MODULE = "hotel_spider.spiders"

# 尊重robots.txt规则
ROBOTSTXT_OBEY = False

# 配置默认请求头
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    "hotel_spider.middlewares.SeleniumMiddleware": 543,
}

# 启用Item Pipeline
ITEM_PIPELINES = {
    "hotel_spider.pipelines.HotelSpiderPipeline": 300,
}
