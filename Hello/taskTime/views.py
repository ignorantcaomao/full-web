from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.cache import cache_page
from .models import workitems, jszc_info
import datetime
from django.shortcuts import render


# Create your views here.

# 给整个类函数添加装饰器
# 新增缓存装饰器
@method_decorator(cache_page(60 * 15), name='dispatch')
class WorkItemsView(View):
    # 默认返回一周的数据

    def get(self, request):
        # 默认取近7天的数据，如果有值，则按实际情况取数
        days = request.GET.get('days') if request.GET.get('days') else 7
        current = datetime.datetime.now() - datetime.timedelta(days=int(days))
        latest_workitems = workitems.objects.filter(
            created__gte=datetime.date(current.year, current.month, current.day))
        return render(request, template_name='workitems.html', context={'latest_workitems': latest_workitems})

    def post(self, request, *args, **kwargs):
        pass


class JszcClass(View):

    def get(self, request):
        current = datetime.datetime.now() + datetime.timedelta(days=-7)
        infos = jszc_info.objects.filter(created__gte=datetime.date(current.year, current.month, current.day))
        return render(request, context={'data': infos})
