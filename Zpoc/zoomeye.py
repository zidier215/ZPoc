# !/usr/bin/python2.7
# -*- coding: UTF-8 -*-
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
import sys
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
           local_cwd = os.getcwd()
           # If the log file is not specify by User, Use Default path : ./log/zpoc_log_xxx,log
           if self.zpoc_log is None:
               tmp = os.path.join(local_cwd, 'log')
               if not os.path.exists(tmp) :
                   os.mkdir(tmp)
               name_day = str(datetime.datetime.now())[:10]
               self.zpoc_log = os.path.join(local_cwd, os.path.join('log', 'zpoc_log_{}.log'.format(name_day)))
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
        
class ZoomEye():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ZoomEye, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    # 构造方法，完成成员变量初始化
    def __init__(self, username, password, log_levels=1):
        self.API_TOKEN = None
        self.url = 'https://api.zoomeye.org/user/login'
        self.user_name = username
        self.password  = password
        self.data = {
            "username": self.user_name,
            "password": self.password
        }
        self.fname = ''
        self.post_data = json.dumps(self.data)
        self.port   = ''
        self.facets = ''
        self.ip_list = []
        self.ip_queue = Queue.Queue(-1)
        # logging The Message, Depend by the Singleton of the ZoomEye() !!!
        self.logs = _log_module(log_levels)
        # Current Work Directory
        self.cwd  = os.getcwd()

    def login(self):
        token=self.load_token()
        if token:
            self.API_TOKEN=token
        else:
            self._login()
        return

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
                self.API_TOKEN = json.loads(b.getvalue())["access_token"]
                self.save_token()
            else:
                logging.warning('success fail,get null result') #2 For WARNING level
            logging.debug(self.API_TOKEN)
            b.close()
            c.close()
        except pycurl.E_HTTP_POST_ERROR:
            logging.error(str(pycurl.E_HTTP_POST_ERROR))
        except Exception as e:
            logging.error('please check your password or username')
            logging.error(e.message) #3 For ERROR level
            pass


    def _search(self, port, page, facets, poc_name):
        self.port = port
        self.facets = facets
        if page > 0:
            for i in range(1, int(page) + 1):
                #url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port, i, facets)
                url = self._get_search_url(port, page, facets)
                url = '{}{}'.format(url,'&page=%s'%i)
                logging.debug('_get_url')
                print '_get_url'
                data = self._get_url(url)
                self._parse_json(data)
            self._write_file()
        else:
            logging.warning('page not be <0') # 2 For WARNING level
            pass
        #thread.exit_thread()
        if self.fname and poc_name:
            try:
                logging.debug(os.getcwd())
                os.system('python pocsuite.py -r {} -f {}'.format(poc_name, self.fname))
            except Exception as e:
                logging.error(e.message) # 3 For ERROR level            
        else:
            logging.error('args error') # 3 For ERROR level

    def run_fast(self, port, page, facets):
        for i in range(page):
            thread.start_new_thread(self._search(port, page, facets), (i, i))


    def _get_search_url(self, port, page, facets):
        url = 'https://api.zoomeye.org/host/search?query='
        flag = False
        logging.debug('port:{}, facets:{}'.format(port, facets))
        if not port and not facets:
            logging.warning('port or facets cant null')
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
        logging.debug(url)        
        return url


    def _get_url(self, url):
        if self.API_TOKEN == None:
            logging.error('none token') # 3 For ERROR level
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
        except Exception as e:
            logging.error(e.message)
            logging.error('go error')
            pass
        return result


    def _write_file(self):
        strs = ''
        # Put All txt into the 'result' Directory
        path = os.path.join(self.cwd, 'result') 
        try:      
            if not os.path.exists(path):
                os.mkdir(path)
        except Exception as e:
            logging.debug(e.message)
        for i in self.ip_list:
            ip = '{}\n'.format(i)
            strs = strs + ip
        r = str(datetime.datetime.now()).replace(' ', '-') 
        #path = #os.getcwd()
        file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
        logging.debug(file_name)
        while True:
            if os.path.exists("{}".format(file_name)):
                r = random.randrange(1, 100000)
                file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
            else:
                break
        logging.debug('write result 2 file {}'.format(file_name))        
        self.fname = file_name
        try:
            file = open(file_name, 'w')
            file.write(strs)
        except IOError as e:
            logging.error(e.message)
        finally :
            file.close()


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
                            logging.warning('just go wrong') # 2 For WARNING level
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
                logging.warning('url is error')
        except Exception as e:
            logging.error(e.message)

    def save_token(self):
        token = self.API_TOKEN
        now_time = datetime.datetime.now()
        try:
            path = self.cwd#os.getcwd()
            file_name = os.path.join(path, 'token.txt')
            write_s = write_s = '{}\n{}'.format(now_time, token) # time before token
            file = open(file_name, 'w')
            file.write(write_s)
            logging.debug('save token success')
        except IOError as e:
            logging.error('save token fail')
            logging.error(e.message)
        finally:
            file.close()
    
    #@staticmethod
    def load_token(self):
        now_time = datetime.datetime.now()
        token = ''
        try:
            path = self.cwd#os.getcwd()
            file_name = os.path.join(path, 'token.txt')
            if os.path.exists(file_name):
                try:
                    file = open(file_name, 'r')
                    last_time_t = '{}'.format(file.readline()).strip() # Clear the space or \n
                    token = file.readline()
                    try:
                        last_time = datetime.datetime.strptime(last_time_t, '%Y-%m-%d %H:%M:%S.%f')
                    except Exception:
                        logging.debug('The datetime want %Y-%m-%d %H:%M:%S')
                        last_time = datetime.datetime.strptime(last_time_t, '%Y-%m-%d %H:%M:%S')
                    if token :
                        if ((now_time - last_time) < _limit_time) : #_limit_time is in the top of this file
                            return token
                except Exception as e:
                    logging.warning(e.message)
                finally:
                    file.close()
            else:
                logging.warning('token file not exits') # 2 For WARNING level 
        except Exception as e:
            logging.error(e.message)
        return None