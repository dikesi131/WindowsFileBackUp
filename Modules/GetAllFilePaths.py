########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-12-09 23:12:44
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 19:20:10
 # $ @FilePath: \undefinedd:\YifanScripts\FileBackup\Modules\GetAllFilePaths.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
from pathlib import Path
import sys
import time
from .CheckFileup import IsFileEmpty,IsTableEmpty
from .GlobalVar import GetVar,SetVar
from .DBoperations import insert_path_data
from .CheckMode import check_mode
from Modules import GetParameter
# GetAllFilePaths函数修饰器
def GetAllFilePathsFunc(func):
    def wrapper(*args, **kwargs):
        parser=GetParameter.GetParameters()
        parm=parser.parse_args()
        mode=parm.mode
        # when (mode is db and table is empty) or (mode is file and file is empty)
        if (IsFileEmpty(GetVar("StoreAllFilePath")) and (not check_mode(mode))) \
        or (IsTableEmpty('File_paths') and check_mode(mode)):
            GetVar("g_logger").info('[+]Start Getting All Files Paths')
            StartTime=time.time()
            func(*args, **kwargs)
            EndTime=time.time()
            GetVar("g_logger").info("[-]End Getting All Files Paths")
            # 将时间转化为 小时-分钟-秒的格式
            SetVar("CostTime",GetVar("CostTime")+(EndTime-StartTime))
        else:
            GetVar('g_logger').info("[DONE]文件名已有备份")

    return wrapper

# 用于获取level 1下所有的文件路径（递归获取），这里是用来获取备份的所有文件路径
# 用于增量备份
@GetAllFilePathsFunc
def GetAllFilePaths(SourcePaths:list,args:object) -> None:
    assert isinstance(SourcePaths,list),'SourcePaths must be a list'
    '''
    sourcepaths:这里指Level 1下所有的文件路径
    args:脚本传入的参数
    '''
    file_set = set()
    for path in SourcePaths:
        path_obj = Path(path)
        # 检查目标文件所在的目录是否存在，如果不存在就创建
        if not path_obj.exists():
            path_obj.mkdir(parents=True)
        
        if path_obj.is_file():
            GetVar('g_logger').error("Function GetAllFilePaths ERROR: path is not a directory")
            sys.exit(1)
        elif path_obj.is_dir():
            for file in path_obj.rglob('*'):
                if file.is_file():
                    # 这里切片需要从备份到的目录名长度开始
                    file_set.add(str(file)[(len(Path(args.output).name)+3):])
                    # 这里的加3是为了处理盘符
        else:
            raise ValueError("Invalid path specified.")
    if args.mode=='file':
        # 写入到文件中，便于存储和后续处理
        with open(GetVar("StoreAllFilePath"), 'w',encoding='utf-8') as f:
            f.write('\n'.join(file_set))
    else:
        insert_path_data(file_set,'File_paths',isend=False)
    GetVar('g_logger').info(f"[SUCCESS]备份目录下所有文件名已写入")