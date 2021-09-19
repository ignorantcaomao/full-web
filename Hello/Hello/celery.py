import os
import json
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')

# 实例化
app = Celery('Hello')

# namespace='CELERY' 作用是允许你在Django配置文件中对celery进行配置
# 但所有Celery配置项必须以celery开头，防止冲突
# app.config_from_object('django.conf:conf', namespace='CELERY')
app.config_from_object('django.conf.conf', namespace='CELERY')

# 自动从Django的已注册app中发现任务
app.autodiscover_tasks()


# 一个测试任务
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print(type(self.request))
    # return json.loads(self.request)

# 启动celery的时候，如果适用的是eventlet
# https://blog.csdn.net/u014007037/article/details/86645862?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link
# https://blog.csdn.net/u014007037/article/details/86645862?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.no_search_link