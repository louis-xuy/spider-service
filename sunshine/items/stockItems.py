#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-01-08 14:08
"""

from scrapy.item import Item, Field

class StockInfoItem(Item):
    _table_name = 'stock_info'
    code = Field()  # 证券代码 code
    symbol = Field()  # 证券简称 name
    fullname = Field()  # 中文名
    enname = Field()  # 英文名
    area = Field()  # 地域
    province = Field()
    city = Field()
    address = Field()  # 注册地址
    sector_code_name = Field()
    sector_code = Field()
    industry_code = Field()
    industry_name = Field()
    board_type = Field()  # 市场类型（主板/创业板/科创板/CDR）
    exchange = Field()
    status = Field()  #状态。’Active’ - 正常上市, ‘Delisted’ - 终止上市, ‘TemporarySuspended’ - 暂停上市,
    listed_date = Field()  # A股上市日期
    de_listed_date = Field()  # 退市日期
    is_hs = Field()  # 是否沪深港通标的，N否 H沪股通 S深股通
    round_lot = Field()
    type = Field()
    trading_hours = Field()
    special_type = Field()


class StockDailyTrade(Item):
    SecuCode = Field()  # 证券代码 code
    Open = Field()  # 开盘 open
    High = Field()  # 最高 high
    Low = Field()  # 最低 low
    Last = Field()  # 最新 last
    PrevClose = Field()  # 前收 prev_close
    ChgRate = Field()  # 涨跌幅 chg_rate(%)
    Volume = Field()  # 成交量(股) volume, 网页上显示的是 手, 1 手等于 100 股
    Amount = Field()  # 成交额(元) amount， 网页上是万元
    TradePhase = Field()  # tradephase
    RiseFall = Field()  # 涨跌 change --> FIX change 是 mysql 关键字
    AmpRate = Field()  # 振幅 amp_rate
    CPXXSubType = Field()
    TradingDay = Field()

class StockNewsItem(Item):
    website = Field()
    url = Field()
    title = Field()
    abstract = Field()
    content = Field()
    datetime = Field()
    original = Field()
    author = Field()
    file_urls = Field()
    files = Field()
    industryName = Field()

class StockFinanceReportItem(Item):
    SecuCode = Field()
    ReportType = Field()
    ReportDateType = Field()
    Type = Field()
    ReportDate = Field()
    Currency = Field()
    MONETARYFUND = Field() # 货币资金
    SETTLEMENTPROVISION = Field()  # 结算备付金
    LENDFUND = Field()
    FVALUEFASSET = Field()
    TRADEFASSET = Field()
    DEFINEFVALUEFASSET = Field()
    BILLREC = Field()
    ACCOUNTREC = Field()  # 应收账款
    ADVANCEPAY = Field() # 预付账款
    PREMIUMREC = Field()
    RIREC = Field()
    RICONTACTRESERVEREC = Field()
    INTERESTREC = Field()
    DIVIDENDREC = Field()
    OTHERREC = Field() # 其他应收款
    EXPORTREBATEREC = Field()
    SUBSIDYREC = Field()
    INTERNALREC = Field()
    BUYSELLBACKFASSET = Field() # 买入返售金融资产
    INVENTORY = Field()
    CLHELDSALEASS = Field()
    NONLASSETONEYEAR = Field()
    OTHERLASSET = Field() # 其他流动资产
    SUMLASSET = Field() # 流动资产合计
    LOANADVANCES = Field() # 发放委托贷款及垫款
    SALEABLEFASSET = Field()
    HELDMATURITYINV = Field()
    LTREC = Field()
    LTEQUITYINV = Field() # 长期股权投资
    ESTATEINVEST = Field()
    FIXEDASSET = Field() # 固定资产
    CONSTRUCTIONPROGRESS = Field() # 在建工程
    CONSTRUCTIONMATERIAL = Field()
    LIQUIDATEFIXEDASSET = Field()
    PRODUCTBIOLOGYASSET = Field()
    OILGASASSET = Field()
    INTANGIBLEASSET = Field() # 无形资产
    DEVELOPEXP = Field()
    GOODWILL = Field()  # 商誉
    LTDEFERASSET = Field()  # 长期待摊费用
    DEFERINCOMETAXASSET = Field()  # 递延所得税资产
    OTHERNONLASSET = Field()  # 其他非流动资产
    SUMNONLASSET = Field()  # 非流动资产合计
    SUMASSET = Field()  # 资产合计
    STBORROW = Field()  # 短期借债
    BORROWFROMCBANK = Field()
    DEPOSIT = Field()
    BORROWFUND = Field()  # 拆入资金
    FVALUEFLIAB = Field()
    TRADEFLIAB = Field()
    DEFINEFVALUEFLIAB = Field()
    BILLPAY = Field()
    ACCOUNTPAY = Field()  # 应付账款
    ADVANCERECEIVE = Field()  # 预售款项
    SELLBUYBACKFASSET = Field()  # 卖出回购金融资产款
    COMMPAY = Field()
    SALARYPAY = Field()  # 应付职工薪酬
    TAXPAY = Field()  # 应交税费
    INTERESTPAY = Field()
    DIVIDENDPAY = Field()
    RIPAY = Field()
    INTERNALPAY = Field()
    OTHERPAY = Field()  # 其他应付款
    ANTICIPATELLIAB = Field()
    CONTACTRESERVE = Field()
    AGENTTRADESECURITY = Field()  # 代理买卖证券款
    AGENTUWSECURITY = Field()
    DEFERINCOMEONEYEAR = Field()
    STBONDREC = Field()  # 应付短期债券
    CLHELDSALELIAB = Field()
    NONLLIABONEYEAR = Field()  # 一年内到期的非流动负债
    OTHERLLIAB = Field()  # 其他流动负债
    SUMLLIAB = Field()  # 流动负债合计
    LTBORROW = Field()
    BONDPAY = Field()  # 应付债券
    PREFERSTOCBOND = Field()
    SUSTAINBOND = Field()
    LTACCOUNTPAY = Field()
    LTSALARYPAY = Field()
    SPECIALPAY = Field()
    ANTICIPATELIAB = Field()
    DEFERINCOME = Field()
    DEFERINCOMETAXLIAB = Field()  # 递延所得税负债
    OTHERNONLLIAB = Field()  # 其他非流动负债
    SUMNONLLIAB = Field()  # 非流动负债合计
    SUMLIAB = Field()  # 负债合计
    SHARECAPITAL = Field()  # 实收资本
    OTHEREQUITY = Field()  #
    PREFERREDSTOCK = Field()
    SUSTAINABLEDEBT = Field()
    OTHEREQUITYOTHER = Field()
    CAPITALRESERVE = Field()  # 资本公积
    INVENTORYSHARE = Field()
    SPECIALRESERVE = Field()
    SURPLUSRESERVE = Field()  # 盈余公积
    GENERALRISKPREPARE = Field()
    UNCONFIRMINVLOSS = Field()
    RETAINEDEARNING = Field()  # 未分配利润
    PLANCASHDIVI = Field()
    DIFFCONVERSIONFC = Field()
    SUMPARENTEQUITY = Field()  # 归属母公司股东权益
    MINORITYEQUITY = Field()  # 少数股东权益
    SUMSHEQUITY = Field()  # 股东权益合计
    SUMLIABSHEQUITY = Field()  # 负债和股东权益合计
    

