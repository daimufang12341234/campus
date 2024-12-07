"""
项目初始化文件
用于配置 MySQL 数据库连接
"""

import pymysql
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()
