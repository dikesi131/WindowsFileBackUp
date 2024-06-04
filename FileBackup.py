########################################################################
 # $ @Author: dikesi
 # $ @Date: 2023-11-20 13:19:35
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-04 22:13:55
 # $ @FilePath: \YifanScripts\FileBackup\FileBackup.py
 # $ @Copyright (c) 2023 by dikesi
########################################################################
import sys
# 将自定义包路径加入系统，让python解释器能找到自定义包的位置
sys.path.append("FileBackup\Modules")
from Modules.GlobalVar import GetVar
from Modules import Logs
from Modules import GetParameter
from Modules import FullBackup
from Modules import GetAllFilePaths
from Modules import IncrementalBackup
from Modules import GetAllFileHashs
from Modules import DifferentialBackup
from Modules import CheckFileup
from Modules import Clear
from Modules.DBoperations import init_db_connection
from Modules.CheckMode import check_mode
from Modules.CheckRecord import check_record

def main():
    Logs.PreTreatment()
    parser=GetParameter.GetParameters()
    args=parser.parse_args()
    mode_flag=check_mode(args.mode)
    clear_flag=check_record(args.clear)
    # 数据库链接设置
    init_db_connection()
    # 判断是否先进行清除备份记录
    if clear_flag and (not mode_flag):
        # clear file records
        Clear.clear_file_content([GetVar('StoreAllFilePath'),GetVar('StoreAllBackupFileHashsPath')])
    elif clear_flag and mode_flag:
        # clear table records
        Clear.clear_table(['File_paths','File_hashcode'])
    else:
        pass
    Logs.InitOriFileBackup(args=args)
    # 如果备份目录不存在或为空，表示还没有进行备份
    if not CheckFileup.CheckBackupPath(args.output):
        # 进行完全备份
        FullBackup.FullBackup(GetVar("OriFileBackup"),args.output)
    else:
        # 进行增量备份
        GetAllFilePaths.GetAllFilePaths(GetVar("AllFilePaths"),args=args)
        IncrementalBackup.IncrementalBackups(GetVar("OriFileBackup"),args.output,mode_flag)
        # 进行差异备份
        GetAllFileHashs.GetAllFilesHash(GetVar("CalculateHashFiles"),mode_flag)
        DifferentialBackup.DifferentialBackup(GetVar("OriFileBackup"),args.output,mode_flag)
    
if __name__=='__main__':
    main()
    