########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-12-09 23:01:54
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-05-29 23:11:27
 # $ @FilePath: \YifanScripts\FileBackup\Modules\GlobalVar.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
# 注：_init()只需要在程序一开始调用的模块调用即可
# 使用set和get方法的目的是为了实现多模块共享全局变量，避免全局变量命名空间不同从而逻辑出错的问题
def _init():
    """在主模块初始化"""
    global GLOBALS_DICT
    # 设置全局变量默认值
    GLOBALS_DICT = {
        # 配置项
        "Config":None,
        # 日志变量
        "g_logger":None,
        # 用于存放不同级别的文件/目录
        # 分别对应level 0 1 2
        "HighLevelFiles":list(),
        "MiddleLevelFiles":list(),
        "LowLevelFiles":list(),
        # 存放所有level的文件
        "OriFileBackup":list(),
        # 用于获取文件hash函数读取
        "CalculateHashFiles":list(),
        # 用于获取文件路径函数读取
        "AllFilePaths":list(),
        # 存放level 1 备份文件路径
        "StoreAllFilePath":"",
        # 存放level 0 备份文件hashcode路径
        "StoreAllBackupFileHashsPath":"",
        # 程序执行时间
        "CostTime":0.0,
        # 配置数据库相关
        "Host":"localhost",
        "User":"root",
        "Password":"123456",
        "Database":"FileBackUp",
        "Charset":"utf8mb4",
        # 配置运行模式-->数据库or文件，默认为文件
        "Module":False,
        # 数据库连接对象-->共用一个连接，避免浪费资源
        "Conn":None
    }
 
# 用于设置全局变量
def SetVar(name:str, value) -> bool:
    """设置Config"""
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False
 
# 用于获取全局变量
def GetVar(name:str):
    """取值Config"""
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"