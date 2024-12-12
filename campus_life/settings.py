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
ALLOWED_HOSTS = ['yueliyue0210.cn', 'www.yueliyue0210.cn', 'localhost', '127.0.0.1']  # 暂时使用 IP

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
    'posts.middleware.DailyStatisticsMiddleware',
]

# 根URL配置
ROOT_URLCONF = "campus_life.urls"

# 模板配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'posts/templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "posts.context_processors.notifications",
                "posts.context_processors.post_categories",
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
        'USER': 'root',           # 使用 root 用户
        'PASSWORD': '138e2cc2b2d3cac1',  # 使用正确的 root 密码
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 60,
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
STATIC_URL = '/static/'  # 静态文件的URL前缀
STATIC_ROOT = '/www/project/2.0/campus_life/static'  # 生产环境静态文件收集目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),  # 开发环境静态文件目录
]

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = '/www/project/2.0/campus_life/media'

# 确保目录存在
os.makedirs(os.path.join(MEDIA_ROOT, 'avatars'), exist_ok=True)

# 文件上传配置
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o775

# 默认主键字段类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 认证相关配置
LOGIN_URL = 'login'  # 登录页面URL
LOGIN_REDIRECT_URL = 'posts:post_list'  # 登录成功后重定向URL
LOGOUT_REDIRECT_URL = 'posts:post_list'  # 退出登录后重定向URL

# 安全设置
SECURE_SSL_REDIRECT = False  # 暂时关闭强制 HTTPS 重定向
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 代理设置
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5分钟缓存
    }
}

# 会话设置
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# 静态文件设置
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB