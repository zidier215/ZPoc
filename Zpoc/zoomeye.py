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
import sys


class ZoomEye():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ZoomEye, cls).__new__(cls, *args, **kwargs)
        return cls._inst


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


    def login(self):
        # token=self.load_token()
        # if token:
        #     self.API_TOKEN=token
        # else:
        #     self._login()
        self._login()


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
                #self.save_token()
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


    def _search(self, port, page, facets, poc_name):
        self.port = port
        self.facets = facets
        if page > 0:
            for i in range(1, int(page) + 1):
                #url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port, i, facets)
                url = self._get_search_url(port, page, facets)
                url = '{}{}'.format(url,'&page=%s'%i)
                print '_get_url'
                data = self._get_url(url)
                self._parse_json(data)
            self._write_file()
        else:
            print 'page not be <0'
            pass
        #thread.exit_thread()
        if self.fname and poc_name:
            os.system('python ../pocsuite.py -r {} -f {}'.format(poc_name, self.fname))
        else:
            print 'args error'


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


    def _write_file(self):
        strs = ''
        for i in self.ip_list:
            ip = '{}\n'.format(i)
            strs = strs + ip
        r = random.randrange(1, 100000)
        path = os.getcwd()
        file_name = '{}\\{}_{}.txt'.format(path, self.facets, r)
        print file_name
        while True:
            if os.path.exists("{}".format(file_name)):
                r = random.randrange(1, 100000)
                file_name = '{}\\{}_{}.txt'.format(path, self.facets, r)
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
                            print 'just go wrong'
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
                print 'url is error'
        except Exception:
            print Exception

    def save_token(self):
        token = self.API_TOKEN
        now_time = datetime.datetime.now()
        try:
            path = os.getcwd()
            #file_name = '{}\\token.txt'.format(path)
            file_name = os.path.join(path, '\\token.txt')
            write_s = os.path.join(token, '\n' + now_time)
            file = open(file_name, 'w')
            #write_s = '{}\n{}'.format(token, now_time)
            file.write(write_s)
            file.close()
            print 'save token success'
        except IOError:
            print 'save token fail'
            print IOError

    @staticmethod
    def load_token():
        last_time = datetime.datetime.now()
        token = ''
        try:
            path = os.getcwd()
            file_name = os.path.join(path, '\\token.txt')
            print file_name
            if os.path.exists(file_name):
                file = open(file_name, 'r')
                token = file.readline()
                last_time = '{}'.format(file.readline())
                #last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
                #now_time = datetime.datetime.now()
                #d = (now_time- last_time).days
                #if d.days <1 and token:
                if token:
                    return token
            else:
                print 'token file not exits'
        except IOError:
            print IOError
        except Exception:
            print Exception

        return None