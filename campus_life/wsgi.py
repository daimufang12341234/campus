"""
WSGI（Web Server Gateway Interface）配置文件
用于在生产环境中部署Django应用

WSGI是Python Web应用程序或框架和Web服务器之间的一种接口，
它提供了一种标准的方式让Web服务器与Python应用程序进行通信。
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django使用的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_life.settings')

# 创建WSGI应用程序对象
# 这个对象将被Web服务器（如Apache、Nginx+uWSGI等）用来与Django应用程序通信
application = get_wsgi_application()
