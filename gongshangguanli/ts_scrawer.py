#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-18 12:49
"""

import os
import re
import sys
import time
import json
import requests
import shutil
from Crypto.Cipher import AES   # 用于AES解码
from rich.progress import Progress
from bs4 import BeautifulSoup as BS

from sunshine.spiders.xygjy_spider import NewsunshineClient, ts_download

# requests.urllib3.disable_warnings()
#
# # 创建路径，先破后立
# def mkdir(path):
#     if os.path.exists(path):
#         shutil.rmtree(path)
#     os.mkdir(path)
    

# class NewsunshineClient(object):
#
#     """连接新阳光的工具类，维护一个Session
#
#     用法：
#
#     client = ZhiHuClient()
#
#     # 第一次使用时需要调用此方法登录一次，生成cookie文件
#     # 以后可以跳过这一步
#     client.login("username", "password")
#
#     # 用这个session进行其他网络操作，详见requests库
#     session = client.getSession()
#     """
#
#     # 网址参数是账号类型
#     TYPE_PHONE_NUM = "UserName"
#     TYPE_EMAIL = "email"
#     loginURL = r"http://yc.tdxl.cn/Account/Login"
#     homeURL = r"http://www.xygjy.com"
#     captchaURL = r"http://yc.tdxl.cn/Account/GetValidateCode?time={}"
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
#         "X-Requested-With": "XMLHttpRequest",
#     }
#
#     captchaFile = os.path.join(sys.path[0], "captcha.jpeg")
#     cookieFile = os.path.join(sys.path[0], "cookie")
#
#     def __init__(self):
#         os.chdir(sys.path[0])  #设置脚本所在目录为当前工作目录
#
#         self.__session = requests.Session()
#         self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
#         # 若已经有 cookie 则直接登录
#         self.__cookie = self.__loadCookie()
#         if self.__cookie:
#             print("检测到cookie文件，直接使用cookie登录")
#             self.__session.cookies.update(self.__cookie)
#             soup = BS(self.open(r"http://www.xygjy.com/").text, "html.parser")
#             print("已登陆账号： %s" % soup.find("label", for_="txtUserName"))
#         else:
#             print("没有找到cookie文件，请调用login方法登录一次！")
#
#
#     # 登录
#     def login(self, username, password):
#         """
#         验证码错误返回：
#         {'errcode': 1991829, 'r': 1, 'data': {'captcha': '请提交正确的验证码 :('}, 'msg': '请提交正确的验证码 :('}
#         登录成功返回：
#         {'r': 0, 'msg': '登陆成功'}
#         """
#         self.__username = username
#         self.__password = password
#         self.__loginURL = self.loginURL.format(self.__getUsernameType())
#         # 随便开个网页，获取登陆所需的_xsrf
#         html = self.open(self.loginURL).text
#         local_time = int(time.time() * 1000)
#         soup = BS(html, "html.parser")
#         # 下载验证码图片
#         while True:
#             print(self.captchaURL.format(local_time))
#             captcha = self.open(self.captchaURL.format(local_time)).content
#
#             with open(self.captchaFile, "wb") as output:
#                 output.write(captcha)
#             # im = Image.open(self.captchaFile)
#             # im.show()
#             # 人眼识别
#             print("=" * 50)
#             print("已打开验证码图片，请识别！")
#             #subprocess.call(self.captchaFile, shell=True)
#             captcha = input("请输入验证码：")
#             os.remove(self.captchaFile)
#             # 发送POST请求
#             data = {
#                 "Password": self.__password,
#                 self.__getUsernameType(): self.__username,
#                 "Code": captcha
#             }
#             #print(data)
#             res = self.__session.post(self.__loginURL,data=data)
#             print("=" * 50)
#             # print(res.text) # 输出脚本信息，调试用
#             print(res.encoding)
#             res.encoding = 'utf-8'
#             if res.json:
#                 print(res.content.decode('utf-8'))
#             if res.json()["ErrorMessage"] == "":
#                 print("登录成功")
#                 self.__saveCookie()
#                 break
#             else:
#                 print("登录失败")
#                 print("错误信息 --->", res.json()["ErrorMessage"])
#
#     def __getUsernameType(self):
#         """判断用户名类型
#         经测试，网页的判断规则是纯数字为phone_num，其他为email
#         """
#         if self.__username.isdigit():
#             return self.TYPE_PHONE_NUM
#         return self.TYPE_EMAIL
#
#     def __saveCookie(self):
#         """cookies 序列化到文件
#         即把dict对象转化成字符串保存
#         """
#         with open(self.cookieFile, "w") as output:
#             cookies = self.__session.cookies.get_dict()
#             json.dump(cookies, output)
#             print("=" * 50)
#             print("已在同目录下生成cookie文件：", self.cookieFile)
#
#     def __loadCookie(self):
#         """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
#         if os.path.exists(self.cookieFile):
#             print("=" * 50)
#             with open(self.cookieFile, "r") as f:
#                 cookie = json.load(f)
#                 return cookie
#         return None
#
#     def open(self, url, delay=0, timeout=10):
#         """打开网页，返回Response对象"""
#         if delay:
#             time.sleep(delay)
#         return self.__session.get(url, timeout=timeout)
#
#     def getSession(self):
#         return self.__session


# class Aescrypt():
#     def __init__(self, key, model, iv):
#         self.key = self.add_16(key)
#         self.model = model
#         self.iv = iv
#
#     def add_16(self, par):
#         if type(par) == str:
#             par = par.encode()
#         while len(par) % 16 != 0:
#             par += b'\x00'
#         return par
#
#     def aesencrypt(self, text):
#         text = self.add_16(text)
#         if self.model == AES.MODE_CBC:
#             aes = AES.new(self.key,self.model,self.iv)
#         elif self.model == AES.MODE_ECB:
#             aes = AES.new(self.key,self.model)
#         encrypt_text = aes.encrypt(text)
#         return encrypt_text
#
#     def aesdecrypt(self, text):
#         if self.model == AES.MODE_CBC:
#             aes = AES.new(self.key, self.model, self.iv)
#         elif self.model == AES.MODE_ECB:
#             aes = AES.new(self.key, self.model)
#         decrypt_text = aes.decrypt(text)
#         decrypt_text = decrypt_text.strip(b"\x00")
#         return decrypt_text


# class ts_download():
#     """
#     加密的ts文件下载
#
#     """
#     def __init__(self, name, m3_url, header):
#         self.name = name
#         self._m3_url = m3_url
#         self._host = m3_url[:m3_url.rfind('/')+1]
#         self._m3u8 = ''
#         self._method = ''
#         self._key = ''
#         self._aescrypt = None
#         self._header = header
#         self._savedir = f'tsfiles/'
#
#     def get_m3u8_video(self):
#         _tslist = []
#         r = requests.get(self._m3_url, self._header, verify=False)
#         with open(f'{self._savedir}{self.name}.m3u8', 'wb') as f:
#             f.write(r.content)
#         self._m3u8 = r.text
#         if '#EXTM3U' not in r.text:
#             raise BaseException('非m3u8链接')
#
#         for index, line in enumerate(r.text.split('\n')):
#             if '#EXT-X-KEY' in line:
#                 self._method = line[line.find('METHOD=') + 7: line.find(',')]
#                 key_url = line[line.find('URI="') + 5:line.rfind(',')-1]
#                 print('key url:',key_url)
#                 p_IV = re.compile('IV=(.{34})')
#                 IV = re.search(p_IV, line).group()
#                 iv = IV.replace("0x", "")[:16].encode()
#                 self.get_key(key_url, iv)
#             if '.ts' in line:
#                 if line[0] == '/':
#                     _tslist.append(f'{self._host}{line}')
#                 elif line[:4] == 'http':
#                     _tslist.append(line)
#                 else:
#                     print(f'{self._m3_url[:self._m3_url.rfind("/") + 1]}{line}')
#                     _tslist.append(f'{self._host}{line}')
#
#         with Progress() as progress:
#             task = progress.add_task("[red]Downloading...", total=len(_tslist))
#             for ts_url in _tslist:
#                 progress.update(task, advance=1)
#                 ts_download.download(self, ts_url)
#
#     def get_key(self, key_url, iv):
#         """
#             下载 key 文件, 并生成AES解密
#         """
#         r = requests.get(key_url, headers=self._header, verify=False)
#         try:
#             key = r.content.decode().strip()
#         except Exception as e:
#             key = r.content.decode('gbk').strip()
#         print('key:', key)
#         try:
#             self._aescrypt = Aescrypt(key, AES.MODE_CBC, iv)  # 生成解码器，以供调用
#             with open(f'{self._savedir}{self.name}.key', 'wb') as f:
#                 f.write(r.content)
#         except Exception as e:
#             print(url, e)
#
#
#     def download(self, ts_url):
#         try:
#             r = requests.get(ts_url, self._header, verify=False, timeout=120)
#             content = self._aescrypt.aesdecrypt(r.content) if self._aescrypt else r.content
#             # print('开始下载')
#             with open(f'{self._savedir}{self.name}.mp4', mode='ab') as f:
#                 f.write(content)
#             print('下载 %s 完成' % ts_url)
#             return True
#         except Exception as e:
#             print(ts_url, e)
#             return False
    

# def app_master(data_tuple, headers):
#     start_list = []
#     for name, u in data_tuple:
#         print(name, u)
#         web_info_list = xyg_download(name, u, headers)
#         time.sleep(1)
#         t = Thread(target=web_info_list.get_m3u8_video)
#         start_list.append(t)
#     for t in start_list:
#         t.start()
#     for t in start_list:
#         t.join()

def main():
    nsc = NewsunshineClient()
    nsc.login('18502150276', 'xj19880512')
    cookies = requests.utils.dict_from_cookiejar(nsc.getSession().cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://yc.tdxl.cn',
        'Referer': 'http://yc.tdxl.cn/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    api = 'http://yc.xygjy.com/Learning/MyCourses/MyCoursewaresLearningList'
    data = {
        'scl_Id': 'SCL20201115-00000001',
        'cls_Id': '',
        'sjt_Id': 'SJT20200605-00000028',
        'sjt_CName': '同等学力英语-翻译',
        'start': '0',
        'limit': '100'
    }
    
    response = requests.post(api, data=data, cookies=cookies, headers=headers)
    resp = response.json()
    results = resp.get('results')
    for row in resp.get('rows'):
        cls_Id = row['cls_Id']
        crw_CName = row['crw_CName']
        crw_FileSize = row['crw_FileSize']
        crw_PlayTime = row['crw_PlayTime']
        crw_VisitLocation = row['crw_VisitLocation']
        crw_DownloadLocation = row['crw_DownloadLocation']
        print(crw_CName, crw_FileSize, crw_PlayTime)
        ts = ts_download(crw_CName, crw_VisitLocation, cookie=cookies)
        ts.get_m3u8_video()

if __name__ == "__main__":
    main()