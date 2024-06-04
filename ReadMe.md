# What is this tool for?

主要用于解决Windows下备份文件需要手动确认是否覆盖文件，不够自动化和快捷，于是写了一个可以自动化读取配置并进行备份文件的项目

目前实现功能如下：

- 完全备份
- 增量备份
- 差异备份

## 完全备份

即将原目录完全copy到指定目录下，采用强制覆盖模式

## 增量备份

即只备份较上一次增加的文件

## 差异备份

即只备份较上一次有修改的文件

# How to use?

- python3+

```py
usage: FileBackup.py [-h] [-o OUTPUT] [-m {db,file}] [-c {yes,no}]
用于进行文件的备份

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        请输入要备份到的目录
  -m {db,file}, --mode {db,file}
                        请输入要使用的模式[db/file],default=file
  -c {yes,no}, --clear {yes,no}
                        是否清除已备份文件的记录[yes/no],default=no
```

# How to config?

> 使用工具前请将config-example内容复制，保存为项目目录下的config.yaml文件

## config-example

```yaml
# 按照文件修改程度/频率不同进行分级别
# HighLevel表示要进行文件内容的修改和文件增删
# MiddleLevel表示文件内容的增删但文件内容几乎不变
# LowLevel表示文件几乎不变
MiddleLevelFiles:
  - HighLevelFiles:
    # HighLevel
    - filename1: "filepath1"
    - filename2: "filepath2"
    - xxx: "xxx"
  # MiddleLevel
  - filename1: "filepath1"
  - filename2: "filepath2"
  - xxx: "xxx"

LowLevelFiles:
  # LowLevel
  - filename1: "filepath1"
  - filename2: "filepath2"
  - xxx: "xxx"

# 存放MiddleLevel备份文件路径
StoreAllFilePath: "AllBackupFileNames.txt"
# 存放HighLevel备份文件hashcode路径
StoreAllBackupFileHashsPath: "AllBackupFileHashs.txt"

# 数据库相关配置
DBConfig:
  - Host: "localhost"
  - User: "root"
  - Password: "xxx"
  - Database: "xxx"
  - Charset: "xxx"

# 发送邮件相关
# QQ邮箱
email: 'xxx@xxx.com'
# 邮箱授权码
PassCode: 'xxx'
# SMTP服务端口(默认为25)
port: 25
# 收件人
SendTo: "xxx@xxx.com"
```

## 文件配置

```yaml
# 按照文件修改程度/频率不同进行分级别
# HighLevel表示要进行文件内容的修改和文件增删
# MiddleLevel表示文件内容的增删但文件内容几乎不变
# LowLevel表示文件几乎不变
MiddleLevelFiles:
  - HighLevelFiles:
    # HighLevel
    - filename1: "filepath1"
    - filename2: "filepath2"
    - xxx: "xxx"
  # MiddleLevel
  - filename1: "filepath1"
  - filename2: "filepath2"
  - xxx: "xxx"

LowLevelFiles:
  # LowLevel
  - filename1: "filepath1"
  - filename2: "filepath2"
  - xxx: "xxx"
```

>将filename和filepath修改为实际文件名/文件路径即可
>
>- HighLevel为差异备份和增量备份
>- MiddleLevel为增量备份
>- LowLevel为完全备份

## 邮箱相关配置

```yaml
# 发送邮件相关
# QQ邮箱
email: xxx
# 邮箱授权码
passcode: xxx
# SMTP服务端口(默认为25)
port: xxx
```

>脚本使用的是QQ邮箱，邮箱和授权码请改为自已的
>
>如果需要使用其他邮箱，可能需要更改Modules/SendEmail函数使其满足你的需求

## 数据库配置

```yaml
DBConfig:
  - Host: "localhost"
  - User: "root"
  - Password: "xxx"
  - Database: "xxx"
  - Charset: "xxx"
```

>将数据库配置改为实际的，存放已备份文件路径的表默认为file_paths，存放已备份文件hashcode的表默认为file_hashcode，其中file_paths用于增量备份，file_hashcode用于差异备份