from pathlib import Path
from .GlobalVar import g_logger
# 获取文件/目录大小
def GetSize(path):
    """Gets file size, or total directory size"""
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        size = 0
        for file in path.glob('**/*'):
            if file.is_file():
                size += file.stat().st_size
        return size
    else:
        g_logger.error(f"[ERROR]获取{path.name}大小失败")
        return 0

# 将获取到的文件/目录大小转化为易读的MB/GB等格式
def FormatSize(path,unit='MB'):
    """ Converts integers to common size units used in computing """
    assert isinstance(path,str),'Path must be a string'
    path=Path(path)
    bit_shift = {"B": 0,
            "kb": 7,
            "KB": 10,
            "mb": 17,
            "MB": 20,
            "gb": 27,
            "GB": 30,
            "TB": 40,}
    assert unit in bit_shift,'InValid unit'
    return "{:,.0f}".format(GetSize(path) / float(1 << bit_shift[unit])) + " " + unit