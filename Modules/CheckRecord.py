########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-06-03 17:09:02
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 17:09:49
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
# 用于判断是否清空以前的记录
def check_record(clear:str) -> bool:
    if clear=='yes':
        return True
    else:
        return False