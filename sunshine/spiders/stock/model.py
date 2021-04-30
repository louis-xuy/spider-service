#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 11:14
"""


from sqlalchemy import Column, Integer, String, Float
from sunshine.db.basic import Base



# 股票基本信息
class StockInfo(dict, Base):
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


class TradeDays(Base):
    __tablename__ = 'trade_days'
    
    id = Column(Integer, primary_key=True)
    exchange = Column(String(16))
    cal_date = Column(String(16))
    is_open = Column(String(16))


class DailyStockData(dict, Base):
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


class SuspendedDays(dict, Base):
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


class IndexComponents(dict, Base):
    """
    指数成分和权重信息
    """
    __tablename__ = 'index_components'

    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    con_code = Column(String(16))
    trade_date = Column(String(16))
    weight = Column(String(16))



class FinanceStockProfit():
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