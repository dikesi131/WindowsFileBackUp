########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-06-03 17:02:44
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 17:09:27
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
# 用于判断启用数据库or文件模式
def check_mode(mode:str) -> bool:
    if mode =='db':
        # 启用数据库模式
        return True
    else:
        return False