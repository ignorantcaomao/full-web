from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
    'jobs',
    'taskTime',
]

MIDDLEWARE += [
    # 'Hello.middleware.CustomMiddleware.LoginRequiredMiddleware',
    # 'Hello.middleware.CustomMiddleware.LimitTimes',
    'Hello.middleware.CustomMiddleware.TimeitMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'hello.sqlite3',
    }
}
