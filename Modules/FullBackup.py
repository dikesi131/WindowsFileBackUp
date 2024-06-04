import time
import subprocess
from pathlib import Path
from .GlobalVar import GetVar,SetVar
# 完全备份函数修饰器
def FullBackupFunc(func):
    def wrapper(*args, **kwargs):
        GetVar('g_logger').info("[+]FullBackup Start")
        StartTime=time.time()
        func(*args, **kwargs)
        EndTime=time.time()
        GetVar('g_logger').info("[-]FullBackup End")
        SetVar("CostTime",GetVar("CostTime")+(EndTime-StartTime))
        # 将时间转化为 小时-分钟-秒的格式
        GetVar("g_logger").info(f"[-]The Cost Time Is {time.strftime('%H:%M:%S',time.gmtime(GetVar('CostTime')))}")

    return wrapper

# 完全备份
@FullBackupFunc
def FullBackup(source_paths:list, dest_path:str) -> None:
    '''
    source_paths is a list of dict,用来存储不同level的文件目录
    dest_path是要备份到的路径
    '''
    assert isinstance(source_paths, list), 'source paths must be a list'
    assert isinstance(dest_path, str), 'dest path must be a str'
    
    dest_path = Path(dest_path)
    # 多层循环将文件路径取出
    for source_dict in source_paths:
        for source_list in source_dict.values():
            for source_path in source_list:
                source_path = Path(source_path)
                
                if source_path.is_dir():
                    dest_dir = dest_path / source_path.name
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    command = f'xcopy "{source_path}" "{dest_dir}" /E /I /Y'
                else:
                    command = f'copy "{source_path}" "{dest_path}" /Y'

                try:
                    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                    GetVar('g_logger').info(f"[SUCCESS] >> {source_path.name} << backup successfully")
                except subprocess.CalledProcessError as e:
                    GetVar('g_logger').error(f"[ERROR] >> {source_path.name} << backup error: {e.stderr}")

