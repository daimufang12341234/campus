"""
Django项目的主要配置文件
包含了项目的所有核心设置
"""

from pathlib import Path
import os
import pymysql
pymysql.install_as_MySQLdb()  # 使用pymysql替代MySQLdb

# 构建项目的基础目录路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全警告：生产环境中需要保密的密钥
SECRET_KEY = "django-insecure-#!kag5prfy2ds_jox%y%&b)7bovka#)mp$fjsf8y=i^0(w4e1y"

# 调试模式：生产环境中应该设置为False
DEBUG = True

# 允许访问的主机列表
ALLOWED_HOSTS = ['*']  # '*'表示允许所有主机，生产环境应该指定具体域名

# 应用定义
INSTALLED_APPS = [
    # Django内置应用
    "django.contrib.admin",        # 管理后台
    "django.contrib.auth",         # 认证系统
    "django.contrib.contenttypes", # 内容类型框架
    "django.contrib.sessions",     # 会话框架
    "django.contrib.messages",     # 消息框架
    "django.contrib.staticfiles",  # 静态文件管理
    
    # 自定义应用
    "posts",  # 帖子应用
]

# 中间件配置
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",         # 安全中间件
    "django.contrib.sessions.middleware.SessionMiddleware",  # 会话中间件
    "django.middleware.common.CommonMiddleware",            # 通用中间件
    "django.middleware.csrf.CsrfViewMiddleware",            # CSRF保护
    "django.contrib.auth.middleware.AuthenticationMiddleware", # 认证中间件
    "django.contrib.messages.middleware.MessageMiddleware",  # 消息中间件
    "django.middleware.clickjacking.XFrameOptionsMiddleware", # 点击劫持保护
]

# 根URL配置
ROOT_URLCONF = "campus_life.urls"

# 模板配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # 模板引擎
        "DIRS": [os.path.join(BASE_DIR, 'templates')],  # 模板目录
        "APP_DIRS": True,  # 是否在应用中查找模板
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",  # 媒体文件处理
            ],
        },
    },
]

# WSGI应用配置
WSGI_APPLICATION = "campus_life.wsgi.application"

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campus_life',
        'USER': 'root',
        'PASSWORD': 'fgx28474',
        'HOST': 'dbconn.sealoshzh.site',
        'PORT': '49697',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 60,
            'autocommit': True,
        }
    }
}

# 密码验证配置
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # 用户属性相似性验证
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # 最小长度验证
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # 常用密码验证
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # 数字密码验证
    },
]

# 国际化配置
LANGUAGE_CODE = "zh-hans"  # 使用中文
TIME_ZONE = "Asia/Shanghai"  # 使用中国时区
USE_I18N = True  # 启用国际化
USE_TZ = True  # 启用时区

# 静态文件配置
STATIC_URL = '/static/'  # 静态文件URL前缀
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 静态文件收集目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 额外的静文件目录
]

# 媒体文件配置
MEDIA_URL = '/media/'  # 媒体文件URL前缀
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 媒体文件存储目录

# 默认主键字段类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 认证相关配置
LOGIN_URL = 'login'  # 登录页面URL
LOGIN_REDIRECT_URL = 'posts:post_list'  # 登录成功后重定向URL
LOGOUT_REDIRECT_URL = 'posts:post_list'  # 退出登录后重定向URL
