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
import os

if __name__ == "__main__":
    z = zoomeye.ZoomEye("", "", 0)
    z.login()
    dork = ''
    port = -1
    page = 1
    poc_name = ''
    search_type = zoomeye.HOST_SERACH
    query = []
    opts, args = getopt.getopt(sys.argv[1:], "hd:o:p:r:q:s:f", ["help", 'dork=', 'port=', 'page=', 'poc=', 'query=', 'search-type=', 'script-file='])
    for op, value in opts:
        if op in ('-q', '--query'):
            query = value.split(',')
        elif op in ('-s', '--search-type'):
            if value == 'web':
                search_type = zoomeye.WEB_SEARCH
            elif value == 'host':
                search_type = zoomeye.HOST_SERACH
            else:
                print 'Bad Search Type Sepcific, Check it For Real!'
                sys.exit(1)
        elif op in ('-d', '--dork'):
            dork = value
        elif op in ('-p', '--page'):
            page = value
        elif op in ('-o', '--port'):
            port = value
        elif op in ('-r', '--poc'):
            poc_name = value
        elif op in ('-f', '--script-file'):
            pass
        elif op in ('-h', '--help'):
            print ''' 
Usage: python lock.py [OPTION1] [ARGUMENT1] ... 
        [-d | --dork] [-p | --page] [-o | --port] [-r | --poc ] [-q | --query] [-s | --search-type]
        [-f | --script-file] [-h | --help] \n
        -q, --query         Query Message Argument
        -d, --facets        Facet Argument, For facets used by ZoomEye Search Result in calculation
        -o, --port          Port in query, Stay For historical
        -r, --poc           Absolute Poc file path
        -s, --search-type   Host Or Web Search
        -p, --page          Page Argument
        -f, --script-file   ZPoc Sript file, For tedious Command Line Argument Saving
        -h, --help          Help Information \n
Examples: 
        1. python lock.py -q nginx,port:80 -d app,os -s host -p 1 -r xxe.py
        2. python lock.py --query=nginx,port:80 -d webapp,os -s web -p 1 -r xxe.py
        3. python lock.py -f xxx.zpoc
            '''
            sys.exit(0)
    # Replace Port Message in Query
    if port != -1:
        if query == []:
            query.append('port:{}'.format(port))
        else:
            for i, val in enumerate(query):
                if val.find('port') != -1:
                    query.pop(i)
                    query.append('port:{}'.format(port))
    #Check Query Message
    if port == -1 and query == []:
        print 'quert or port is Empty'
    # Search PoC file in Current Dir or pocs Dir
    if poc_name == '':
        print 'poc file is Needed, Check it For Real'
        sys.exit(1)
    else:
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, poc_name)):
            cwd = os.path.dirname(cwd)
            tmp = os.path.join(cwd, os.path.join('pocs', poc_name))
            if not os.path.exists(tmp):
                print 'PoC File Not Exist in Current Dir Or "poc" dir!'
                sys.exit(1)
            else:
                poc_name = tmp
    if dork == '':
        print 'facets is Empty'
    
    z.search(port, page, dork, poc_name, query, search_type)
    #print 'test'
    #print page, dork, poc_name, query
        
    #z._search(port, page, dork, poc_name)

