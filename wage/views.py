import json
from base64 import decode
from urllib import parse

import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import WageDeptment, WagePosition, WageEmployee, WageRank, WageJobLevel, WageLeave, WageSkill, WageBase


def ifNull(data):
    if data != "" and data is not None:
        return True
    else:
        return False


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
    r = requests.get(url=url, data=json.dumps(d))
    retu_data = r.json()
    # 部门，进dept
    if d['table'] == 'T_HR_Department':
        for datas in retu_data['data']:
            WageDeptment.objects.update_or_create(
                defaults={
                    'id': datas[0],
                    'dept_id': datas[1],
                    'dept_name': datas[2],
                    'dept_base': datas[3],
                    'dept_short_name': datas[4]
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
            print(datas[0])
            try:
                rank = WageRank.objects.get(id=datas[8])
            except Exception as e:
                print(e)
                rank = WageRank.objects.get(id=34)
            try:
                level = WageJobLevel.objects.get(id=datas[11])
            except Exception as e:
                print(e)
                level = WageJobLevel.objects.get(id=10)
            WageEmployee.objects.update_or_create(
                defaults={
                    'emp_id': datas[0],
                    'emp_name': datas[1],
                    'emp_dept_id': datas[2],
                    'emp_posi_id': datas[3] if ifNull(datas[3]) else 1,
                    'emp_entry_date': datas[4],
                    'emp_leave_date': datas[5],
                    'emp_job_status': datas[6],
                    'emp_job_type': datas[7],
                    'emp_rank_id': datas[8],
                    'emp_in_date': datas[9],
                    'emp_leave_bl_date': datas[10],
                    'emp_job_level_id': datas[11] if ifNull(datas[11]) else 10,
                    'emp_dlidl': datas[12],
                    'emp_pay_type': datas[13],
                    'emp_id_num': datas[14],
                    'emp_source': datas[15],
                    'emp_tel': datas[16],
                    'emp_gsgs': datas[17],
                },
                emp_id=datas[0]
            )

    # V_Ding_Payroll进离职工资表
    if d['table'] == 'V_Ding_Payroll':
        for datas in retu_data['data']:
            try:
                emp = WageEmployee.objects.get(emp_id=datas[0])
            except Exception as e:
                emp = WageEmployee.objects.get(id=125339)
                print(e)
            WageLeave.objects.update_or_create(
                defaults={
                    'leave_emp': emp,
                    'leave_wage_date': datas[1],
                    'leave_base_wage': datas[2],
                    'leave_position_wage': datas[3],
                    'leave_perfor_wage': datas[4],
                    'leave_phone': datas[5],
                    'leave_skill': datas[6],
                    'leave_manage': datas[7],
                    'leave_year': datas[8],
                    'leave_fix': datas[9],
                    'leave_eat': datas[10],
                    'leave_s_base_wage': datas[11],
                    'leave_s_position_wage': datas[12],
                    'leave_perfor_ratio': datas[13],
                    'leave_perfor': datas[14],
                    'leave_subsidy': datas[15],
                    'leave_over': datas[16],
                    'leave_night': datas[17],
                    'leave_rp': datas[18],
                    'leave_reward': datas[19],
                    'leave_temp': datas[20],
                    'leave_test': datas[21],
                    'leave_attend': datas[22],
                    'leave_holiday': datas[23],
                    'leave_pfund': datas[24],
                    'leave_other': datas[25],
                    'leave_compet': datas[26],
                    'leave_total_wage': datas[27],
                    'leave_person_insur': datas[28],
                    'leave_comp_insur': datas[29],
                    'leave_income_tax': datas[30],
                    'leave_we': datas[31],
                    'leave_house': datas[32],
                    'leave_otherplus': datas[33],
                    'leave_othersub': datas[34],
                    'leave_disp': datas[35],
                    'leave_special': datas[36],
                    'leave_actual_wage': datas[37],
                    'leave_remark': datas[38]
                },
                leave_emp=emp,
                leave_wage_date=datas[1]
            )
    return HttpResponse({"success": "true"})


def leavedata(request):
    return render(request, 'wage/leavewage.html')


def searchwage(request):
    username = request.POST.get('username')
    idcode = request.POST.get('idcode')
    searchmonth = request.POST.get('searchmonth')
    # 根据上述信息查询离职薪资，写入leavedatas，到前台访问
    # 如果有值则传递到data.html
    leavedatas = {}
    leaveSql = "select * from wage_leave where leave_wage_period = '%s' and leave_emp_id = '%s'" % (
        searchmonth[:4] + "年" + searchmonth[-2:] + "月", idcode)
    print(leaveSql)
    leaveDataList = WageLeave.objects.raw(leaveSql)
    if len(leaveDataList) > 0:
        for data in leaveDataList:
            leavedatas['leavedatas'] = [{'id': '月份', 'data': searchmonth},
                                        {'id': '基本工资', 'data': data.leave_base_wage},
                                        {'id': '岗位工资', 'data': data.leave_position_wage},
                                        {'id': '绩效工资', 'data': data.leave_perfor_wage},
                                        {'id': '话费补贴', 'data': data.leave_phone},
                                        {'id': '技能津贴', 'data': data.leave_skill},
                                        {'id': '管理津贴', 'data': data.leave_manage},
                                        {'id': '年资津贴', 'data': data.leave_year},
                                        {'id': '固定补贴', 'data': data.leave_fix},
                                        {'id': '就餐补贴', 'data': data.leave_eat},
                                        {'id': '应发基本工资', 'data': data.leave_s_base_wage},
                                        {'id': '应发岗位工资', 'data': data.leave_s_position_wage},
                                        {'id': '综合绩效系数', 'data': data.leave_perfor_ratio},
                                        {'id': '绩效', 'data': data.leave_perfor},
                                        {'id': '补贴合计', 'data': data.leave_subsidy},
                                        {'id': '加班费', 'data': data.leave_over},
                                        {'id': '夜班津贴', 'data': data.leave_night},
                                        {'id': '奖惩', 'data': data.leave_rp},
                                        {'id': '奖金', 'data': data.leave_reward},
                                        {'id': '临时补贴', 'data': data.leave_temp},
                                        {'id': '体检报销费用', 'data': data.leave_test},
                                        {'id': '考勤异常扣款', 'data': data.leave_attend},
                                        {'id': '请假补扣款', 'data': data.leave_holiday},
                                        {'id': '社保公积金补扣', 'data': data.leave_pfund},
                                        {'id': '其他补扣款', 'data': data.leave_other},
                                        {'id': '竞业补偿金', 'data': data.leave_compet},
                                        {'id': '应发合计', 'data': data.leave_total_wage},
                                        {'id': '社保公积金个人承担', 'data': data.leave_person_insur},
                                        {'id': '社保公积金公司承担', 'data': data.leave_comp_insur},
                                        {'id': '代扣个税', 'data': data.leave_income_tax},
                                        {'id': '水电费', 'data': data.leave_we},
                                        {'id': '房租费', 'data': data.leave_house},
                                        {'id': '其他加', 'data': data.leave_otherplus},
                                        {'id': '其他减', 'data': data.leave_othersub},
                                        {'id': '一次性补偿金', 'data': data.leave_disp},
                                        {'id': '专项附加扣除合计', 'data': data.leave_special},
                                        {'id': '实发工资', 'data': data.leave_actual_wage},
                                        {'id': '薪资备注', 'data': data.leave_remark},
                                        ]
        return render(request, 'wage/data.html', leavedatas)
    else:
        # 否则无值则传递到leavewage.html并且返回一个弹窗，未查询到值，请重试
        leavedatas['messages'] = 1
        return render(request, 'wage/leavewage.html', leavedatas)


