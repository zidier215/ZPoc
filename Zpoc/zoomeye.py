#!/usr/bin/python
#coding=utf8
__author__ = 'MR.SJ'
# !/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import json
import certifi
import pycurl
import StringIO
import random
import Queue
import os
import datetime
import thread
<<<<<<< HEAD:Zpoc/zoomeye.py
import sys
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
=======
import logging

_limit_time = datetime.timedelta(0,0,0,0,0,12,0)

# 这是一个初始化的类，以来于ZoomEye() 类的单例效果，不会重复初始化
# 使用的时候还是依靠 logging的五个接口
# logging.debug(message), logging.info(message), logging.warning(message)
# logging.error(message), logging.critical(message)
# 日志的存放位置可以自行指定，或者默认不指定就会在当前目录下创建一个 log 目录，并在其中存放日志文件
#    日志文件的默认命名是 zpoc_log_年-月-日.log
# 在初始化 ZoomEye()的时候，在第三个参数位置传入想要的日志等级
#    0~4 分别对应 debug ~ critical
class _log_module():
       def __init__(self, log_level=1, file_dst=None):
           self.LEVEL = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
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
               logging.warning('log_moudle load Fail!Check For the Directory or the Authority')
       
       def clear(self):
           with open(self.zpoc_log, 'w') as target:
               pass

>>>>>>> master:zoomeye/zoomeye.py
    
       
class ZoomEye():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ZoomEye, cls).__new__(cls, *args, **kwargs)
        return cls._inst

<<<<<<< HEAD:Zpoc/zoomeye.py

    def __init__(self, username, password):
=======
    # 构造方法，完成成员变量初始化
    def __init__(self, username, password, log_levels=1):
>>>>>>> master:zoomeye/zoomeye.py
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
<<<<<<< HEAD:Zpoc/zoomeye.py
        # logging The Message
        logs = _log_module()

=======
        # logging The Message, Depend by the Singleton of the ZoomEye() !!!
        self.logs = _log_module(log_levels)
>>>>>>> master:zoomeye/zoomeye.py

    def login(self):
        token=self.load_token()
        if token:
            self.API_TOKEN=token
        else:
            self._login()
        return
<<<<<<< HEAD:Zpoc/zoomeye.py

=======
>>>>>>> master:zoomeye/zoomeye.py

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
                logging.info('success login') # For INFO level
                #print 'success login'
                self.API_TOKEN = json.loads(b.getvalue())["access_token"]
                self.save_token()
            else:
                logging.warning('success fail,get null result') #2 For WARNING level
                #print 'success fail,get null result'
            logging.debug(self.API_TOKEN)
            #print self.API_TOKEN
            b.close()
            c.close()
        except pycurl.E_HTTP_POST_ERROR:
            logging.error(str(pycurl.E_HTTP_POST_ERROR))
            #print pycurl.E_HTTP_POST_ERROR
        except Exception as e:
            logging.error('please check your password or username')
            logging.error(e.message) #3 For ERROR level
            #print 'please check your password or username'
            #print e.message
            pass


    def _search(self, port, page, facets, poc_name):
        self.port = port
        self.facets = facets
        if page > 0:
            for i in range(1, int(page) + 1):
<<<<<<< HEAD:Zpoc/zoomeye.py
                #url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port, i, facets)
                url = self._get_search_url(port, page, facets)
                url = '{}{}'.format(url,'&page=%s'%i)
                print '_get_url'
=======
                url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port, i, facets)
                logging.debug('_get_url') # 0 for DEBUG level
                #print '_get_url'
>>>>>>> master:zoomeye/zoomeye.py
                data = self._get_url(url)
                self._parse_json(data)
            self._write_file()
        else:
            logging.warning('page not be <0') # 2 For WARNING level
            #print 'page not be <0'
            pass
        #thread.exit_thread()
        if self.fname and poc_name:
<<<<<<< HEAD:Zpoc/zoomeye.py
            os.system('python ../pocsuite.py -r {} -f {}'.format(poc_name, self.fname))
=======
            try:
                os.system('python pocsuite.py -r {} -f {}'.format(poc_name, self.fname))
            except Exception as e:
                logging.error(e.message) # 3 For ERROR level
            
>>>>>>> master:zoomeye/zoomeye.py
        else:
            logging.error('args error') # 3 For ERROR level
            #print 'args error'


    def run_fast(self, port, page, facets):
        for i in range(page):
            thread.start_new_thread(self._search(port, page, facets), (i, i))


    def _get_search_url(self, port, page, facets):
        url = 'https://api.zoomeye.org/host/search?query='
        flag = False
        if port and facets:
            print 'port or facets cant null'
            sys.exit()
        if port != 0:
            url = '{}{}'.format(url, '"port:%s"' % port)
            flag = True
        # if page > 0:
        #     if flag:
        #         url = '{}{}'.format(url, '&page={}')
        #     else:
        #         url = '{}{}'.format(url, 'page={}')
        #     flag = True
        # else:
        #     flag = False
        if facets:
            if flag:
                url = '{}{}'.format(url, '&facets=%s' % facets)
            else:
                url = '{}{}'.format(url, 'facets=%s' % facets)
        print url
        return url


    def _get_url(self, url):
        if self.API_TOKEN == None:
            logging.error('none token') # 3 For ERROR level
            #print 'none token'
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
            logging.debug('result')
            #print 'result'
        except Exception as e:
            logging.error(e.message)
            logging.error('go error')
            #print e
            #print 'go error'
            pass
        return result


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
<<<<<<< HEAD:Zpoc/zoomeye.py
        print file_name
=======
        logging.debug(file_name)
        #print file_name
>>>>>>> master:zoomeye/zoomeye.py
        while True:
            if os.path.exists("{}".format(file_name)):
                r = random.randrange(1, 100000)
                file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
                #file_name = '{}\\{}_{}.txt'.format(path, self.facets, r)
            else:
                break
        logging.debug('write result 2 file {}'.format(file_name))        
        #print 'write result 2 file {}'.format(file_name)
        self.fname = file_name
        try:
            file = open(file_name, 'w')
            file.write(strs)
            file.close()
        except IOError as e:
            logging.error(e.message)
            #print IOError


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
<<<<<<< HEAD:Zpoc/zoomeye.py
                            print '[WARN] {} >> just go wrong'.format(datetime.datetime.now())
=======
                            logging.warning('just go wrong') # 2 For WARNING level
                            #print 'just go wrong'
>>>>>>> master:zoomeye/zoomeye.py
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
<<<<<<< HEAD:Zpoc/zoomeye.py
                print '[WARN] {} >> url is error << in {}'.format(datetime.datetime.now())
        except Exception:
            print Exception
=======
                logging.warning('url is error')
                #print 'url is error'
        except Exception as e:
            logging.error(e.message)
>>>>>>> master:zoomeye/zoomeye.py

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
<<<<<<< HEAD:Zpoc/zoomeye.py
            print '[INFO] {} : save token success'.format(datetime.datetime.now())
        except IOError:
            print '[ERROR] {} >>> save token fail'.format(datetime.datetime.now())
            print IOError
=======
            logging.debug('save token success')
            #print 'save token success'
        except IOError as e:
            logging.error('save token fail')
            logging.error(e.message)
            #print 'save token fail'
            #print IOError
>>>>>>> master:zoomeye/zoomeye.py
    
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
<<<<<<< HEAD:Zpoc/zoomeye.py
=======
                    logging.debug('The datetime want %Y-%m-%d %H:%M:%S')
>>>>>>> master:zoomeye/zoomeye.py
                    last_time = datetime.datetime.strptime(last_time_t, '%Y-%m-%d %H:%M:%S')
                #now_time = datetime.datetime.now()
                #d = (now_time- last_time).days
                #if d.days <1 and token:
                if token :
                    if ((now_time - last_time) < _limit_time) : #_limit_time is in the top of this file
                        return token
            else:
                logging.warning('token file not exits') # 2 For WARNING level 
                #print 'token file not exits'
        except IOError as e:
            logging.error(e.message)
            #print IOError
        except Exception as e:
            logging.error(e.message)
            #print Exception

        return None