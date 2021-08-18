from .celery import app as celery_app
import pymysql
# 自定义对外暴露接口
__all__ = ['celery_app']

pymysql.install_as_MySQLdb()