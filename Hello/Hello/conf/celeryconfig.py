# 最重要的配置，设置消息broker， 格式： db://user:password@host:port/dbname
# 如果redis安装在本地，使用localhost
# 如果docker部署的redis，使用redis：//redis:6379

CELERY_BROKER_URL = 'redis://172.16.206.203:6379/0'

# celery时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'

# 为django_celery_result存储Celery任务执行结果设置后台
# 格式： db+scheme://user:password@host:port/dbname
# 支持数据库django-db 和django-cache存储任务状态及结果
# CELERY_RESULT_BACKEND = 'redis://172.16.206.203:6379/0'

# 注释掉django\db\backends\base\base.py 552行的raise
CELERY_RESULT_BACKEND = "django-db"

# celery内容等消息的格式设置，默认json

CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
CELERY_TASK_TIME_LIMIT = 5

# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。
# 设为0，存储结果永不过期
CELERY_RESULT_EXPIRES = 0

# 任务限流
CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

# Worker并发数量，一般默认CPU核数，可以不设置
CELERY_WORKER_CONCURRENCY = 2

# 每个worker执行了多少任务就会死掉，默认是无限的
CELERY_WORKER_MAX_TASKS_PER_CHILD = 200

# 定时任务配置
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
DJANGO_CELERY_BEAT_TZ_AWARE = False