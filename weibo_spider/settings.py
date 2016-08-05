# encoding=utf-8
BOT_NAME = 'weibo_spider'

SPIDER_MODULES = ['weibo_spider.spiders']
NEWSPIDER_MODULE = 'weibo_spider.spiders'

DOWNLOADER_MIDDLEWARES = {
    "weibo_spider.middleware.UserAgentMiddleware": 401,
    "weibo_spider.middleware.CookiesMiddleware": 402,
}

ITEM_PIPELINES = {
    'weibo_spider.pipelines.MySQLPipeline': 300,
}
MYSQL_PIPELINE_URL = 'mysql://root:123@localhost/weibospider_2'

DOWNLOAD_DELAY = 5  # 间隔时间
# CONCURRENT_ITEMS = 1000
# CONCURRENT_REQUESTS = 100
# REDIRECT_ENABLED = False
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 0
# CONCURRENT_REQUESTS_PER_SPIDER=100
# DNSCACHE_ENABLED = True
# LOG_LEVEL = 'INFO'    # 日志级别
# CONCURRENT_REQUESTS = 70
