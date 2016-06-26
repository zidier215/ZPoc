#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
__author__ = 'MR.SJ'

#####################################################
# example:
#python lock.py -d app,os -p 1 -o 21 -r xxe.py
#-d dork
#-p page
#-o port
#-r poc
####################################################
import getopt
import sys
import zoomeye


if __name__ == "__main__":
    z = zoomeye.ZoomEye("1064901069@qq.com", "wsx88619973@", 0)
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
    print port, page, dork, poc_name
    z._search(port, page, dork, poc_name)

