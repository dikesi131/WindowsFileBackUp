########################################################################
 # $ @Author: dikesi
 # $ @Date: 2024-01-09 16:55:34
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-04 23:01:58
 # $ @FilePath: \YifanScripts\FileBackup\Modules\DifferentialBackup.py
 # $ @Copyright (c) 2024 by dikesi
########################################################################
import time
from pathlib import Path
import shutil
import hashlib
from .GlobalVar import GetVar,SetVar
from .SendEmail import SendEmail
from .DBoperations import insert_hashcode_data,check_data_in_table

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

# 差异备份函数修饰器
def DifferentialBackupFunc(func):
    def wrapper(*args, **kwargs):
        GetVar("g_logger").info("[+]DifferentialBackup Start")
        StartTime=time.time()
        func(*args, **kwargs)
        EndTime=time.time()
        GetVar("g_logger").info("[-]DifferentialBackup End")
        # 将时间转化为 小时-分钟-秒的格式
        SetVar("CostTime",GetVar("CostTime")+(EndTime-StartTime))
        GetVar("g_logger").info(f"[-]The Cost Time Is {time.strftime('%H:%M:%S',time.gmtime(GetVar('CostTime')))}")
        SendEmail()

    return wrapper

# 差异备份
@DifferentialBackupFunc
def DifferentialBackup(source_paths:list,dest_path:str,mode_check:bool) -> None:
    '''
    source_paths is a list of dict, 用来存储不同level的文件目录
    dest_path 是要备份到的路径
    mode_check:决定数据库or文件模式,true-->数据库,false-->文件
    '''
    assert isinstance(source_paths, list), 'source paths must be a list'
    assert isinstance(dest_path, str), 'dest path must be a str'
    assert isinstance(mode_check, bool), 'module check must be boolean'

    # 读取已备份好的文件列表
    backup_file = GetVar("StoreAllBackupFileHashsPath")
    backuped_file_hashs=set()
    if Path(backup_file).exists():
        with open(backup_file, 'r', encoding='utf-8') as f:
            backuped_file_hashs = set(f.read().splitlines())
    NewFilesHashCode=set()
    sql='INSERT INTO File_hashcode (hashcode) VALUES (%s)'

    dest_path = Path(dest_path)
    # 检查目标备份目录是否存在，如果不存在就创建
    if not dest_path.exists():
        dest_path.mkdir(parents=True)
    # level 0才需要差异备份
    source_dict = source_paths[0]
    for source_path in source_dict['0']:
        source_path = Path(source_path)

        # 取出所有文件
        for file in source_path.glob('**/*'):
            if file.is_file():
                # 设置copy到的位置，保持原有目录结构不变
                dest_file_path = dest_path / source_path.name / file.relative_to(source_path)
                dest_file_directory = dest_file_path.parent
                # 检查目标文件所在的目录是否存在，如果不存在就创建
                if not dest_file_directory.exists():
                    dest_file_directory.mkdir(parents=True)
                # (mode is file and file_hashcode is not in backuped_files_hashs) or (mode is db and file_hashcode is not in table)
                if ((CalculateHash(str(file)) not in backuped_file_hashs) and (not mode_check))\
                or ((not check_data_in_table(CalculateHash(str(file)),'File_hashcode','hashcode')) and mode_check):
                    try:
                        # 执行复制操作
                        # copy2函数必须要路径存在，否则会报错
                        shutil.copy2(file, dest_file_path)
                        if mode_check:
                            cursor=GetVar('Conn').cursor()
                            cursor.execute(sql,(CalculateHash(str(file)),))
                        else:
                            NewFilesHashCode.add(CalculateHash(str(file)))
                        GetVar("g_logger").info(f"[SUCCESS] {file.name} >> backup successfully")
                    except IOError as e:
                        GetVar("g_logger").error(f"[ERROR] {file.name} >> backup error: {e}")
                else:
                    GetVar("g_logger").info(f"[DONE]{file.name} 文件HashCode已在备份文件列表中")

    # 数据库模式
    if mode_check:
        insert_hashcode_data(NewFilesHashCode,'File_hashcode',isend=True)
    else:
        # 更新已备份的文件列表
        with open(backup_file, 'a+', encoding='utf-8') as f:
            f.write('\n'.join(NewFilesHashCode))

    GetVar("g_logger").info("[SUCCESS] 备份目录下所有文件HashCode已更新完成")