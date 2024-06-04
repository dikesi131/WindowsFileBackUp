########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-01-09 16:55:34
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-05-31 16:59:05
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
from pathlib import Path
from .GlobalVar import _init,GetVar
import sys
_init()
# 用于检测是否已经有过备份
def CheckBackupPath(path:str) -> bool:
    assert isinstance(path,str),'path must be a string'
    '''
    path:备份文件的路径
    '''
    path = Path(path)
    if not path.exists():
        GetVar('g_logger').error("[ERROR]备份文件路径不存在")
        sys.exit(1)
    if any(path.iterdir()):
        return True
    return False

# 检查StoreAllFilePath和StoreAllBackupFileHashsPath所指文件路径是否为空，不为空则表明已有备份
def IsFileEmpty(file_path:str) -> bool:
    path = Path(file_path)
    if not path.exists():
        path.touch()
        return True
    return path.stat().st_size == 0

# 检查表是否为空，不为空则表示已有备份
def IsTableEmpty(table_name:str) -> bool:
    conn=GetVar('Conn')
    try:
        with conn.cursor() as cursor:
            # 查询表中是否有数据
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchone()
            count = result['count']
            return count == 0

    except Exception as e:
        GetVar('g_logger').error("Error checking if table is empty:", e)