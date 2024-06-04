########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-12-10 22:43:30
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-05-29 21:52:28
 # $ @FilePath: \YifanScripts\FileBackup\Modules\GetConfig.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
import yaml
from .GlobalVar import GetVar,SetVar
# 加载config.yaml文件
def LoadConfig():
    with open("config.yaml",'r',encoding="utf-8") as f:
        SetVar('Config',yaml.load(f.read(),Loader=yaml.FullLoader))

# 从config.yaml文件中获取设定项
def GetFromConfig(ConfigName:str,Files:list) -> None:
    LoadConfig()
    assert ConfigName in ['HighLevelFiles','MiddleLevelFiles','LowLevelFiles'],'Error: Unknown Config'
    '''
    configname:这里指config.yaml中的配置名
    files:这里指HighLevelFiles/MiddleLevelFiles等所有文件的文件路径的list,配合globalvar
    '''
    # 获取LowLevel
    if ConfigName=='LowLevelFiles':
        for FileDict in GetVar('Config')[ConfigName]:
            for value in FileDict.values():
                Files.append(value)
    
    # 获取MiddleLevel
    elif ConfigName=='MiddleLevelFiles':
        for FileDict in GetVar('Config')[ConfigName][1:]:
            for value in FileDict.values():
                Files.append(value)
    
    #获取HighLevel 
    elif ConfigName=='HighLevelFiles': 
        for DictList in GetVar('Config')['MiddleLevelFiles'][0].values():
            for dic in DictList:
                for value in dic.values():
                    Files.append(value)
    else:
        pass

    # 读取备份文件/文件hash的文件路径
    SetVar("StoreAllFilePath",GetVar('Config')['StoreAllFilePath'])
    SetVar("StoreAllBackupFileHashsPath",GetVar('Config')['StoreAllBackupFileHashsPath'])

# 获取数据库相关配置
def GetDBConfig():
    # 必须globalvar中全局变量和config.yaml中的数据库相关配置命名相同
    for file_dict in GetVar('Config')['DBConfig']:
        for key,value in file_dict.items():
            SetVar(key,value)