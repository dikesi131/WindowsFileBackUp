########################################################################
 # $ @Author: d1k3si
 # $ @Date: 2024-05-27 17:33:13
 # $ @LastEditors: d1k3si
 # $ @LastEditTime: 2024-06-04 22:14:49
 # $ @email:2098415680@qq.com
 # $ @Copyright (c) 2024 by d1k3si
########################################################################
from .GlobalVar import GetVar
import pymysql
def clear_file_content(file_paths:list) -> None:
    '''
    file_paths:要清空的记录备份文件路径/hashcode的文件
    '''
    assert isinstance(file_paths,list), "file_paths should be a list"
    try:
        for file_path in file_paths:
            # Open the file in write mode to clear its content
            with open(file_path, 'w') as file:
                file.truncate(0)  
                # Truncate the file to remove its content
            GetVar('g_logger').info("func clear_file_content error:Stored File content cleared successfully.")
    except FileNotFoundError:
        GetVar('g_logger').error("func clear_file_content error:Stored File_list '{0}' not found.".format(','.join(file_paths)))
    except IOError:
        GetVar('g_logger').error("func clear_file_content error:Error occurred while clearing content of '{0}'.".format(','.join(file_paths)))

def clear_table(table_names:list) -> None:
    '''
    table_names:要清空的表名列表
    '''
    assert isinstance(table_names,list),'table_name must be a list'
    try:
        conn=GetVar('Conn')
        # Create a cursor object
        cursor = conn.cursor()

        for table_name in table_names:
            # Check if the table exists
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()

            if result:
                # Execute SQL command to delete all records from the table
                cursor.execute(f"TRUNCATE {table_name}")

                # Commit the changes
                conn.commit()

                GetVar('g_logger').info(f"All records deleted from table '{table_name}' successfully.")
            else:
                GetVar("g_logger").info(f"Table '{table_name}' does not exist.")

    except pymysql.Error as e:
        GetVar('g_logger').error("Error occurred while clearing tables:", e)