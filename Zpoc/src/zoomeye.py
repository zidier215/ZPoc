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
HOST_SEARCH = 0
WEB_SEARCH  = 1
_host_api = 'https://api.zoomeye.org/host/search?'
_web_api  = 'https://api.zoomeye.org/web/search?'
ENGLISH = 0
CHINESE = 1
def zoomeye_help(type = ENGLISH):
    if type == ENGLISH:
        print '''
    IF YOU WANT CHINESE HELP: zoomeye.zoomeye_help(zoomeye.CHINESE)

       zoomeye_username = 'zpoc@domain.com'
       zoomeye_password = 'zpoc'
       log_level = 1 
    1. zpoc = zoomeye.ZoomEye(zoomeye_username, zoomeye_password, log_level)
        PS: log_level is from 0 up to 4 For debug, info, warning, error, critical
            you also could IGNORE it, Because of its Default Value is 1
    2. zpoc.login()
        PS: Call login to Fetch the token, And you Could GET/POST message Success
            To put it Simplely, It makes our Program to Work now
       page = 1
       query = ['port:80']
       facets = 'app,os'
       poc_name = 'xxx.py'
       port = ''
       search_type = zoomeye.HOST_SEARCH
    3. zpoc.search(port, page, facets, poc_name, query, search_type)
        PS: From Up to Down is : page We need, query argument is a list, facets argument,
        port is just a historical paramter, set it to empty
        poc_name is For PoC file name, put it to le pocs directory
        search_type is For Web Search OR Host Search : zoomeye.WEB_SEARCH, zoomeye.HOST_SEARCH
    4. zpoc.search(....) # Second time Search AS the same syntax
        new_username = 'newzpoc@domain.com'
        new_password = 'newzpoc'
    5. zpoc.relogin(new_username, new_password)
        PS: If you wanna to Change the ZoomEye Account, call relogin with Not Empty Paramters
            If you wanna to logout, Just Make the two paramters stay Empty ''
        '''
    else:
        print '''
   zoomeye_username = 'zpoc@domain.com'
   zoomeye_password = 'zpoc'
   log_level = 1
1. zpoc = zoomeye.ZoomEye(zoomeye_username, zoomeye_password, log_level)
    注释: log_level 的取值范围是0到4，分别对应 debug, info, warning, error, critical
          你也可以忽略他们，因为这是一个带默认值的参数，默认是info级别
2. zpoc.login()
    注释: 调用login是为了取得token属性，这样就能正常获取数据了
          简单来说，就是调用了login之后就能正常开始工作了
   page = 1
   query = ['port:80']
   facets = 'app,os'
   poc_name = 'xxx.py'
   port = ''
   search_type = zoomeye.HOST_SEARCH
3. zpoc.search(port, page, facets, poc_name, query, search_type)
    注释: 从上至下的参数依次是 : page 我们需要的页数, query 是一个链表, facets 参数,
          port 是一个历史遗留的参数, 可以简单的将其置为空
          poc_name 是你的PoC文件名, 把它放在pocs文件夹内
          search_type 有两个取值 HOST_SEARCH 和 WEB_SEARCH
4. zpoc.search(....) # 后续多次搜索只需要调用这个函数就行
    new_username = 'newzpoc@domain.com'
    new_password = 'newzpoc'
5. zpoc.relogin(new_username, new_password)
    注释: 如果你想更换账号，那就调用这个函数，并传入新的账号密码
          如果你想退出本次账号，那将两个参数置为空 '' 就行
    '''
        
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
           local_cwd = os.path.dirname(os.getcwd())
           if self.zpoc_log is None:
               tmp = os.path.join(local_cwd, 'logs')
               if not os.path.exists(tmp) :
                   os.mkdir(tmp)
               name_day = str(datetime.datetime.now())[:10]
               self.zpoc_log = os.path.join(local_cwd, os.path.join('logs', 'zpoc_log_{}.log'.format(name_day)))
               if not os.path.exists(self.zpoc_log) :
                   with open(self.zpoc_log, 'w') as f:
                       pass
           try:
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
        self.search_type = HOST_SEARCH
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
    
    def _logout(self):
        self.token = None
        self.user_name = '' 
        self.password  = ''
        self.data = {"username": '', "password": ''}
        token_file = os.path.join(os.getcwd(), 'token.txt')
        try:
            if os.path.exists(token_file):
                os.remove(token_file)
        except Exception as e:
            logging.warning('loggout Exception For ' + e.message)
    
    def relogin(self, username, password):
        self._logout()
        if username == '' or password == '':
            return
        self.user_name = username
        self.password = password
        self.data = {
            "username": self.user_name,
            "password": self.password
        }
        self.login()

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
            message = b.getvalue()
            if message:
                logging.debug('Get Message From ZoomEye.org Success!')
                self.API_TOKEN = json.loads(message)["access_token"]
                # if self.API_TOKEN is nothing ,WILL Raise Exception by json.loads()
                self.save_token()
            else:
                logging.error('login fail,get nothing From ZoomEye.org') #2 For WARNING level
                raise Exception('Get Nothing')
            logging.debug(self.API_TOKEN)
            b.close()
            c.close()
        except pycurl.E_HTTP_POST_ERROR:
            logging.error(str(pycurl.E_HTTP_POST_ERROR))
            # exit , will Be Replaced by Re-Entry
            sys.exit()
        except Exception as e:
            logging.error(e.message + ' AND CHECK Your ZoomEye/Seebug Username and Password') #3 For ERROR level
            # exit , will Be Replaced by Re-Entry
            sys.exit()
    
    # Search Code
    def _search(self, query, page, facets, poc_name, type=HOST_SEARCH):
        self.facets = facets
        if page > 0:
            for i in range(1, int(page) + 1):
                url = self._get_search_url(query, page, facets, type)
                url = '{}{}'.format(url,'&page=%s'%i)
                logging.debug('_get_url')
                #print '_get_url'
                data = self._get_url(url)
                try:
                    if type == HOST_SEARCH:
                        logging.debug('HOST_SEARCH Start')
                        self._parse_json(data)
                        logging.debug('HOST_SEARCH End')
                    elif type == WEB_SEARCH:
                        logging.debug('WEB_SEARCH Start')
                        self._parse_json_get_ip(data)
                        logging.debug('WEB_SEARCH End')
                    else:
                        raise Exception('Bad Search Type')
                except Exception as e:
                    logging.warning(e.message)
                    return
            self._write_file()
        else:
            logging.warning('page not be <0') # 2 For WARNING level
            pass
        self.comand_poc(poc_name)
    
    # Host Search
    def _host_search(self, query, page, facets, poc_name):
        self._search(query, page, facets, poc_name, HOST_SEARCH)
    # Web Search
    def _web_search(self, query, page, facets, poc_name):
        self._search(query, page, facets, poc_name, WEB_SEARCH)
    # Interface of Search        
    def search(self, port, page, facets, poc_name, query, search_type):
        # If Port(-o, --port) is not specific, then take it From query 
        if port == -1:
            for i,val in enumerate(query):
                tmp = val.find('port:')
                if tmp != -1:
                    port = val[5:]
                    break
        if port == -1:
            port = ''    
        self.port = port
        query_arg = ''
        for i, val in enumerate(query):
            query_arg += val+' '
        # if Query Argument is Not Empty    
        if query_arg != '':
            query_arg = '"{}"'.format(query_arg.rstrip(' '))
        if search_type == HOST_SEARCH:
            logging.debug('Host Search For query:{}, facets:{}, page:{}, poc-file:{}'.format(query_arg,facets,page,poc_name))
            self._host_search(query_arg, page, facets, poc_name)
        else:
            logging.debug('Web Search For query:{}, facets:{}, page:{}, poc-file:{}'.format(query_arg,facets,page,poc_name))
            self._web_search(query_arg, page, facets, poc_name)
    
    def comand_poc(self,poc_name):
        if self.fname and poc_name:
            try:
                logging.debug(os.getcwd())
                exit_code = os.system('pocsuite -r {} -f {}'.format(poc_name, self.fname))
                if exit_code is not 0:
                    exit_code = os.system('python ../pocsuites.py -r {} -f {}'.format(poc_name, self.fname))
                elif exit_code is not 0:
                    exit_code = os.system('python pocsuites.py -r {} -f {}'.format(poc_name, self.fname))
                else:
                    raise Exception('No Such Command, Check Your pocsuite')
            except Exception as e:
                logging.error('os.system : '+e.message) # 3 For ERROR level
        else:
            logging.error('args error') # 3 For ERROR level
            sys.exit(1)

    def run_fast(self, port, page, facets):
        for i in range(page):
            thread.start_new_thread(self._search(port, page, facets), (i, i))


    def _get_search_url(self, query, page, facets, type):
        url = _host_api
        if type is not WEB_SEARCH and type is not HOST_SEARCH:
            logging.error('search type is ERROR! Check For real')
        if type is WEB_SEARCH:
            url = _web_api    
        flag = False
        logging.debug('query:{}, facets:{}'.format(query, facets))
        if query == '' and facets == '':
            logging.warning('port or facets cant null')
            sys.exit()
        if query != '':
            url = '{}{}'.format(url, 'query={}'.format(query))
            flag = True
            #url = '{}{}'.format(url, '"port:%s"' % port)
        if facets != '':
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
        logging.debug('FULL REQUEST '+url)
        result = ''
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
            logging.debug(result)
            if not result:
                raise Exception('getvalue() error')
            logging.debug('result')
        except Exception as e:
            logging.error(e.message)
            logging.error('_get_url has meet Some Error, Check your Network')
        return result


    def _write_file(self):
        strs = ''
        # Put All txt into the 'zoomeyedata' Directory
        path = os.path.join(os.path.dirname(self.cwd), 'zoomeyedata') 
        try:      
            if not os.path.exists(path):
                os.mkdir(path)
        except Exception as e:
            logging.debug(e.message)
        for i in self.ip_list:
            ip = '{}\n'.format(i)
            strs = strs + ip
        r = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        #file_name = os.path.join(path, str(self.facets)+'_'+str(r)+'.txt')
        file_name = os.path.join(path,self.facets.replace('/',',')+str(r)+'.txt')
        logging.debug(file_name)
        logging.debug('write result to file {}'.format(file_name))
        file_name=r'{}'.format(file_name)
        self.fname = file_name
        files = open(file_name, 'w')
        try:
            logging.debug('write file')
            print 'write file'
            files.write(strs)
            files.close()
            logging.debug('write success')
        except IOError as e:
            logging.error(e.message)


    def _parse_json_get_ip(self, rawdata):
        # Search For ip message Means that "ip": [xxx.xxx.xxx.xxx]
        found = rawdata.find('"ip":')
        while found != -1:
            start = rawdata.find('[', found) + 2
            end = rawdata.find('"]', start)
            logging.debug('ip: {}'.format(rawdata[start:end]))
            self.ip_list.append(rawdata[start:end])
            found = rawdata.find('"ip":', end)
    
    def _parse_json(self, jsondata):
        port = self.port
        facets = self.facets
        data = None
        try:
            data = json.loads(jsondata)
        except:
            raise Exception('Data Receive Could Not Be parse by json')
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
        files = ''
        try:
            path = self.cwd#os.getcwd()
            file_name = os.path.join(path, 'token.txt')
            write_s = write_s = '{}\n{}'.format(now_time, token) # time before token
            files = open(file_name, 'w')
            files.write(write_s)
            logging.debug('save token success')
        except IOError as e:
            logging.error('save token fail')
            logging.error(e.message)
        finally:
            files.close()
    
    #@staticmethod
    def load_token(self):
        now_time = datetime.datetime.now()
        token = ''
        try:
            path = self.cwd#os.getcwd()
            file_name = os.path.join(path, 'token.txt')
            files = ''
            if os.path.exists(file_name):
                try:
                    files = open(file_name, 'r')
                    last_time_t = '{}'.format(files.readline()).strip() # Clear the space or \n
                    token = files.readline()
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
                    files.close()
            else:
                logging.warning('token file not exits') # 2 For WARNING level 
        except Exception as e:
            logging.error(e.message)
        return None