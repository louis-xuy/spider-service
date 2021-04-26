#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-01-15 17:49

这个文件用来启动，重启，关闭mongodb

# os : win64
# __init__:初始化，获取mongodb程序和配置文件路径
# GetPid：调用__QueryMongoPid，获取mongodb的进程pid
# OnlyStart：调用__StartMongo，启动mongod
# StopMongo：强制结束mongod
# Restart：重启mongod

"""

import os
import subprocess
import sys
import time
import signal
from db_init import mongodb_conf_init


class MongdbStart(object):

    def __init__(self):
        mongodb_conf = mongodb_conf_init()
        tip = mongodb_conf.mongodb_conf_init()
        if not tip:
            print('mongodb 配置文件写入失败')
            exit()
        self.MONGO_BIN_MONGOD = os.path.join(mongodb_conf.MONGO_BIN, "mongod")
        self.MONGO_CONF_MONGOD = os.path.join(mongodb_conf.MONGO_HOME, "mongodb.conf")

    def __QueryMongoPid(self):
        # 返回查询的MongoDB的pid的对象
        #cmd = 'tasklist /fi "imagename eq mongod.exe"'
        cmd = 'tasklist /fi "imagename eq mongod.exe"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        s1 = subprocess.getoutput(cmd)
        #print(s1)
        if 'PID' not in s1:
            print('mongodb is not running...')
        else:
            tmp0 = s1.split('\n')
            tmp1 = tmp0[-1].replace(' ', '')
            tmp2 = tmp1.split('Console', 1)[0]
            app_pid = tmp2.split('.exe')[1]
            return app_pid
        #return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    def GetPid(self):
        # 返回pid结果
        return self.__QueryMongoPid()

    def __StartMongo(self):
        # 启动MongoDB
        #print(self.MONGO_BIN_MONGOD)
        cmd = [self.MONGO_BIN_MONGOD, '-f', self.MONGO_CONF_MONGOD]
        print("Mongodb Starting ....")
        return subprocess.Popen(cmd)

    def StopMongo(self):
        # 停止MongoDB
        print("Stop Mongdb......")
        time.sleep(2)
        pid = self.GetPid()
        if pid:
            # 假如有pid则强制杀死
            #os.kill(int(pid), signal.SIGKILL)
            os.popen('taskkill.exe /F  /pid:' + str(pid))
            print("mongod is stopped")
        else:
            print("mongo is not running")

    def OnlyStart(self):
        # 　启动MongoDB
        result = self.GetPid()
        #print("mongodb is starting")
        if result:
            print("程序已在运行, pid为：", result)
        else:
            self.__StartMongo()
            print("mongodb is running")
            print('mongodb pid :', self.GetPid())

    def Restart(self):
        # 重启MongoDB
        self.StopMongo()
        result = self.GetPid()
        if result:
            return "程序未退出，请重新停止"
        time.sleep(3)
        print(result, 11111)
        self.__StartMongo()
        result = self.GetPid()
        if result:
            print("程序的pid为：", result)

#     def ActionJudge(self):
#         # 启动参数选择
#         CHOICE = ['start', 'restart', 'stop']
#         while 1:
#             action = sys.argv[1]
#             if action in CHOICE:
#                 return action
#             else:
#                 print("您输入有误，请重新输入，可选：{}".format(CHOICE))
#
#
if __name__ == '__main__':
    mongo = MongdbStart()
    #启动，如果想使用注释掉的方法，请注释掉下边这句
    mongo.OnlyStart()
    # action = mongo.ActionJudge()
    # if action == 'start':
    #     mongo.OnlyStart()
    # elif action == 'restart':
    #     mongo.Restart()
    # elif action == 'stop':
    #     mongo.StopMongo()