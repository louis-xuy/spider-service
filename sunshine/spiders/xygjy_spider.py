#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-02-11 22:54
"""

import os
import re
import sys
import threading
import time
import json
from io import BytesIO
from bs4 import BeautifulSoup as BS
import requests
from scrapy import Request, FormRequest, Spider
# from Crypto.Cipher import AES   # 用于AES解码
#from PIL import Image
from rich.progress import Progress


class Aescrypt():
    """
    加密解密
    
    """
    def __init__(self, key, model, iv):
        self.key = self.add_16(key)
        self.model = model
        self.iv = iv

    def add_16(self, par):
        if type(par) == str:
            par = par.encode()
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        if self.model == AES.MODE_CBC:
            aes = AES.new(self.key,self.model,self.iv)
        elif self.model == AES.MODE_ECB:
            aes = AES.new(self.key,self.model)
        encrypt_text = aes.encrypt(text)
        return encrypt_text

    def aesdecrypt(self, text):
        if self.model == AES.MODE_CBC:
            aes = AES.new(self.key, self.model, self.iv)
        elif self.model == AES.MODE_ECB:
            aes = AES.new(self.key, self.model)
        decrypt_text = aes.decrypt(text)
        decrypt_text = decrypt_text.strip(b"\x00")
        return decrypt_text


class ts_download():
    """
    加密的ts文件下载

    """
    
    def __init__(self, name, m3_url, header=None, cookie=None):
        self.name = name
        self._m3_url = m3_url
        self._host = m3_url[:m3_url.rfind('/') + 1]
        self._m3u8 = ''
        self._method = ''
        self._key = ''
        self._aescrypt = None
        self._header = header
        self.cookie = cookie
        self._savedir = f'/Users/jaxon/Downloads/xygjy'
    
    def get_m3u8_video(self):
        _tslist = []
        r = requests.get(self._m3_url+'?U1REMjAyMDExMTUtMDAwMDAwMDF8MTg1MDIxNTAyNzZ8NzZmODE5ZDRjMjIxZDQyMHxhOTdhN2YyNjhhOGY3Nzhi', self._header, verify=False)
        with open(f'{self._savedir}/{self.name}.m3u8', 'wb') as f:
            f.write(r.content)
        self._m3u8 = r.text
        if '#EXTM3U' not in r.text:
            print(self._m3_url)
            print(r.text)
            raise BaseException('非m3u8链接')
        
        for index, line in enumerate(r.text.split('\n')):
            if '#EXT-X-KEY' in line:
                self._method = line[line.find('METHOD=') + 7: line.find(',')]
                key_url = line[line.find('URI="') + 5:line.rfind(',') - 1]
                print('key url:', key_url)
                p_IV = re.compile('IV=(.{34})')
                IV = re.search(p_IV, line).group()
                iv = IV.replace("0x", "")[:16].encode()
                self.get_key(key_url, iv)
            if '.ts' in line:
                if line[0] == '/':
                    _tslist.append(f'{self._host}{line}')
                elif line[:4] == 'http':
                    _tslist.append(line)
                else:
                    _tslist.append(f'{self._host}{line}')
        
        with Progress() as progress:
            task = progress.add_task("[red]{} Downloading...".format(self.name), total=len(_tslist))
            for ts_url in _tslist:
                progress.update(task, advance=1)
                try:
                    self.download(ts_url)
                except Exception as e:
                    print("异常请求：%s" % e.args)
                    return
    
    def get_key(self, key_url, iv):
        """
            下载 key 文件, 并生成AES解密
        """
        param = {'get':'VTFSRU1qQXlNREV4TVRVdE1EQXdNREF3TURGOE1UZzFNREl4TlRBeU56WjhOelptT0RFNVpEUmpNakl4WkRReU1IeGhPVGRoTjJZeU5qaGhPR1kzTnpoaXwyMDE4dGR4bHh4eHRjejEtMQ'}
        r = requests.get(key_url, headers=self._header, params=param, cookies=self.cookie, verify=False)
        try:
            key = r.content.decode().strip()
        except Exception as e:
            key = r.content.decode('gbk').strip()
        print('key:', key)
        try:
            self._aescrypt = Aescrypt(key, AES.MODE_CBC, iv)  # 生成解码器，以供调用
            with open(f'{self._savedir}/{self.name}.key', 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(e)
    
    def download(self, ts_url):
        try:
            r = requests.get(ts_url, self._header, verify=False, cookies=self.cookie, timeout=120)
            content = self._aescrypt.aesdecrypt(r.content) if self._aescrypt else r.content
            # print('开始下载')
            with open(f'{self._savedir}/{self.name}.mp4', mode='ab') as f:
                f.write(content)
            return True
        except Exception as e:
            print(ts_url, e)
            raise Exception


class NewsunshineClient(object):
    """连接新阳光的工具类，维护一个Session

    用法：

    client = ZhiHuClient()

    # 第一次使用时需要调用此方法登录一次，生成cookie文件
    # 以后可以跳过这一步
    client.login("username", "password")

    # 用这个session进行其他网络操作，详见requests库
    session = client.getSession()
    """
    
    # 网址参数是账号类型
    TYPE_PHONE_NUM = "UserName"
    TYPE_EMAIL = "email"
    homeURL = r"http://www.xygjy.com"
    session_path = '/Users/jaxon/WorkSpace/spider-service/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    captchaFile = os.path.join(session_path, "captcha.jpeg")
    cookieFile = os.path.join(session_path, "cookie")

    def __init__(self):
        os.chdir(sys.path[0])  # 设置脚本所在目录为当前工作目录
        self.__session = requests.Session()
        self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
        # 若已经有 cookie 则直接登录
        self.__cookie = self.__loadCookie()
        if self.__cookie:
            print("检测到cookie文件，直接使用cookie登录")
            self.__session.cookies.update(self.__cookie)
            soup = BS(self.open(r"http://www.xygjy.com/").text, "html.parser", fromEncoding='utf-8')
            print(soup)
            print("已登陆账号： %s" % soup.find("label", for_="txtUserName"))
        else:
            print("没有找到cookie文件，请调用login方法登录一次！")

    # 登录
    def login(self, username, password):
        """
        验证码错误返回：
        {'errcode': 1991829, 'r': 1, 'data': {'captcha': '请提交正确的验证码 :('}, 'msg': '请提交正确的验证码 :('}
        登录成功返回：
        {'r': 0, 'msg': '登陆成功'}
        """
        loginURL = r"http://yc.tdxl.cn/Account/Login"
        self.__username = username
        self.__password = password
        self.__loginURL = loginURL.format(self.__getUsernameType())
        while True:
            captcha = self._get_captcha()
            # 发送POST请求
            data = {
                "Password": self.__password,
                self.__getUsernameType(): self.__username,
                "Code": captcha
            }
            # print(data)
            res = self.__session.post(self.__loginURL, data=data)
            res.encoding = 'utf-8'
            if res.json:
                print(res.content.decode('utf-8'))
            if res.json()["ErrorMessage"] == "":
                print("登录成功")
                self.__saveCookie()
                break
            else:
                print("登录失败")
                print("错误信息 --->", res.json()["ErrorMessage"])
    
    def _get_captcha(self):
        ## 获取验证码
        api = r"http://yc.tdxl.cn/Account/GetValidateCode?time={}"
        timestamp = int(time.time() * 1000)
        captcha = self.__session.get(api.format(timestamp))
        BytesIOObj = BytesIO()
        BytesIOObj.write(captcha.content)
        img = Image.open(BytesIOObj)
        # with open(self.captchaFile, 'wb') as f:
        #     f.write(captcha.content)
        #     img = Image.open(self.captchaFile)
        img_thread = threading.Thread(target=img.show, daemon=True)
        img_thread.start()
        capt = input('请输入图片里的验证码：')
        # self.__session.post(api, data={'input_text': capt})
        return capt
        
    
    def __getUsernameType(self):
        """判断用户名类型
        经测试，网页的判断规则是纯数字为phone_num，其他为email
        """
        if self.__username.isdigit():
            return self.TYPE_PHONE_NUM
        return self.TYPE_EMAIL
    
    def __saveCookie(self):
        """cookies 序列化到文件
        即把dict对象转化成字符串保存
        """
        with open(self.cookieFile, "w") as output:
            cookies = self.__session.cookies.get_dict()
            json.dump(cookies, output)
            print("=" * 50)
            print("已在同目录下生成cookie文件：", self.cookieFile)
    
    def __loadCookie(self):
        """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
        if os.path.exists(self.cookieFile):
            print("=" * 50)
            with open(self.cookieFile, "r") as f:
                cookie = json.load(f)
                return cookie
        return None
    
    def open(self, url, delay=0, timeout=10):
        """打开网页，返回Response对象"""
        if delay:
            time.sleep(delay)
        return self.__session.get(url, timeout=timeout)
    
    def getSession(self):
        return self.__session



class newSunVideoSpider(Spider):
    name = 'xygjy_video'
    #allowed_domains = ['http://xygjy.com']
    #url = 'http://bgp.xygjy.com/booksfile/TDXL2021/gs/cwgl/2021gscwgl{}/playlist.m3u8?U1REMjAyMDExMTUtMDAwMDAwMDF8MTg1MDIxNTAyNzZ8NzZmODE5ZDRjMjIxZDQyMHwyODdiNTVkMWI1MDk5NGEy'

    custom_settings = {
        'COOKIES_ENABLED': True,
    }
    
    def start_requests(self):
        print("start ...")
        nsc = NewsunshineClient()
        nsc.login('18502150276', 'xj19880512')
        self._session = nsc.getSession()
        url = 'http://yc.tdxl.cn/Account/GetModelList'
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Length': '0',
                        'Origin': 'http://yc.tdxl.cn',
                        'Referer': 'http://yc.tdxl.cn/',
                        'Accept': '*/*',
                        'Content-Type': 'application/json'}
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        self.cookies = requests.utils.dict_from_cookiejar(self._session.cookies)
        yield Request(url, method='post', callback=self._parse_home_page, headers=self.headers, cookies=self.cookies)
    
    def _parse_home_page(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'http://yc.tdxl.cn',
            'Referer': 'http://yc.tdxl.cn/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Language': 'zh-CN,zh;q=0.9'
            }
        #api = 'http://yc.tdxl.cn/Learning/MyCourses/MyCoursewaresLearningList'
        api = 'http://yc.xygjy.com/Learning/MyCourses/MyCoursewaresLearningList'
        resp = response.json()
        for d in resp:
            v = d.get('AccountClassCourses', None)
            if v:
                v = v[0]
                sjt_id = v.get('sjt_Id')
                treeData = v.get('TreeData', [])
                if treeData:
                    treeData = json.loads(re.sub(r'\b([^:",]+)(?=:)', r'"\1"', re.sub(r'\s*|,\s*(?=\}$)', '', treeData)))
                    for course in treeData:
                        nid = course.get('nid')
                        text = course.get('text')
                        data = {
                                'scl_Id': sjt_id,
                                'cls_Id': '',
                                'sjt_Id': nid,
                                'sjt_CName': text,
                                'start': '0',
                                'limit': '100'
                        }
                        yield FormRequest(api, method='POST', formdata=data, cookies=self.cookies,
                                            headers=headers, callback=self.parse, dont_filter=True)
    
                
    def parse(self, response, **kwargs):
        header = {
            'Host': 'bgp.xygjy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            
        }
        resp = response.json()
        results = resp.get('results')
        for row in resp.get('rows'):
            cls_Id = row['cls_Id']
            crw_CName = row['crw_CName']
            crw_FileSize = row['crw_FileSize']
            crw_PlayTime = row['crw_PlayTime']
            crw_VisitLocation = row['crw_VisitLocation']
            crw_DownloadLocation = row['crw_DownloadLocation']
            ts = ts_download(crw_CName, crw_VisitLocation, cookie=self.cookies)
            ts.get_m3u8_video()
    
    
    def parse_item(self, response):
        start_list = []
        #tp = ThreadPool(10)
        body = response.text
        rows = body.json.rows
        for row in rows:
            scl_Id = row['scl_Id']
            name = row['crw_CName']
            fileSize = row['crw_FileSize']
            playTime = row['crw_PlayTime']
            visitLocation = row['crw_VisitLocation']
            downloadLocation = row['crw_DownloadLocation']
            FileMemo = row['FileMemo']
            #m3 = xyg_download(name, downloadLocation, header)
            # tp.set_tasks(m3.get_m3u8_video, )
            # res = tp.final_results()

