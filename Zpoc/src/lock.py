#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
__author__ = 'MR.SJ'

#####################################################
# example:
#python lock.py --help
####################################################
import getopt
import sys
import zoomeye
import os
import platform

def handle_script(file_name=''):
    script_path = os.path.join(os.path.dirname(os.getcwd()), 'etc')
    ##print script_path
    if file_name == '':
        file_name = 'script.zpoc'
    file_name = os.path.join(script_path, file_name)
    result = {}
    try:
        file = open(file_name, 'r')
        line_number = 0
        for line in file:
            # For Each Line
            line = line.rstrip('\n')
            ##print 'Read {} : '.format(line_number) + line
            line_number = line_number + 1
            # If line is empty, Skip it
            if line == '':
                continue
            # if Line is start with '#', It should Not Be parse
            index = line.find('#')
            if index == 0:
                continue
            if index == -1:
                index = len(line)
            real_line = line[0:index].strip()
            # Search For Configuration
            # Each Paramter is put in key : value
            seperate = real_line.find(':')       
            if seperate == -1:
                raise Exception('Error script Syntax')
            key = real_line[0:seperate].strip()
            value = real_line[seperate+1:].strip()
            if key == 'port':
                result['port'] = value
            elif key == 'query':
                result['query'] = value
            elif key == 'facets':
                result['facets'] = value
            elif key == 'poc':
                result['poc'] = value
            elif key == 'page':
                result['page'] = int(value)
            elif key == 'search-type':
                if value.lower() == 'web':
                    value = zoomeye.WEB_SEARCH
                elif value.lower() == 'host':
                    value = zoomeye.HOST_SEARCH
                else:
                    raise Exception('Wrong Search type in line {}'.format(line_number))
                result['search-type'] = value
            # Not the Correct Key
            else:
                raise Exception('Some thing Bad Key Occur in the Script File line {}'.format(line_number))
        file.close()
    except Exception as e:
        print 'Read "{}" File Fail'.format(file_name)
        print e.message
        sys.exit(1)
    return result

def _help():
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
        1. python lock.py -q port:80,nginx -d app,os -s host -p 1 -r xxe.py
        2. python lock.py --query=port:80,nginx -d webapp,os -s web -p 1 -r xxe.py
      * 3. python lock.py -f xxx.zpoc
Others:
        1. If you want a Iterative Handle, Just open Python Iterative Environment, And Import zoomeye,
        Call zoomeye.zoomeye_help() For More Usage
        2. If you want a Command Line Operation, See Examples
        3. ZoomEye Manual Site:https://www.zoomeye.org/help/manual
            '''
    sys.exit(0)

if __name__ == "__main__":
    dork = ''
    port = -1
    page = 1
    poc_name = ''
    search_type = zoomeye.HOST_SEARCH
    query = []
    opts, args = getopt.getopt(sys.argv[1:], "hd:o:p:r:q:s:f", ["help", 'facets=', 'port=', 'page=', 'poc=', 'query=', 'search-type=', 'script-file='])
    for op, value in opts:
        if op in ('-q', '--query'):
            query = value.split(',')
        elif op in ('-s', '--search-type'):
            if value == 'web':
                search_type = zoomeye.WEB_SEARCH
            elif value == 'host':
                search_type = zoomeye.HOST_SEARCH
            else:
                print 'Bad Search Type Sepcific, Check it For Real!'
                sys.exit(1)
        elif op in ('-d', '--facets'):
            dork = value
        elif op in ('-p', '--page'):
            page = value
        elif op in ('-o', '--port'):
            port = value
        elif op in ('-r', '--poc'):
            poc_name = value
        elif op in ('-f', '--script-file'):
            dict_result = handle_script()
            query = dict_result['query'].split(',')
            port  = dict_result['port']
            dork  = dict_result['facets']
            poc_name = dict_result['poc']
            page  = dict_result['page']
            search_type = dict_result['search-type']
        elif op in ('-h', '--help'):
            _help()
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
    ##print query, dork, page, search_type, poc_name, port
    #检查token，输入是否使用token，提示用户名，用户交互输入用户名密码
    # User Interative
    name = raw_input('Enter Your ZoomEye Username: ')
    psw  = raw_input('Enter Your ZoomEye Password: ')
    #sys.exit(1)
    z = zoomeye.ZoomEye(name, psw, 0)
    name = ''
    psw = ''
    # login
    z.login()
    # Search
    z.search(port, page, dork, poc_name, query, search_type)

    sysattr = platform.system()
    if sysattr == 'Windows':
        os.system('pause')
        os.system('cls')
    else:
        raw_input('Press Any Key to Continue')
        os.system('clear')   
    while True:
        print ''' Choose One Of the Five Selections[1-5]
        1. Search The Same Paramters Again
        2. Search The Same Paramters Except "query" and "PoC-file"
        3. Search With other Paramters
        4. search With zpoc script file
        5. Exit 
        '''
        choose = raw_input('> ')
        if choose == '1':
            z.search(port, page, dork, poc_name, query, search_type)
        elif choose == '2':  
            query = []
            query.append(raw_input('query = '))
            poc_name = raw_input('PoC File Name = ')
            run = raw_input('Are The Paramters Rright?[y/n]').lower()
            while run != 'y' and run != 'n':
                run = raw_input('Are The Paramters Rright?[y/n]').lower()
            z.search(port, page, dork, poc_name, query, search_type)    
        elif choose == '3':
            run = 'y'
            while run == 'y':
                page = int(raw_input('page = '))
                query = []
                query.append(raw_input('query = '))
                facets = raw_input('facets = ')
                poc_name = raw_input('PoC File Name = ')
                search_type = int(raw_input('search_type(0 For HOST_SEARCH,1 For WEB_SEARCH) = '))
                run = raw_input('Are The Paramters Rright?[y/n]').lower()
                while run != 'y' and run != 'n':
                    run = raw_input('Are The Paramters Rright?[y/n]').lower()
                z.search(port, page, dork, poc_name, query, search_type) 
        elif choose == '4':
            result = handle_script()   
            query = result['query'].split(',')
            port  = result['port']
            dork  = result['facets']
            poc_name = result['poc']
            page  = result['page']
            search_type = result['search-type']
            z.search(port, page, dork, poc_name, query, search_type)
        elif choose == '5':
            print 'Thanks For Using!' 
            sys.exit(1)
        else:
            print 'Bad Choosing'
        if sysattr == 'Windows':
            os.system('pause')
            os.system('cls')
        else:
            raw_input('Press Any Key to Continue')
            os.system('clear')
    #print 'test'
    #print page, dork, poc_name, query       
    #z._search(port, page, dork, poc_name)

