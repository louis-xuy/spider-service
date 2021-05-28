from scrapy import Spider, Request


class IndexDailyEMSpider(Spider):
    """
    东方财富股票指数数据
    http://quote.eastmoney.com/center/hszs.html
    :param symbol: 带市场标识的指数代码
    :type symbol: str
    :return: 指数数据
    :rtype:
    """

    name = "index_daily_em"

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.spiders.stock.pipelines.IndexDailyPipeline': 800
        },
    }

    def __init__(self, *args, **kwargs):
        super(IndexDailyEMSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        market_map = {"sz": "0", "sh": "1"}
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "cb": "jQuery1124033485574041163946_1596700547000",
            "secid": f"{market_map[symbol[:2]]}.{symbol[2:]}",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields1": "f1,f2,f3,f4,f5",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "klt": "101",  # 日频率
            "fqt": "0",
            "beg": "19900101",
            "end": "20220101",
            "_": "1596700547039",
        }

