#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 1:14

__author__ = 'xujiang@baixing.com'


import sqlite3
import os


class MySqLite(object):
    """
    SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说没有独立的维护进程，所有的维护都来自于程序本身。
    在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候连接对象会自动创建数据库文件；
    如果数据库文件已经存在，则连接对象不会再创建数据库文件，而是直接打开该数据库文件。

    对于数据库链接对象来说，具有以下操作：
        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：
        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动
        update()            --更新数据
        delete()             --删除数据

    """
    # 是否打印sql
    SHOW_SQL = True

    def __init__(self, path):
        self.path = path

    def get_conn(self):
        """
        获取数据库连接
        """
        try:
            conn = sqlite3.connect(self.path)

            """
            该参数是为了解决一下错误：
            ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str).
            It is highly recommended that you instead just switch your application to Unicode strings.
            """
            # conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
            conn.text_factory = str
            if os.path.exists(self.path) and os.path.isfile(self.path):
                print('硬盘上面:[{}]'.format(self.path))
                return conn
        except sqlite3.OperationalError as e:
            print("Error:%s" % e)

    def get_cursor(self, conn):
        """
        该方法是获取数据库的游标对象，参数为数据库的连接对象
        """
        if conn is not None:
            return conn.cursor()
        else:
            return self.get_conn().cursor()


    def close_all(self, conn, cu):
        """
        关闭数据库游标对象和数据库连接对象
        """
        try:
                cu.close()
                conn.close()
        except sqlite3.OperationalError as e:
            print("Error:%s" % e)


    def create_table(self, sql):
        """
        创建数据库表
        """
        if sql is not None and sql != '':
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            if self.SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            cu.execute(sql)
            conn.commit()
            print('创建数据库表[cndba]成功!')
            self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def drop_table(self, table):
        """
        如果表存在,则删除表
        """
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table
            if self.SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            cu.execute(sql)
            conn.commit()
            print('删除数据库表[{}]成功!'.format(table))
            cu.close()
            conn.close()
            # self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(table))

    def insert(self, sql, data):
        """
        插入数据
        """
        if sql is not None and sql != '':
            if data is not None:
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                for d in data:
                    if self.SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    conn.commit()
                self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def fetchall(self, sql):
        """
        查询所有数据
        """
        if sql is not None and sql != '':
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            if self.SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            cu.execute(sql)
            r = cu.fetchall()
            if len(r) > 0:
                for e in range(len(r)):
                    print(r[e])
            self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def fetchone(self, sql, data):
        """
        查询一条数据
        """
        if sql is not None and sql != '':
            if data is not None:
                #Do this instead
                d = (data,)
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                if self.SHOW_SQL:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                cu.execute(sql, d)
                r = cu.fetchall()
                if len(r) > 0:
                    for e in range(len(r)):
                        print(r[e])
                self.close_all(conn, cu)
            else:
                print('the [{}] equal None!'.format(data))
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def update(self, sql, data):
        """
        更新数据
        """
        if sql is not None and sql != '':
            if data is not None:
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                for d in data:
                    if self.SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    conn.commit()
                self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def delete(self, sql, data):
        """
        删除数据
        """
        if sql is not None and sql != '':
            if data is not None:
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                for d in data:
                    if self.SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    conn.commit()
                self.close_all(conn, cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))


def drop_table_test(mydb):
    '''删除数据库表测试'''
    print('删除数据库表测试...')
    mydb.drop_table('cndba')

def create_table_test(mydb):
    '''创建数据库表测试'''
    print('创建数据库表测试...')
    create_table_sql = '''
    create table stock_basic(
        id int(11) unsigned not null auto_increment comment'主键',
        code varchar(16) not null comment '股票代码',
        symbol varchar(16) not null comment '股票名称',
        fullname varchar(128) comment '中文名',
        enname varchar(128) comment '英文全称',
        cnspell varchar(64) comment '拼音缩写',
        area varchar(20) comment '地域',
        province varchar(20) comment '省份',
        province varchar(20) comment '省份',
        address varchar(128) comment '地址',
        industry_name varchar(16) comment '所属行业',
        industry_code varchar(16) comment '所属行业',
        board_type varchar(16) comment '板块类型（主板/创业板/科创板/CDR）',
        exchange varchar(16) comment '交易所代码',
        curr_type varchar(16) comment '交易货币',
        status varchar(16) comment '上市状态 ’Active’ - 正常上市, ‘Delisted’ - 终止上市, ‘TemporarySuspended’ - 暂停上市,',
        listed_date varchar(16) comment '上市日期',
        de_listed_date varchar(16) comment '上市日期',
        created_datetime varchar(30) comment '创建时间',
        update_datetime varchar(30) comment '更新时间'
    )
    '''
    mydb.create_table(create_table_sql)


def insert_test(mydb):
    """
    插入测试数据
    """
    print('保存数据测试...')
    sql = '''INSERT INTO stock values (?, ?, ?, ?, ?, ?)'''
    data = [(1, 'Dave', '男', 20, '安徽省合肥市', '123****62'),
            (2, 'cndba', '男', 22, '安徽省安庆市', '123****63'),
            (3, 'oracle', '女', 18, 'http://www.cndba.cn', '123****87'),
            (4, 'Python', '女', 21, 'http://www.cndba.cn/dave', '123****32')]
    mydb.insert(sql, data)

def fetchall_test(mydb):
    """
    查询所有数据
    """
    print('查询所有数据...')
    fetchall_sql = '''SELECT * FROM cndba'''
    mydb.fetchall(fetchall_sql)


def fetchone_test(mydb):
    """
    查询一条数据
    """
    print('查询一条数据...')
    fetchone_sql = 'SELECT * FROM cndba WHERE ID = ? '
    data = 1
    # fetchone_sql = 'SELECT * FROM cndba WHERE address = ? '
    # data = '美国'
    mydb.fetchone(fetchone_sql, data)


def update_test(mydb):
    """
    更新数据
    """
    print('更新数据...')
    update_sql = 'UPDATE cndba SET name = ? WHERE ID = ? '
    data = [('Oracle', 1),
            ('MySQL', 2)]
    mydb.update(update_sql, data)


def delete_test(mydb):
    """
    删除数据
    """
    print('删除数据...')
    delete_sql = 'DELETE FROM cndba WHERE NAME = ? AND ID = ? '
    data = [('Oracle', 1),
            ('python', 2)]
    mydb.delete(delete_sql, data)



if __name__ == '__main__':

    dbfile = 'stock_data.db'
    mydb = MySqLite(dbfile)

    create_table_test(mydb)
    # drop_table_test(mydb)
    # insert_test(mydb)
    # fetchone_test(mydb)
    # update_test(mydb)

    # delete_test(mydb)
    fetchall_test(mydb)