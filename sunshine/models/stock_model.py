#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 11:14
"""


from sqlalchemy import Column, Integer, String, Float
from . import Base
# from scrapy_sqlitem.sqlitem import SqlAlchemyItemMeta


class TradeDays(Base):
    __tablename__ = 'trade_days'

    id = Column(Integer, primary_key=True)
    exchange = Column(String(16))
    cal_date = Column(String(16))
    is_open = Column(String(16))

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


# 股票基本信息
class StockInfo(Base):
    __tablename__ = 'stock_info'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    industry_code = Column(String(10))
    market_tplus = Column(Integer)
    symbol = Column(String(16))
    special_type = Column(String(16))
    exchange = Column(String(16))
    status = Column(String(16))
    type = Column(String(16))
    listed_date = Column(String(16))
    de_listed_date = Column(String(16))
    sector_code_name = Column(String(16))
    abbrev_symbol = Column(String(16))
    sector_code = Column(String(50))
    round_lot = Column(Integer)
    trading_hours = Column(String(50))
    board_type = Column(String(50))
    industry_name = Column(String(16))
    trading_code = Column(String(5))
    fullname = Column(String(64))
    area = Column(String(16))
    total_capital = Column(Integer)
    current_capital = Column(Integer)

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return self.code

# 股票额外信息
class ListedStockInfoExt(Base):
    # 表的名字:
    __tablename__ = 'listed_stock_info_ext'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(16))
    name = Column(String(16))
    industry = Column(String(16))
    area = Column(String(16))
    trade_date = Column(String(16))
    list_date = Column(String(16))
    pe = Column(Float)
    float_share = Column(Float)
    total_share = Column(Float)
    total_assets = Column(Float)
    liquid_assets = Column(Float)
    fixed_assets = Column(Float)
    reserved = Column(Float)
    reserved_pershare = Column(Float)
    eps = Column(Float)
    bvps = Column(Float)
    pb = Column(Float)
    undp = Column(Float)
    per_undp = Column(Float)
    rev_yoy = Column(Float)
    profit_yoy = Column(Float)
    gpr = Column(Float)
    npr = Column(Float)
    holder_num = Column(Integer)


class DailyStockData(Base):
    __tablename__ = 'daily_stock'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    datetime = Column(String(16))
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    pre_close = Column(Float)
    volume = Column(Float)
    money = Column(Float)
    turnover = Column(Float)
    
    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class SuspendedDays(Base):
    """停牌信息"""
    __tablename__ = 'suspended_days'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    suspend_date = Column(String(16))
    suspend_timing = Column(String(16))
    suspend_type = Column(String(16))
    
    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class IndexComponents(Base):
    """
    指数成分和权重信息
    """
    __tablename__ = 'index_components'

    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    con_code = Column(String(16))
    trade_date = Column(String(16))
    weight = Column(String(16))



class FinanceStockProfitStatement(Base):
    """
    财务报表-利润表
    """
    __tablename__ = 'profit_flow'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(16))
    revenue = Column(Float)
    operating_revenue = Column(Float)
    net_interest_income = Column(Float)
    net_commission_income = Column(Float)
    commission_income = Column(Float)
    commission_expense = Column(Float)
    net_proxy_security_income = Column(Float)
    sub_issue_security_income = Column(Float)
    net_trust_income = Column(Float)
    earned_premiums = Column(Float)
    premiums_income = Column(Float)
    reinsurance_income = Column(Float)
    reinsurance = Column(Float)
    unearned_premium_reserve = Column(Float)
    total_expense = Column(Float)
    operating_expense = Column(Float)
    refunded_premiums = Column(Float)
    compensation_expense = Column(Float)
    amortization_expense = Column(Float)
    premium_reserve = Column(Float)
    amortization_premium_reserve = Column(Float)
    policy_dividend_payout = Column(Float)
    reinsurance_cost = Column(Float)
    other_operating_revenue = Column(Float)
    other_operating_cost = Column(Float)
    r_n_d = Column(Float)
    other_net_income = Column(Float)
    net_open_hedge_income = Column(Float)
    other_revenue = Column(Float)
    gredit_asset_impairment = Column(Float)
    o_n_a_expense = Column(Float)
    amortization_reinsurance_cost = Column(Float)
    insurance_commission_expense = Column(Float)
    disposal_income_on_asset = Column(Float)
    cost_of_goods_sold = Column(Float)
    sales_tax = Column(Float)
    gross_profit = Column(Float)
    selling_expense = Column(Float)
    ga_expense = Column(Float)
    financing_expense = Column(Float)
    financing_interest_income = Column(Float)
    financing_interest_expense = Column(Float)
    exchange_gains_or_losses = Column(Float)
    profit_from_operation = Column(Float)
    invest_income_associates = Column(Float)
    fair_value_change_income = Column(Float)
    investment_income = Column(Float)
    asset_impairment = Column(Float)
    interest_income = Column(Float)
    interest_expense = Column(Float)
    non_operating_revenue = Column(Float)
    non_operating_expense = Column(Float)
    disposal_loss_on_asset = Column(Float)
    other_effecting_total_profits_items = Column(Float)
    profit_before_tax = Column(Float)
    income_tax = Column(Float)
    unrealised_investment_loss = Column(Float)
    other_effecting_net_profits_items = Column(Float)
    net_profit = Column(Float)
    non_recurring_pnl = Column(Float)
    net_profit_deduct_non_recurring_pnl = Column(Float)
    classified_by_continuity_operation = Column(Float)
    continuous_operation_net_profit = Column(Float)
    discontinued_operation_net_profit = Column(Float)
    classified_by_ownership = Column(Float)
    net_profit_parent_company = Column(Float)
    minority_profit = Column(Float)
    other_income = Column(Float)
    other_income_unclassified_income_statement = Column(Float)
    remearsured_other_income = Column(Float)
    other_income_equity_unclassified_income_statement = Column(Float)
    other_equity_instruments_change = Column(Float)
    corporate_credit_risk_change = Column(Float)
    other_income_classified_income_statement = Column(Float)
    other_income_equity_classified_income_statement = Column(Float)
    financial_asset_available_for_sale_change = Column(Float)
    financial_asset_hold_to_maturity_change = Column(Float)
    cash_flow_hedging_effective_portion = Column(Float)
    foreign_currency_statement_converted_difference = Column(Float)
    others = Column(Float)
    other_debt_investment_change = Column(Float)
    assets_reclassified_other_income = Column(Float)
    other_debt_investment_reserve = Column(Float)
    other_income_minority = Column(Float)
    total_income = Column(Float)
    total_income_parent_company = Column(Float)
    total_income_minority = Column(Float)
    basic_earnings_per_share = Column(Float)
    fully_diluted_earnings_per_share = Column(Float)
    report_date = Column(String(10))

# class FinanceStockCashFlowStatement(Base):
#     __tablename__ = 'cash_flow'
#     pass
    # cash_received_from_sales_of_goods, # 销售商品、提供劳务收到的现金： 公司销售商品、提供劳务实际收到的现金 :investopedia(opens new window)
    # refunds_of_taxes	# 收到的税费返还： 公司按规定收到的增值税、所得税等税费返还额 :mba(opens new window)
    # net_deposit_increase	客户存款和同业存放款项净增加额
    # net_increase_from_central_bank	向中央银行借款净增加额
    # net_increase_from_other_financial_institutions	向其他金融机构拆入资金净增加额
    # draw_back_canceled_loans	收回已核销贷款
    # cash_received_from_interests_and_commissions	收取利息、手续费及佣金的现金
    # net_increase_from_disposing_financial_assets	处置交易性金融资产净增加额
    # net_increase_from_repurchasing_business	回购业务资金净增加额
    # cash_received_from_original_insurance	收到原保险合同保费取得的现金
    # cash_received_from_reinsurance	收到再保业务现金净额
    # net_increase_from_insurer_deposit_investment	保户储金及投资款净增加额
    # net_increase_from_financial_institutions	拆入资金净增加额
    # cash_received_from_proxy_security	代理买卖证券收到的现金净额
    # cash_received_from_sub_issue_security	代理承销证券收到的现金净额
    # cash_from_other_operating_activities	收到其它与经营活动有关的现金：公司除了上述各项目外，收到的其他与经营活动有关的现金，
    # 如捐赠现金收入、罚款收入、流动资产损失中由个人赔偿的现金收入等 :mba(opens new window)
    # cash_from_operating_activities	经营活动现金流入小计
    # cash_paid_for_goods_and_services	购买商品、接受劳务支付的现金： 公司购买商品、接受劳务实际支付的现金 :investopedia(opens new window)
    # assets_depreciation_reserves	资产减值准备
    # exchange_rate_change_effect	汇率变动对现金及现金等价物的影响
    # other_effecting_cash_equivalent_items	影响现金及现金等价物的其他科目
    # cash_equivalent_increase	现金及现金等价物净增加额（来源现金流量表主表）
    # begin_period_cash_equivalent	加:期初现金及现金等价物余额
    # end_period_cash_equivalent	期末现金及现金等价物余额
    # cash_paid_for_employee	支付给职工以及为职工支付的现金： 公司实际支付给职工，以及为职工支付的现金，
    # 包括本期实际支付给职工的工资、奖金、各种津贴和补贴等 :mba(opens new window)
    # cash_paid_for_taxes	支付的各项税费： 反映企业按规定支付的各种税费，包括本期发生并支付的税费，以及本期支付以前各期发生的税费和预交的税金等 :mba(opens new window)
    # net_increase_from_loans_and_advances	客户贷款及垫款净增加额
    # net_increase_from_central_bank_and_banks	存放中央银行和同业款项净增加额
    # net_increase_from_lending_capital	拆出资金净增加额
    # cash_paid_for_comissions	支付手续费及佣金的现金
    # cash_paid_for_orignal_insurance	支付原保险合同赔付款项的现金
    # cash_paid_for_reinsurance	支付再保业务现金净额
    # cash_paid_for_policy_dividends	支付保单红利的现金
    # net_increase_from_trading_financial_assets	为交易目的而持有的金融资产净增加额
    # net_increase_from_operating_buy_back	返售业务资金净增加额(经营)
    # cash_paid_for_other_operation_activities	支付其他与经营活动有关的现金： 反映企业支付的其他与经营活动有关的现金支出，
    # 如罚款支出、支付的差旅费、业务招待费的现金支出、支付的保险费等 :mba(opens new window)
    # cash_paid_for_operation_activities	经营活动现金流出小计
    # cash_flow_from_operating_activities	经营活动产生的现金流量净额： 指企业投资活动和筹资活动以外的所有交易活动和事项的现金流入和流出量 :mba(opens new window)
    # cash_received_from_disposal_of_investment	收回投资收到的现金
    # cash_received_from_investment	取得投资收益收到的现金
    # cash_received_from_disposal_of_asset	处置固定资产、无形资产和其他长期资产收回的现金净额： 公司处置固定资产、无形资产和其他长期资产收回的现金 :investopedia(opens new window)
    # cash_received_from_other_investment_activities	收到其他与投资活动有关的现金： 公司除了上述各项以外，收到的其他与投资活动有关的现金 :mba(opens new window)
    # cash_received_from_investment_activities	投资活动现金流入小计
    # cash_paid_for_asset	购建固定资产、无形资产和其他长期资产所支付的现金 :wikipedia(opens new window)
    # cash_paid_to_acquire_investment	投资支付的现金： 反映企业进行权益性投资和债权性投资支付的现金，
    # 包括企业取得的除现金等价物以外的股票投资和债券投资等支付的现金等 :mba(opens new window)
    # cash_paid_for_other_investment_activities	支付其他与投资活动有关的现金： 反映企业除了上述各项以外，支付的其他与投资活动有关的现金流出 :mba(opens new window)
    # cash_paid_for_investment_activities	投资活动产生的现金流出小计
    # cash_flow_from_investing_activities	投资活动产生的现金流量净额：指企业长期资产的购建和对外投资活动（不包括现金等价物范围的投资）的现金流入和流出量 :mba(opens new window)
    # cash_received_from_investors	吸收投资收到的现金：反映企业收到的投资者投入现金，包括以发行股票、债券等方式筹集的资金实际收到的净额 :mba(opens new window)
    # cash_received_from_minority_invest_subsidiaries	其中:子公司吸收少数股东投资收到的现金
    # cash_received_from_issuing_security	发行债券收到的现金
    # cash_received_from_financial_institution_borrows	取得借款收到的现金： 公司向银行或其他金融机构等借入的资金 :mba(opens new window)
    # cash_received_from_issuing_equity_instruments	发行其他权益工具收到的现金
    # net_increase_from__financing_buy_back	回购业务资金净增加额(筹资)
    # cash_received_from_other_financing_activities	收到其他与筹资活动有关的现金：反映企业收到的其他与筹资活动有关的现金流入，如接受现金捐赠等 :mba(opens new window)
    # cash_received_from_financing_activities	筹资活动现金流入小计
    # cash_paid_for_debt	偿还债务支付的现金：公司以现金偿还债务的本金，包括偿还银行或其他金融机构等的借款本金、偿还债券本金等 :mba(opens new window)
    # cash_paid_for_dividend_and_interest	分配股利、利润或偿付利息支付的现金：反映企业实际支付给投资人的利润以及支付的借款利息、债券利息等 :mba(opens new window)
    # dividends_paid_to_minority_by_subsidiaries	其中:子公司支付给少数股东的股利、利润或偿付的利息
    # cash_paid_for_other_financing_activities	支付其他与筹资活动有关的现金：反映企业支付的其他与筹资活动有关的现金流出 :mba(opens new window)
    # cash_paid_to_financing_activities	筹资活动现金流出小计
    # cash_flow_from_financing_activities	筹资活动产生的现金流量净额：指企业接受投资和借入资金导致的现金流入和流出量 :mba(opens new window)
    # net_cash_deal_from_sub	处置子公司及其他营业单位收到的现金净额
    # net_cash_payment_from_sub	取得子公司及其他营业单位支付的现金净额
    # net_increase_in_pledge_loans	质押贷款净增加额
    # net_increase_from_investing_buy_back	返售业务资金净增加额(投资)
    # net_inc_cash_and_equivalents	现金及现金等价物净增加额（来源为财务附注）
    # fixed_asset_depreciation	固定资产折旧
    # deferred_expense_amortization	长期待摊费用摊销
    # intangible_asset_amortization	无形资产摊销'
