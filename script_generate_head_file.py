#!/usr/bin/env python
# coding=utf-8


import sys
import os
'''
采用有限状态机对文件内容进行词法分析
状态机相对c编译器是极为简化·

'''
global filecontent,filename

def analysecontent():
    global filecontent
    c_size = len(filecontent)
    print c_size
def writetoheadfile():
    global filename_pre

def getfilecontent():
    global filename,filecontent
    fp = open(filename,'r')
    filecontent = fp.read()
    fp.close()

def print_help():
    print 'please use this script as:python force_compile_byerrors.py  cfile'


#main
def main():
    global filename_pre,filename

    filename = ''#待编译的c文件名
    if len(sys.argv) != 2:
        print_help()
    else:
        filename = sys.argv[1] #命令中输入的c文件名
    # 得到c文件名的除 .c 的部分，并且创建 .h 头文件
    seq = filename.find('.c')
    if(seq == -1):
        print 'cfilename error'
        return

    filename_pre = filename[:seq]
    filename_pre += '.h'
    #创建头文件.h
    createfile_cmd = 'touch %s'% filename_pre
    os.system(createfile_cmd)

    # 在c文件中添加头文件
    file_c = open(filename,'r')
    #首先判断原文件中是否已经包含.h文件
    first_line = file_c.readline()
    insert_content = '#include "%s"' % filename_pre
    if(first_line not in insert_content):
        file_c_content = file_c.read() #得到文件中所有内容
        file_c.close()
        a = file_c_content.split('\n')
        a.insert(0,insert_content)
        s = '\n'.join(a)
        file_c = file(filename,'w')
        file_c.write(s)#将新生成的内容插入到c文件中
    file_c.close()
    getfilecontent()#再次得到c文件中所有内容
    analysecontent()#分析文件内容
    writetoheadfile()#将得到的分析结果写入到头文件

if __name__ == "__main__":

    main()



