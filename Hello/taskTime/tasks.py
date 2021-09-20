from django.db import connection
from celery import shared_task
import requests
import json
import time
from .models import workitems, jszc_info

base_url = "http://space.techstar.com.cn:8081"
headers = {
    'Authorization': 'Bearer perm:ZGV2MQ==.6YeH6ZuGeW91dHJhY2vkv6Hmga8=.b0x04UpA9hUAKBb0Mf9jTT6EoIKJN0',
    'Cookie': 'YTJSESSIONID=node0matmvieuraj5170vpt2qt3fyx27824280.node0'
}


# 获取工时填写信息
@shared_task
def get_workitems():
    '''
    1、先访问数据库获取最新一条数据的记录
    2、从youtrack里按条数获取数据
    3、如果有新数据，插入到数据库中
    4、数据库更新后，通知相关人
    :return:
    '''
    print('start work: get_workitems')
    datas = workitems.objects.all()
    counts = datas.count()
    result = []
    url_template = base_url + "/api/workItems?&fields=created,duration(minutes),author(name),creator(name),date,id,text,type,updated,issue(idReadable,id)" + "&$skip={}&$top=10000"
    # 拼接现在请求的url
    url = url_template.format(counts)

    # 请求工时数据
    with requests.get(url=url, headers=headers, timeout=60) as resp:
        data = json.loads(resp.text)
    # 数据为空，直接放回结果
    if not data:
        print('没有新数据加入')
        return
    # 解析数据
    for item in data:
        temp = {}
        # 工作量（小时）
        temp['duration'] = item.get('duration').get('minutes', 0) / 60
        # 日志填写时间
        timeArray = time.localtime(item.get('created', '') / 1000)
        temp['created'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 填写的日志
        text = item.get('text', '')
        temp['text'] = '' if text is None else text
        # 填写人
        temp['author'] = item.get('author').get('name', '')
        # 唯一id
        temp['id'] = item.get('id', '')
        # 任务id号
        temp['idReadable'] = item.get('issue').get('idReadable', '')

        line = (temp['duration'], temp['created'], temp['text'], temp['author'], temp['id'], temp['idReadable'])
        result.append(str(line))

    # 批量插入去重数据
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """insert ignore into taskTime_workitems (duration, created, text, author, id, idReadable) values %s""" % ','.join(
                    result))
        except Exception as e:
            print('insert failed', e)

    print('现有数据条数', workitems.objects.all().count())
    return len(result)


# 获取技术支持任务信息
# @task
@shared_task
def get_jszc_info():
    print('start work: get_jszc_info')
    counts = jszc_info.objects.all().count()
    result = []
    url_template = base_url + "/api/admin/projects/17CJY003/issues?fields=id,idReadable,summary,created,updated,customFields(id,name,value(fullName,id,minutes,name,presentation,text))" + "&$skip={}&$top=100"
    url = url_template.format(counts)
    print(url)
    with requests.get(url=url, headers=headers, timeout=60) as resp:
        data = json.loads(resp.text)
    if not data:
        return

    for item in data:
        temp = {}
        customFields = item['customFields']
        for obj in customFields:
            if isinstance(obj['value'], str):
                temp[obj['name']] = obj['value']
            elif isinstance(obj['value'], dict):
                temp[obj['name']] = obj['value']['name'] if obj['value'].get('name') else obj[
                    'value'].get(
                    'minutes')
            elif isinstance(obj['value'], list):
                temp[obj['name']] = ';'.join([o['name'] for o in obj['value']])
        temp['id'] = item['id']
        temp['summary'] = item['summary']
        temp['created'] = item['created']
        temp['updated'] = item['updated']
        temp['idReadable'] = item['idReadable']
        result.append(temp)

    # 数据格式化
    data_list = []
    for item in result:
        id = item.get('id')
        projectId = item.get('idReadable')
        taskName = item.get('summary', '')
        projectName = item.get('项目编号及名称', '')
        department = item.get('来源部门', '')
        author = item.get('指派人', '')
        timeArray = time.localtime(item.get('created', '') / 1000)
        created = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        timeArray1 = time.localtime(item.get('updated', '') / 1000)
        updated = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)

        data_list.append(str((id, projectId, taskName, projectName, department, author, created, updated)))

    # 批量插入去重数据
    with connection.cursor() as cursor:
        cursor.execute(
            """insert ignore into taskTime_jszc_info (id, projectId, taskName, projectName, department, author, created, updated) values %s""" % ','.join(
                data_list))

    print('现有数据条数', jszc_info.objects.all().count())
    return len(data_list)

# if __name__ == '__main__':
#     get_workitems()
#     # get_jszc_info()
