########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-12-09 23:08:48
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 19:27:01
 # $ @FilePath: \YifanScripts\FileBackup\Modules\IncrementalBackup.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
from pathlib import Path
import shutil
import time
from .GlobalVar import GetVar,SetVar
from .DBoperations import insert_path_data,check_data_in_table

# 增量备份函数修饰器
def IncrementalBackupsFunc(func):
    def wrapper(*args, **kwargs):
        GetVar('g_logger').info("[+]IncrementalBackups Start")
        StartTime=time.time()
        func(*args, **kwargs)
        EndTime=time.time()
        GetVar('g_logger').info("[-]IncrementalBackups End")
        # 将时间转化为 小时-分钟-秒的格式
        SetVar("CostTime",GetVar("CostTime")+(EndTime-StartTime))
        # SendEmail()

    return wrapper

# 增量备份
@IncrementalBackupsFunc
def IncrementalBackups(source_paths:list, dest_path:str,mode_check:bool) -> None:
    '''
    source_paths is a list of dict, 用来存储不同level的文件目录
    dest_path 是要备份到的路径
    module_check:决定数据库or文件模式,true-->数据库,false-->文件
    '''
    assert isinstance(source_paths, list), 'source paths must be a list'
    assert isinstance(dest_path, str), 'dest path must be a str'
    assert isinstance(mode_check, bool), 'module check must be boolean'

    # 读取已备份好的文件列表
    backup_file = GetVar("StoreAllFilePath")
    backuped_files = set()
    if Path(backup_file).exists():
        with open(backup_file, 'r', encoding='utf-8') as f:
            backuped_files = set(f.read().splitlines())
    NewFilePaths=set()
    sql='INSERT INTO File_paths (path) VALUES (%s)'

    dest_path = Path(dest_path)
    # 检查目标备份目录是否存在，如果不存在就创建
    if not dest_path.exists():
        dest_path.mkdir(parents=True)
    # level 1才需要增量备份
    source_dict = source_paths[1]
    for source_path in source_dict['1']:
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
                # 通过切片操作把盘符去掉
                # (mode is file and file_path is not in backuped_files) or (mode is db and file_path is not in table)
                if ((str(file)[2:] not in backuped_files) and (not mode_check)) \
                or ((not check_data_in_table(str(file)[2:],'File_paths','path')) and mode_check):
                    try:
                        # 执行复制操作
                        # copy2函数必须要路径存在，否则会报错
                        shutil.copy2(file, dest_file_path)
                        if mode_check:
                            cursor=GetVar('Conn').cursor()
                            # conn.cursor()
                            cursor.execute(sql,(str(file)[2:],))
                            # execute use to insert,the value must be like (1,)
                        else:
                            NewFilePaths.add(str(file)[2:])
                        GetVar('g_logger').info(f"[SUCCESS] {file.name} >> backup successfully")
                    except IOError as e:
                        GetVar('g_logger').error(f"[ERROR] {file.name} >> backup error: {e}")
                else:
                    GetVar('g_logger').info(f"[DONE]{file.name} 已在备份文件列表中")
    # 数据库模式
    if mode_check:
        # 之后还有insert_hashcode_data要使用数据库连接，所以不能断开
        insert_path_data(NewFilePaths,'File_paths',isend=False)
    else:
        # 更新已备份的文件列表
        with open(backup_file, 'a+', encoding='utf-8') as f:
            f.write('\n'.join(NewFilePaths))

    GetVar('g_logger').info("[SUCCESS] 备份目录下所有文件名已更新完成")