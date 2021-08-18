import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')

# 实例化
app = Celery('Hello')

# namespace='CELERY' 作用是允许你在Django配置文件中对celery进行配置
# 但所有Celery配置项必须以celery开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')


# 自动从Django的已注册app中发现任务
app.autodiscover_tasks()

# 一个测试任务
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.requets!r}')
