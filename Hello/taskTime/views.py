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
class BaseView(View):
    model_name = None

    def get(self, request):
        # 默认取近7天的数据，如果有值，则按实际情况取数
        days = request.GET.get('days') if request.GET.get('days') else 7
        current = datetime.datetime.now() - datetime.timedelta(days=int(days))
        latest_workitems = self.model_name.objects.filter(
            created__gte=datetime.date(current.year, current.month, current.day))
        return render(request, template_name='{}.html'.format(self.model_name.__name__),
                      context={'datas': latest_workitems})

    def post(self, request, *args, **kwargs):
        fields = [field.name for field in self.model_name._meta.get_fields()]
        # 检测提交的字段的是否在模型字段里
        for key in request.POST.keys():
            if key not in fields:
                print('error keys')
                return render(request, template_name='{}.html'.format(self.model_name.__name__), context={'datas': ''})

        return render(request, template_name='{}.html'.format(self.model_name.__name__), context={'datas': ''})


class WorkItemsView(BaseView):
    model_name = workitems

# # 给整个类函数添加装饰器
# # 新增缓存装饰器
# @method_decorator(cache_page(60 * 15), name='dispatch')
# class WorkItemsView(View):
#     # 默认返回一周的数据
#
#     def get(self, request):
#         # 默认取近7天的数据，如果有值，则按实际情况取数
#         days = request.GET.get('days') if request.GET.get('days') else 7
#         current = datetime.datetime.now() - datetime.timedelta(days=int(days))
#         latest_workitems = workitems.objects.filter(
#             created__gte=datetime.date(current.year, current.month, current.day))
#         return render(request, template_name='workitems.html', context={'latest_workitems': latest_workitems})
#
#     def post(self, request, *args, **kwargs):
#         pass
#
#
# class JszcClass(View):
#
#     def get(self, request):
#         current = datetime.datetime.now() + datetime.timedelta(days=-7)
#         infos = jszc_info.objects.filter(created__gte=datetime.date(current.year, current.month, current.day))
#         return render(request, context={'data': infos})
