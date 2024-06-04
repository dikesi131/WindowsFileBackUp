########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-01-09 16:55:34
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 17:04:33
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
import argparse
# 获取参数
def GetParameters() -> object:
    parser=argparse.ArgumentParser(description="用于进行文件的备份")
    parser.add_argument("-o",'--output',type=str,help="请输入要备份到的目录",default='G:/backup')
    parser.add_argument("-m",'--mode',type=str,help="请输入要使用的模式[db/file],default=file",choices=['db','file'],default='file')
    parser.add_argument('-c','--clear',type=str,help="是否清除已备份文件的记录[yes/no],default=no",choices=['yes','no'],default='no')
    return parser