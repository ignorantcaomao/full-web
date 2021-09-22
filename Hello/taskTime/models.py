from django.db import models


# Create your models here.
class workitems(models.Model):
    id = models.CharField(verbose_name='id', max_length=64, primary_key=True)
    text = models.CharField(verbose_name='工作内容', max_length=255, default=None)
    author = models.CharField(verbose_name='填写人', max_length=128)
    idReadable = models.CharField(verbose_name='任务号', max_length=128)
    duration = models.IntegerField(verbose_name='工作量', default=0)
    created = models.DateTimeField(verbose_name='填写日期')

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['-created', 'author', 'idReadable']


class jszc_info(models.Model):
    id = models.CharField(verbose_name='id', max_length=128, primary_key=True)
    author = models.CharField(verbose_name='执行人', max_length=128)
    taskName = models.CharField(verbose_name='任务名称', max_length=255)
    department = models.CharField(verbose_name='部门', max_length=255)
    projectName = models.CharField(verbose_name='项目名称', max_length=255)
    created = models.DateTimeField(verbose_name='创建时间')
    updated = models.DateTimeField(verbose_name='更新时间')
    projectId = models.CharField(verbose_name='任务编号', max_length=128)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['-updated', '-created', 'author']
