#!/usr/bin/python
#coding=utf8
__author__ = 'MR.SJ'
import json
import certifi
import pycurl
import StringIO
import random
import Queue
import os
import datetime
import thread
import logging

_limit_time = datetime.timedelta(0,0,0,0,0,12,0)
class _log_module():
       def __init__(self, log_level=1, file_dst=None):
           self.LEVEL = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
           print self.LEVEL[log_level]   
           self.zpoc_log = file_dst
           self.log_level = log_level
           self.write_fd = None 
           # If the log file is not specify by User, Use Default path : ./log/zpoc_log_xxx,log
           if self.zpoc_log is None:
               tmp = os.path.join(os.getcwd(), 'log')
               if not os.path.exists(tmp) :
                   os.mkdir(tmp)
               name_day = str(datetime.datetime.now())[:10]
               self.zpoc_log = os.path.join(os.getcwd(), os.path.join('log', 'zpoc_log_{}.log'.format(name_day)))
               if not os.path.exists(self.zpoc_log) :
                   f = open(self.zpoc_log, 'w')
                   f.close()
           try:
               # Config the logging Engine 
               logging.basicConfig(filename=self.zpoc_log, level=self.LEVEL[log_level], format='[%(levelname)s](%(asctime)s) in %(filename)s:line %(lineno)d : %(message)s')
           except Exception:
               self.writefd = sys.stderr
               print 'Open Log file Fail!'
       
       def clear(self):
           with open(self.zpoc_log, 'w') as target:
               pass

       @staticmethod
       # Default Logging For INFO Level
       def log(message):
           logging.info(message)

       @staticmethod
       def log_level(message, level=1):
           if level is 1:
               logging.info(message)
           elif level is 0:
               logging.debug(message)
           elif level is 2:
               logging.warning(message)
           elif level is 3:
               logging.error(message)
           else:
               logging.critical(message)
    
       
class ZoomEye():
    # 实现单例模式，保证只有一个实例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ZoomEye, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    # 构造方法，完成成员变量初始化
    def __init__(self, username, password):
        self.API_TOKEN = None
        self.url = 'https://api.zoomeye.org/user/login'
        self.user_name = username
        self.password = password
        self.data = {
            "username": self.user_name,
            "password": self.password
        }
        self.fname = ''
        self.post_data = json.dumps(self.data)
        self.port = ''
        self.facets = ''
        self.ip_list = []
        self.ip_queue = Queue.Queue(-1)
        # logging The Message
        logs = _log_module()

    #实现登录模块
    def login(self):
        token=self.load_token()
        if token:
            self.API_TOKEN=token
        else:
            self._login()
        return

    #登录模块具体实现
    def _login(self):
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.URL, self.url)
            b = StringIO.StringIO()
            c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CUSTOMREQUEST, "POST")
            c.setopt(pycurl.POSTFIELDS, self.post_data)
            c.perform()
            if b.getvalue():
                print 'success login'
                self.API_TOKEN = json.loads(b.getvalue())["access_token"]
                self.save_token()
            else:
                print 'success fail,get null result'
            print self.API_TOKEN
            b.close()
            c.close()
        except pycurl.E_HTTP_POST_ERROR:
            print pycurl.E_HTTP_POST_ERROR
        except Exception as e:
            print 'please check your password or username'
            print e.message
            pass

    #搜索模块实现
    def _search(self, port, page, facets, poc_name):
        self.port = port
        self.facets = facets
        if page > 0:
            for i in range(1, int(page) + 1):
                url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port, i, facets)
                print '_get_url'
                data = self._get_url(url)
                self._parse_json(data)
            self._write_file()
        else:
            print 'page not be <0'
            pass
        #thread.exit_thread()
        if self.fname and poc_name:
            os.system('python pocsuite.py -r {} -f {}'.format(poc_name, self.fname))
        else:
            print 'args error'

    #基于多线程的搜索模块
    def run_fast(self, port, page, facets):
        for i in range(page):
            thread.start_new_thread(self._search(port, page, facets), (i, i))

    #根据输入参数得到
    def search_url(self, port, page, facets):
        url = 'https://api.zoomeye.org/host/search?query='
        flag = False
        if port != 0:
            url.join('"port:%s"' % port)
            flag = True
        if page:
            if flag:
                url.join('&page=%s' % page)
            else:
                url.join('page=%s' % page)
            flag = True
        else:
            flag = False
        if facets:
            if flag:
                url.join('&facets=%s' % facets)
            else:
                url.join('facets=%s' % facets)

        return url

    #封装的请求模块
    def _get_url(self, url):
        if self.API_TOKEN == None:
            print 'none token'
            return
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.URL, url)
            b = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
            c.setopt(pycurl.HTTPHEADER, ['Authorization: JWT %s' % self.API_TOKEN.encode()])
            c.setopt(pycurl.CUSTOMREQUEST, "GET")
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.perform()
            result = b.getvalue()
            print 'result'
        except Exception as e:
            print e
            print 'go error'
            pass
        return result

    #存储模块
    def _write_file(self):
        strs = ''
        for i in self.ip_list:
            ip = '{}\n'.format(i)
            strs = strs + ip
        r = str(datetime.datetime.now()).replace(' ', '-') 
        #r = random.randrange(1, 100000)
        path = os.getcwd()
        file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
        #file_name = '{}\\{}_{}.txt'.format(path, self.facets, r)
        print file_name
        while True:
            if os.path.exists("{}".format(file_name)):
                r = random.randrange(1, 100000)
                file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
                #file_name = '{}\\{}_{}.txt'.format(path, self.facets, r)
            else:
                break

        print 'write result 2 file {}'.format(file_name)
        self.fname = file_name
        try:
            file = open(file_name, 'w')
            file.write(strs)
            file.close()
        except IOError:
            print IOError

    #解析json数据模块
    def _parse_json(self, jsondata):
        port = self.port
        facets = self.facets
        data = json.loads(jsondata)
        try:
            if 'matches' in data:
                for host in data['matches']:
                    result = {}
                    if host.has_key('site'):
                        result['site'] = host['site']
                    else:
                        if host.has_key('ip'):
                            if port:
                                result['ip'] = "{}:{}".format(host['ip'], host['portinfo']['port'])
                            else:
                                result['ip'] = host['ip']
                            self.ip_list.append(result['ip'])
                        else:
                            print '[WARN] {} >> just go wrong'.format(datetime.datetime.now())
                    if facets:
                        for facet in data['facets']:
                            if host.has_key(facet):
                                result[facet] = host[facet]
                            else:
                                for key in host.keys():
                                    if isinstance(host[key], dict):
                                        if host[key].has_key(facet):
                                            result[facet] = host[key][facet]
                                            break
                                else:
                                    result[facet] = ""

            else:
                print '[WARN] {} >> url is error << in {}'.format(datetime.datetime.now())
        except Exception:
            print Exception

    def save_token(self):
        token = self.API_TOKEN
        now_time = datetime.datetime.now()
        try:
            path = os.getcwd()
            #file_name = '{}\\token.txt'.format(path)
            file_name = os.path.join(path, 'token.txt')
            write_s = write_s = '{}\n{}'.format(now_time, token) # time before token
            file = open(file_name, 'w')
            #write_s = '{}\n{}'.format(token, now_time)
            file.write(write_s)
            file.close()
            print '[INFO] {} : save token success'.format(datetime.datetime.now())
        except IOError:
            print '[ERROR] {} >>> save token fail'.format(datetime.datetime.now())
            print IOError
    
    @staticmethod
    def load_token():
        now_time = datetime.datetime.now()
        token = ''
        try:
            path = os.getcwd()
            file_name = os.path.join(path, 'token.txt')
            if os.path.exists(file_name):
                file = open(file_name, 'r')
                last_time_t = '{}'.format(file.readline()).strip() # Clear the space or \n
                token = file.readline()
                try:
                    last_time = datetime.datetime.strptime(last_time_t, '%Y-%m-%d %H:%M:%S.%f')
                except Exception:
                    last_time = datetime.datetime.strptime(last_time_t, '%Y-%m-%d %H:%M:%S')
                #now_time = datetime.datetime.now()
                #d = (now_time- last_time).days
                #if d.days <1 and token:
                if token :
                    if ((now_time - last_time) < _limit_time) : #_limit_time is in the top of this file
                        return token
            else:
                print 'token file not exits'
        except IOError:
            print IOError
        except Exception:
            print Exception

        return None