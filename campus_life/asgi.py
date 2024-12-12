"""
ASGI（Asynchronous Server Gateway Interface）配置文件
用于在支持异步的服务器上部署Django应用

ASGI是WSGI的继任者，它提供了一个标准接口，
允许Python异步web应用程序与web服务器进行通信。
它支持HTTP、WebSocket等多种协议。
"""

import os

from django.core.asgi import get_asgi_application

# 设置Django使用的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_life.settings')

# 创建ASGI应用程序对象
# 这个对象将被异步Web服务器（如Daphne、Uvicorn等）用来与Django应用程序通信
application = get_asgi_application()
