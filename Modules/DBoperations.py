########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-05-26 00:08:59
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-03 19:22:25
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
import pymysql
from .GlobalVar import GetVar,SetVar
# 数据库连接
def init_db_connection() -> None:
    # 连接数据库
    conn = pymysql.connect(host=GetVar('Host'),
                           user=GetVar('User'),
                           password=GetVar('Password'),
                           database=GetVar('Database'),
                           charset=GetVar('Charset'),
                           cursorclass=pymysql.cursors.DictCursor)
    SetVar('Conn',conn)

def check_data_in_table(data:str, table_name:str,column_name:str) -> bool:
    assert isinstance(data,str),'data must be a string'
    assert isinstance(table_name,str),'table_name must be a string'
    assert isinstance(column_name,str),'column_name must be a string'
    '''
    data:要检查的数据
    table_table:要检查的表
    column_name:要检查的列
    '''
    conn=GetVar('Conn')
    try:
        with conn.cursor() as cursor:
            # 构造 SQL 查询语句
            sql = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
            
            # 执行查询
            cursor.execute(sql, (data,))
            
            # 获取查询结果
            result = cursor.fetchone()
            
            # 如果结果不为空，则表示字符串存在于表中
            if result:
                return True
            else:
                return False
    except Exception as e:
        GetVar('g_logger').error('error: %s' % e)

# 数据库插入文件路径
def insert_path_data(data:set, table_name:str,isend=True) -> None:
    assert isinstance(data,set),'data must be a set'
    assert isinstance(table_name,str),'table_name must be a string'
    '''
    data:插入的数据,形如value1,value2,value3,......
    table_name:要插入的表名
    isend:指定是否执行conn.close()
    '''
    # 连接数据库
    conn = GetVar('Conn')
    try:
        with conn.cursor() as cursor:
            # 检查表是否已存在，如果不存在则创建表
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()
            if not table_exists:
                create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    path VARCHAR(255) NOT NULL
                )
                """
                cursor.execute(create_table_query)

            # 开启事务
            conn.begin()
            # 插入数据
            sql = f"INSERT INTO {table_name} (path) VALUES (%s)"
            # 将集合转换为一个以元组为元素的列表
            values = [(value,) for value in iter(data)]
            # executemany use to insert values,values must be like [(1,),(2,),(3,),(4,),]
            cursor.executemany(sql, values)

        # 提交事务
        conn.commit()
        GetVar('g_logger').info("Data inserted successfully!")

    except Exception as e:
        # 发生异常时回滚事务
        conn.rollback()
        GetVar('g_logger').error("Error inserting data:", e)

    if isend:
        # 只有最后一个数据库操作函数执行关闭数据库连接操作
        # 关闭数据库连接
        conn.close()
    else:
        pass

# 数据库插入文件hashcode
def insert_hashcode_data(data:set, table_name:str,isend=True) -> None:
    assert isinstance(data,set),'data must be a set'
    assert isinstance(table_name,str),'table_name must be a string'
    '''
    data:插入的数据,形如value1,value2,value3,......
    table_name:要插入的表名
    isend:指定是否执行conn.close()
    '''
    # 连接数据库
    conn = GetVar('Conn')
    try:
        with conn.cursor() as cursor:
            # 检查表是否已存在，如果不存在则创建表
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()
            if not table_exists:
                create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hashcode VARCHAR(255) NOT NULL
                )
                """
                cursor.execute(create_table_query)

            # 开启事务
            conn.begin()
            # 插入数据
            sql = f"INSERT INTO {table_name} (hashcode) VALUES (%s)"
            # 将集合转换为一个以元组为元素的列表
            values = [(value,) for value in iter(data)]
            cursor.executemany(sql, values)

        # 提交事务
        conn.commit()
        GetVar('g_logger').info("Data inserted successfully!")

    except Exception as e:
        # 发生异常时回滚事务
        conn.rollback()
        GetVar('g_logger').error("Error inserting data:", e)

    if isend:
        # 只有最后一个数据库操作函数执行关闭数据库连接操作
        # 关闭数据库连接
        conn.close()
    else:
        pass