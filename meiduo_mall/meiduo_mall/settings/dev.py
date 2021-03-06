"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, sys, datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把apps文件夹路径, 加入导包路径
sys.path.insert(
    0,
    os.path.join(BASE_DIR, 'apps')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2m4)&8@0!w*ssk0@r#or-pk+cp=3zekvzbynxpg0z((uo6iro^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # 注册用户应用
    'corsheaders',  # 加载应用解决跨域问题
    'verifications',  # 验证码模块
    'oauth',  # QQ登陆模块
    'areas',  # 地区模块
    'contents',  # 注册 广告子应用:
    'goods',  # 商品
    'haystack',  # 全文检索
    'carts',  # 购物车
    'orders',  # 订单
    'payment',  # 支付
    'rest_framework',  # drf框架
    'meiduo_admin',  # 后台管理站点应用
]

MIDDLEWARE = [
    # 跨域中间件，作用：响应OPTIONS请求
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 添加这一行的配置信息, 把 templates的绝对路径导入到 [] 中:
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '192.168.209.130',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'yc',  # 数据库用户名
        'PASSWORD': '12345',  # 数据库用户密码
        'NAME': 'meiduo_mall_db'  # 数据库名字
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    # 默认存储信息: 存到 0 号库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.209.130:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # session 信息: 存到 1 号库
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.209.130:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码信息: 存到 2 号库
    "verify_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.209.130:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用户浏览记录 3 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.209.130:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 购物车存储 存到 5 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.209.130:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

ALLOWED_HOSTS = ['www.meiduo.site']
# 或者设置 通配域名
# ALLOWED_HOSTS = ['*']

# 指定django使用的自定义的用户模型类
# 注意，参数不是导包路径。是一种固定的格式："应用名.自定义用户模型类"
AUTH_USER_MODEL = 'users.User'

# CORS跨域请求白名单设置
CORS_ORIGIN_WHITELIST = [
    'http://www.meiduo.site:8080',  # 商城页面前端
    'http://www.meiduo.site:8081',  # 后台管理站点前端
    'http://www.meiduo.site:8000',
    '192.168.209.130:8000',
    '192.168.209.130:8080',
    '192.168.209.130:8081',
]
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

# QQ登录参数
# 我们申请的 客户端id
QQ_CLIENT_ID = '101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 我们申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

# 发送短信的相关设置, 这些设置是当用户没有发送相关字段时, 默认使用的内容:
# 发送短信必须进行的设置:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 我们使用的 发件smtp服务器 地址
EMAIL_HOST = 'smtp.163.com'
# 知名端口号
EMAIL_PORT = 25
# 下面的内容是可变的, 随后台设置的不同而改变
# 发送邮件的邮箱
EMAIL_HOST_USER = 'yuanchu1598@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'MQBANHBLZMFIOELL'
# 收件人看到的发件人
EMAIL_FROM = '袁楚<yuanchu1598@163.com>'
# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8080/success_verify_email.html?token='

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.FastDFSStorage'

# FastDFS相关参数
FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.209.130:9200/',  # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall',  # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 对接支付宝
ALIPAY_APPID = '2021000116681991'  # 应用ID
ALIPAY_DEBUG = True  # 调试模式，对接沙箱应用时为True,对接正式应用时为False
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'  # 对接支付宝的网关，如果对接沙箱应用就是测试网关
ALIPAY_RETURN_URL = "http://www.meiduo.site:8080/pay_success.html"  # 支付成功后的回调地址

# DRF框架配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # JSONWebTokenAuthentication功能：从头部中按照既定的格式提取token并校验
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT身份认证后端
        'rest_framework.authentication.SessionAuthentication',  # session身份认证机制
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# jwt拓展配置
JWT_AUTH = {
    # 设置jwt的token值的签发有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10),
    # 指定登陆响应参数构造函数
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'meiduo_mall.utils.custom_jwt_response_handler.jwt_response_payload_handler'
}

# BASE_DIR是内层目录
# FDFS_PATH是FDFS配置文件路径
FDFS_PATH = os.path.join(BASE_DIR, 'utils/client.conf')
