#!/usr/bin/env python
# coding=utf-8


import sys
import os
'''
采用有限状态机对文件内容进行词法分析
状态机相对c编译器是极为简化·

'''
filecontent = ''
filename = ''
global var_name ,struct_name

#标识符种类
NORMAL_ID = 1#普通的类型标识符
NORMAL_VAR = 2#普通的变量
STRUCT_TYPE = 3#结构体名
STRUCT_MEM = 4 #结构体成员变量


var_name = []#保存所有未定义数据类型的名称
struct_name = {}#保存所有

## 满足标识符的字符数组
characters1 = [chr(i) for i in range(ord('a'),ord('z'))]
characters2 = [chr(i) for i in range(ord('A'),ord('Z'))]
characters3 = [chr(i) for i in range(ord('0'),ord('9'))]
characters = characters1+characters2+characters3
characters.append('_')
characters_first = characters1+characters2
characters_first.append('_')

#二维数组 保存经过分词之后的文件内容 ， 每行为一个维度
filecontent_splited = []

def analysecontent():#分析c文件内容
    global filecontent,characters,characters_first 
    c_size = len(filecontent)
    #逐个字符分析
    current_pos = 0
    newline = []#暂存一行中的标识符
    IS_NOTE = 0 #是否在注释内部

    while (current_pos < c_size):
        #判断是否是注释内容
        if(filecontent[current_pos] == '/'):
            if(filecontent[current_pos+1] == '/' and not IS_NOTE  ):
                IS_NOTE = 1
            elif (filecontent[current_pos-1] == '*' and IS_NOTE ):
                IS_NOTE = 0
            elif (filecontent[current_pos+1] == '*' and not IS_NOTE):
                IS_NOTE = 10000
        #判断是否开始行的一行
        elif(filecontent[current_pos] == '\n'):
            if(IS_NOTE):
                IS_NOTE -=1
            if(len(newline)):
                filecontent_splited.append(newline)
                newline = []
        #判断是否是标识符的开始
        elif(filecontent[current_pos] in characters_first and not IS_NOTE):
            #得到标识符
            start = current_pos
            current_pos+=1
            while(filecontent[current_pos] in characters or filecontent[current_pos] == '.'):
                current_pos+=1
            Identifier = filecontent[start:current_pos]
            newline.append(Identifier)
            #继续找下一个标识符
        current_pos+=1
    for item in filecontent_splited:
        print item





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



