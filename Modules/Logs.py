########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-12-10 22:43:30
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-05-27 19:14:49
 # $ @FilePath: \YifanScripts\FileBackup\Modules\Logs.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
import logging
from pathlib import Path
from .GlobalVar import _init,SetVar,GetVar
import time
from .GetConfig import GetFromConfig,GetDBConfig
_init()
# 日志初始化
def InitLogger():
    # 设置控制台日志处理程序
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)

    # 设置文件日志处理程序
    file_handler = logging.FileHandler('FileBackup.log',encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 设置日志记录器
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(msecs)d %(name)s %(levelname)s \
                        %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    # 创建日志记录器
    SetVar('g_logger',logging.getLogger(__name__))

    GetVar('g_logger').setLevel(logging.DEBUG)
    # g_logger.addHandler(console_handler)
    GetVar('g_logger').addHandler(file_handler)

# 清空日志文件
def ClearLogFile():
    filename = 'FileBackup.log'
    log_file = Path(filename)

    if log_file.exists():
        log_file.write_text('')
    else:
        pass

# 预处理
def PreTreatment():
    ClearLogFile()
    InitLogger()
    # 添加工具开头标志加入日志
    starting_banner = ('\n' + '-' * 70 + '\n' +
                   f"\n\tStarted At {time.ctime()}  @Athouer:dikesi"
                   + '\n\n' + '-' * 70 + '\n')
    GetVar('g_logger').info(f"{starting_banner}")

# 备份文件的初始化
def InitOriFileBackup(args:object):
    '''
    args:脚本接收的参数
    '''
    HighLevelFiles=GetVar('HighLevelFiles')
    MiddleLevelFiles=GetVar('MiddleLevelFiles')
    LowLevelFiles=GetVar('LowLevelFiles')
    GetVar('OriFileBackup')
    CalculateHashFiles=GetVar('CalculateHashFiles')
    AllFilePaths=GetVar('AllFilePaths')
    
    # 读取不同Level的文件
    GetFromConfig('HighLevelFiles',HighLevelFiles)
    GetFromConfig('MiddleLevelFiles',MiddleLevelFiles)
    GetFromConfig('LowLevelFiles',LowLevelFiles)

    # 读取数据库相关配置
    GetDBConfig()
    
    SetVar('OriFileBackup',[{'0':HighLevelFiles},{'1':MiddleLevelFiles},{'2':LowLevelFiles}])
    for i in HighLevelFiles:
        # 获取用于差异备份文件的路径
        CalculateHashFiles.append(args.output+i[2:])

    for j in MiddleLevelFiles:
        # 获取用于增量备份的文件路径
        AllFilePaths.append(args.output+j[2:])