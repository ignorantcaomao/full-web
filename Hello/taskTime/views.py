import json
from django.http import JsonResponse
from django.db import connection
from .tasks import get_workitems, get_jszc_info
from django.shortcuts import render
from .db import DbOperate
import pandas as pd


# Create your views here.

def workInfo(request):
    # 查询关联数据
    sql = """select a.author, a.created, a.duration, a.text, b.projectName, b.department, b.taskName, b.projectId from taskTime_workitems a 
                join taskTime_jszc_info b 
                on a.idReadable = b.projectId             
                group by  b.taskName 
                order by a.created desc"""

    cursor = connection.cursor()
    ret = cursor.execute(sql).fetchall()

    print(cursor.execute("select count(*) from taskTime_workitems").fetchone())
    # # 读取数据
    # with DbOperate('../hello.sqlite3') as sqlite_db:
    #     tables = sqlite_db.execute_sql("""
    #     select name from sqlite_master where type='table' order by name;
    #     """)
    #     for item in tables:
    #         print('table: ', item)
    #     datas = []
    #     result = sqlite_db.execute_sql(sql)
    #     for item in result:
    #         datas.append(item)
    # 生成csv文件
    # df = pd.DataFrame(datas)
    # df.to_csv('test.csv', index=True, header=False)

    return JsonResponse(ret, safe=False, json_dumps_params={'ensure_ascii': False})




