from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .tasks import add


def async_celery(request):

    add.delay(3, 5)

    return HttpResponse('celery works')


def apply_celery(request):
    result = add.apply_async(args=[4, 8])
    return HttpResponse(result.task_id + ': ' + result.status)
