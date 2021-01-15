"""
使用celery搭建一步程序，学习使用该程序来实现"异步发送短信"
# 安装到虚拟环境, 你懂得~
pip install Celery -i https://pypi.tuna.tsinghua.edu.cn/simple

# main.py文件，是我们异步程序的主脚本文件(相当于django中的manage.py)
"""

from celery import Celery

# 1、创建异步程序对象
celery_app = Celery('meiduo')

# 2、加载配置文件
# 注意：我们异步程序是在celery_tasks包所在目录作为工作目录运行的。
celery_app.config_from_object('celery_tasks.config')

# 3、注册异步任务 —— 异步任务是以python包的形式封装的
celery_app.autodiscover_tasks([
    'celery_tasks.sms', # sms任务包的导包路径
])



