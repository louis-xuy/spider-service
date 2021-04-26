create table stock_basic(
    id int(11) unsigned not null auto_increment comment'主键',
    code varchar(16) not null comment '股票代码',
    symbol varchar(16) not null comment '股票名称',
    fullname varchar(128) comment '中文名',
    enname varchar(128) comment '英文全称',
    cnspell varchar(64) comment '拼音缩写',
    area varchar(20) comment '地域',
    province varchar(20) comment '省份',
    address varchar(128) comment '地址',
    industry_name varchar(16) comment '所属行业',
    industry_code varchar(16) comment '所属行业',
    sector_code_cn varchar(16) comment '所属行业',
    board_type varchar(16) comment '板块类型（主板/创业板/科创板/CDR）',
    exchange varchar(16) comment '交易所代码',
    curr_type varchar(16) comment '交易货币',
    status varchar(16) comment '上市状态 ’Active’ - 正常上市, ‘Delisted’ - 终止上市, ‘TemporarySuspended’ - 暂停上市,',
    listed_date varchar(16) comment '上市日期',
    de_listed_date varchar(16) comment '退市日期',
    created_datetime varchar(30) comment '创建时间',
    update_datetime varchar(30) comment '更新时间'
);


create table stock_finance_lrb(
    id int(11) unsigned not null auto_increment comment'主键',
    revenue float comment '营业总收入：公司经营所取得的收入总额金融类公司不公布营业总收入，因此 revenue 指标只能使用类似的一个指标-operating_revenue',
    operating_revenue float comment '营业收入：公司经营主要业务所取得的收入总额',
    net_interest_income float comment '利息净收入',
    net_commission_income float comment '利息净收入',
    commission_income float comment '其中:手续费及佣金收入',
    commission_expense float comment '其中:手续费及佣金支出',
    net_proxy_security_income float comment '其中:代理买卖证券业务净收入',
    sub_issue_security_income float comment '其中:证券承销业务净收入',
    net_trust_income float comment '其中:受托客户资产管理业务净收入',
    earned_premiums float comment '已赚保费',
    premiums_income float comment '保险业务收入',

    report_date varchar(30) comment '报表日期',
)





