########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-01-09 16:55:34
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 19:18:48
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
import hashlib
from pathlib import Path
import sys
import  time
from .CheckFileup import IsFileEmpty,IsTableEmpty
from .GlobalVar import GetVar,SetVar
from .DBoperations import insert_hashcode_data
from .CheckMode import check_mode
from Modules import GetParameter
# 计算文件的hash值，采用分块hash的方式计算，分块大小可调整
# 分块hash的好处在于处理大文件hash时效率提高
def CalculateHash(filepath:str, algorithm="md5", block_size=4096):
    """
        计算文件的块哈希值
        block_size表示分块的大小
    """
    hash_algo = hashlib.new(algorithm)
    with open(filepath, 'rb') as file:
        buffer = file.read(block_size)
        while len(buffer) > 0:
            hash_algo.update(buffer)
            buffer = file.read(block_size)
    return hash_algo.hexdigest()

# GetAllFilesHash函数修饰器
def GetAllFilesHashFunc(func):
    def wrapper(*args, **kwargs):
        parser=GetParameter.GetParameters()
        parm=parser.parse_args()
        mode=parm.mode
        # when (mode is db and table is empty) or (mode is file and file is empty)
        if (IsFileEmpty(GetVar("StoreAllBackupFileHashsPath")) and (not check_mode(mode))) \
        or (IsTableEmpty('File_hashcode') and check_mode(mode)):
            GetVar("g_logger").info('[+]Start Getting All Files HashCodes')
            StartTime=time.time()
            func(*args, **kwargs)
            EndTime=time.time()
            GetVar("g_logger").info("[-]End Getting All Files HashCodes")
            # 将时间转化为 小时-分钟-秒的格式
            SetVar("CostTime",GetVar("CostTime")+(EndTime-StartTime))
        else:
            GetVar("g_logger").info("[DONE]文件hashcode已有备份")
    
    return wrapper

@GetAllFilesHashFunc
# 获得level 0下所有文件的hash
def GetAllFilesHash(SourcePaths:list,mode_flag:bool) -> None:
    assert isinstance(SourcePaths,list),'SourcePaths must be a list'
    '''
    sourcepaths:这里为level 0的所有文件路径
    mode_flag:true-->数据库模式,false-->file模式
    '''
    hash_set = set()
    for path in SourcePaths:
        path_obj = Path(path)
        # 检查目标文件所在的目录是否存在，如果不存在就创建
        if not path_obj.exists():
            path_obj.mkdir(parents=True)
        
        if path_obj.is_file():
            GetVar("g_logger").error("Function GetAllFilePaths ERROR: path is not a directory")
            sys.exit(1)
        elif path_obj.is_dir():
            for file in path_obj.rglob('*'):
                if file.is_file():
                    hash_set.add(CalculateHash(file))
        else:
            raise ValueError("Invalid path specified.")
    if not mode_flag:
        # 写入到文件中，便于存储和后续处理
        with open(GetVar("StoreAllBackupFileHashsPath"), 'a+',encoding='utf-8') as f:
            f.write('\n'.join(hash_set))
    else:
        insert_hashcode_data(hash_set,'File_hashcode',isend=False)
    GetVar("g_logger").info(f"[SUCCESS]备份目录下所有文件HashCode已写入")