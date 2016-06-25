__author__ = 'MR.SJ'
#####################################################
# example:
#python lock.py -d app,os -p 1 -o 21 -r xxe.py
#-d 指定dork组件
#-p 指定页数
#-o 指定端口
#-r 指定poc
####################################################
import zoomeye
import getopt
import sys
import os

if __name__ == "__main__":
    z = zoomeye.ZoomEye("r00teer@163.com", "gh0s1ter@zpt")
    z.login()
    dork = ''
    port = 0
    page = 1
    poc_name = ''
    opts, args = getopt.getopt(sys.argv[1:], "hd:o:p:r:")
    for op, value in opts:
        if op == '-d':
            dork = value
        elif op == '-p':
            page = value
        elif op == '-o':
            port = value
        elif op == '-r':
            poc_name = value
        elif op == '-h':
            print ''' help info: \n
            -d  dork
            -p  page
            -o  port
            -r  poc_file
            '''
            sys.exit()
    z._search(port, page, dork, poc_name)

