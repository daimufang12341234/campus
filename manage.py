#!/usr/bin/env python
"""
Django的命令行工具，用于管理项目
主要功能包括：
- 运行开发服务器 (runserver)
- 创建数据库迁移 (makemigrations)
- 应用数据库迁移 (migrate)
- 创建超级用户 (createsuperuser)
- 收集静态文件 (collectstatic)
等等
"""
import os
import sys

def main():
    """
    主函数，设置Django环境并执行命令行命令
    """
    # 设置Django的默认配置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_life.settings')
    
    try:
        # 导入Django的命令行工具
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，给出友好的错误提示
        raise ImportError(
            "无法导入Django。你确定它已经安装了吗？"
            "安装Django: pip install django"
        ) from exc
    
    # 执行命令行命令
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # 当直接运行此文件时执行main函数
    main()
