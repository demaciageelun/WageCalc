import json
from base64 import decode
from urllib import parse

import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import WageDeptment, WagePosition, WageEmployee


# from functions import insertdata

# Create your views here.
# 从接口获取数据，并写入系统中，包含岗位，部门，人员。
def getdatafrominter(request):
    url = "http://127.0.0.1:36002/mssqlinterface"
    # d = {"table": "T_HR_Department", "param": "id,DepartmentCode,DepartmentName,D_glgs"}
    # d = {"table": "t_hr_post", "param": "id,PostCode,PostName,IfUse"}
    # d = {"table": "t_hr_employee", "param": "Code,Name,DeptID,PostID,_jtrzrq,DimissionDate,EmployeeStatusID,_ygzt"}
    # 从定时任务中获取任务，从接口取数据
    d = json.loads(request.body.decode('utf8'))
    print(d)
    r = requests.get(url=url, data=json.dumps(d))
    retu_data = r.json()
    print(retu_data['data'])
    # 部门，进dept
    if d['table'] == 'T_HR_Department':
        for datas in retu_data['data']:
            WageDeptment.objects.update_or_create(
                defaults={
                    'id': datas[0],
                    'dept_id': datas[1],
                    'dept_name': datas[2],
                    'dept_base': datas[3]
                },
                id=datas[0]
            )
    # 岗位进position
    if d['table'] == 't_hr_post':
        for datas in retu_data['data']:
            WagePosition.objects.update_or_create(
                defaults={
                    'id': datas[0],
                    'posi_id': datas[1],
                    'posi_name': datas[2],
                },
                id=datas[0]
            )
    # emp进员工信息表
    if d['table'] == 't_hr_employee':
        for datas in retu_data['data']:
            print(datas[1])
            try:
                dept = WageDeptment.objects.get(id=datas[2])
            except Exception as e:
                dept = WageDeptment.objects.get(id=23333)
                print(dept)
                print(e)

            try:
                p = WagePosition.objects.get(id=datas[3])
            except Exception as e:
                print(e)
                p = WagePosition.objects.get(id=1)
            WageEmployee.objects.update_or_create(
                defaults={
                    'emp_id': datas[0],
                    'emp_name': datas[1],
                    'emp_dept': dept,
                    'emp_posi': p,
                    'emp_entry_date': datas[4],
                    'emp_leave_date': datas[5],
                    'emp_job_status': datas[6],
                    'emp_job_type': datas[7]
                },
                emp_id=datas[0]
            )
    return HttpResponse({"success": "true"})
