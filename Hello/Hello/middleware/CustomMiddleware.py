from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import HttpResponse
import time


# 登陆限制的中间件
class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        # 开发白名单
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.open_urls:
            return redirect(self.login_url + '?next=' + request.get_full_path())
        response = self.get_response(request)
        return response


# 统计请求耗时的中间件
class TimeitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        end = time.time()
        response['CostTime'] = '%s s' % (end - start)
        print(f'花费时间： %ss' % (end - start))
        return response


# 登陆次数限制
class LimitTimes:
    def __init__(self, get_response):
        self.get_response = get_response
        # 访问列表
        self.__visit_list = {}
        # 受限列表
        self.__limited_ip = {}
        # 时间频率
        self.time = 60
        # 访问次数
        self.count = 10

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # 检查访问IP是否在被限制的名单里
        if ip in self.__limited_ip.keys():
            val = time.time() - self.__limited_ip[ip]
            if val < 60:
                return HttpResponse('频繁登陆，请%ss再重试' % (60 - val))
            else:
                print('受限已过')
                self.__limited_ip.pop(ip)
                return self.get_response(request)

        # 检查ip访问列表里的访问次数
        if ip not in self.__visit_list.keys():
            self.__visit_list[ip] = [time.time()]
            return self.get_response(request)
        else:
            # 当前时间
            cur = time.time()
            if len(self.__visit_list.get(ip)) < self.count:
                self.__visit_list[ip].append(cur)
                return self.get_response(request)
            else:
                if cur - self.__visit_list.get(ip)[0] > self.time:
                    self.__visit_list[ip] = self.__visit_list.get(ip)[1:] + [cur]
                    return self.get_response(request)
                else:
                    self.__limited_ip[ip] = cur
                    self.__visit_list[ip] = []
                    return HttpResponse('频繁登陆，请60s再重试')
