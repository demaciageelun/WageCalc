import openpyxl
from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db.models import F
from django.http import JsonResponse, FileResponse
from simpleui.admin import AjaxAdmin
from .models import WageDeptment, WagePosition, WageEmployee, WageExpense, WageExpenseInto, WagePerformanceInto, \
    WageFixWage, WageMonth, WagePeriod, WageFixLog, WageBase, WageSkill, WageManage
import datetime as firstdate
from .functions import monthcalc, verifyIdName

period_list = WagePeriod.objects.values('id', 'period_name')
global options_list
options_list = []
for data in period_list:
    temp = {'key': data['id'], 'label': data['period_name']}
    options_list.append(temp)


# Register your models here.
# 周期表
class WagePeriodAdmin(AjaxAdmin):
    list_display = ['period_name']
    search_fields = ['period_name']


# 部门表
class WageDeptmentAdmin(AjaxAdmin):
    list_display = ['dept_id', 'dept_name', 'dept_short_name', 'dept_base']
    search_fields = ['dept_id', 'dept_name', 'dept_base', 'dept_short_name']
    list_filter = ['dept_base', 'dept_short_name']


# 岗位表
class WagePositionAdmin(AjaxAdmin):
    list_display = ['posi_id', 'posi_name']
    search_fields = ['posi_id', 'posi_name']
    # list_filter = ['posi_id', 'posi_name']


# 员工表
class WageEmployeeAdmin(AjaxAdmin):
    list_display = ['emp_id', 'emp_name', 'emp_dept', 'emp_posi', 'emp_entry_date', 'emp_in_date', 'emp_leave_date',
                    'emp_leave_bl_date', 'emp_job_status',
                    'emp_job_type', 'emp_rank', 'glgs']
    search_fields = ['emp_id', 'emp_name']
    list_filter = ['emp_dept__dept_short_name', 'emp_posi__posi_name', 'emp_job_type', 'emp_job_status', 'emp_rank',
                   'emp_dept__dept_base']
    actions = ['download']

    def glgs(self, obj):
        return obj.emp_dept.dept_base

    glgs.short_description = '管理归属'

    def get_job_status(self, num):
        numbers = {
            1: "在职",
            2: "离职",
            99: "黑名单",
        }
        return numbers.get(num, None)

    def download(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        row1 = ['工号', '姓名', '部门', '岗位', '集团入职日期', '入职日期', '离职结薪日期', '离职办理日期', '在职状态', '在职类型', '合同归属', '管理归属']
        ws.append(row1)
        for datas in queryset:
            row2 = [
                str(datas.emp_id) if str(datas.emp_id) != "None" else "",  # 工号
                str(datas.emp_name) if str(datas.emp_name) != "None" else "",  # 姓名
                str(datas.emp_dept) if str(datas.emp_dept) != "None" else "",  # 部门
                str(datas.emp_posi) if str(datas.emp_posi) != "None" else "",  # 岗位
                str(datas.emp_entry_date) if str(datas.emp_entry_date) != "None" else "",  # 集团入职日期
                str(datas.emp_in_date) if str(datas.emp_in_date) != "None" else "",  # 入职日期
                str(datas.emp_leave_date) if str(datas.emp_leave_date) != "None" else "",  # 离职结薪日期
                str(datas.emp_leave_bl_date) if str(datas.emp_leave_bl_date) != "None" else "",  # 离职办理日期
                self.get_job_status(datas.emp_job_status),  # 在职状态
                str(datas.emp_job_type) if str(datas.emp_job_type) != "None" else "",  # 在职类型
                str(datas.emp_rank) if str(datas.emp_rank) != "None" else "",  # 合同归属
                str(datas.emp_dept.dept_base) if str(datas.emp_dept.dept_base) != "None" else "",  # 管理归属
            ]
            ws.append(row2)
        wb.save('static/emp.xlsx')
        #     下载
        file = open('static/emp.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="emp.xlsx"'
        return response

        # 显示的文本，与django admin一致

    download.short_description = '下载数据'
    # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    download.type = 'success'


# 费用项目表
class WageExpenseAdmin(AjaxAdmin):
    list_display = ['expense_name']
    search_fields = ['expense_name']


# 费用项目引入表
class WageExpenseIntoAdmin(AjaxAdmin):
    list_display = ['into_emp', 'dept', 'position', 'into_periods', 'into_expense', 'into_reason',
                    'into_calc_elem_1',
                    'into_calc_elem_2',
                    'into_calc_elem_other', 'into_money', 'into_effecte_date', 'into_expir_date']
    actions = ['upload_file', 'download_templates']
    list_filter = ['into_emp__emp_dept__dept_short_name', 'into_emp__emp_posi', 'into_periods', 'into_expense']
    raw_id_fields = ['into_emp', 'into_expense']
    search_fields = ['into_emp__emp_id', 'into_emp__emp_name']

    def dept(self, obj):
        return obj.into_emp.emp_dept.dept_short_name

    dept.short_description = '部门'

    def position(self, obj):
        return obj.into_emp.emp_posi

    position.short_description = '岗位'

    def download_templates(self, request, queryset):
        file = open('static/templates/expense.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="expense.xlsx"'
        return response

    download_templates.short_description = '下载模板'
    download_templates.type = 'warning'
    download_templates.icon = 'el-icon-paperclip'
    download_templates.acts_on_all = True

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload = request.FILES['upload']
        # 将上传的文件保存到static中
        print(str(firstdate.date.today()))
        with open('static/expense/' + str(firstdate.date.today()) + upload.name, 'wb') as f:
            for line in upload.chunks():
                f.write(line)
        f.close()
        workbook = openpyxl.load_workbook('static/expense/' + str(firstdate.date.today()) + upload.name)
        # 可以使用workbook对象的sheetnames属性获取到excel文件中哪些表有数据
        table = workbook.active
        rows = table.max_row
        cols = table.max_column
        # 获取标题栏数据
        head_data = []
        for datas in range(cols):
            head_data.append(table.cell(1, datas + 1).value)
        if '工号' in head_data and '姓名' in head_data and '周期' in head_data and '成本归属' in head_data and '公司' in head_data and '项目' in head_data and '原因' in head_data and '计算要素1' in head_data and '计算要素2' in head_data and '其他计算要素' in head_data and '金额' in head_data and '生效日期' in head_data and '失效日期' in head_data:
            # 创建一个字符串来手机所有错误数据
            error_str = ''
            for datas in range(rows):
                if datas > 0:
                    emp_id = table.cell(datas + 1, head_data.index('工号') + 1).value
                    if type(emp_id) == int:
                        emp_name = table.cell(datas + 1, head_data.index('姓名') + 1).value
                        sql_name = WageEmployee.objects.raw("select id,emp_name from wage_employee where emp_id = '" + str(emp_id) + "'")
                        if len(sql_name) > 0 and str(sql_name[0]) == emp_name:
                            expense_name = table.cell(datas + 1, head_data.index('项目') + 1).value
                            period_name = table.cell(datas + 1, head_data.index('周期') + 1).value
                            into_emp_id = WageEmployee.objects.filter(emp_id=int(emp_id)).values('id')[0]['id']
                            into_expense_id = WageExpense.objects.filter(expense_name=expense_name).values('id')[0]['id']
                            WageExpenseInto.objects.update_or_create(
                                defaults={
                                    'into_emp_id': into_emp_id,
                                    'into_periods': period_name,
                                    'into_expense_id': into_expense_id,
                                    'into_reason': table.cell(datas + 1, head_data.index('原因') + 1).value,
                                    'into_calc_elem_1': table.cell(datas + 1, head_data.index('计算要素1') + 1).value,
                                    'into_calc_elem_2': table.cell(datas + 1, head_data.index('计算要素2') + 1).value,
                                    'into_calc_elem_other': table.cell(datas + 1, head_data.index('其他计算要素') + 1).value,
                                    'into_money': table.cell(datas + 1, head_data.index('金额') + 1).value,
                                    'into_effecte_date': table.cell(datas + 1, head_data.index('生效日期') + 1).value,
                                    'into_expir_date': table.cell(datas + 1, head_data.index('失效日期') + 1).value,

                                },
                                into_emp_id=into_emp_id,
                                into_periods=period_name,
                                into_money=table.cell(datas + 1, head_data.index('金额') + 1).value,
                                into_expense_id=into_expense_id,
                                into_reason=table.cell(datas + 1, head_data.index('原因') + 1).value,
                                into_calc_elem_1=table.cell(datas + 1, head_data.index('计算要素1') + 1).value,
                                into_calc_elem_2=table.cell(datas + 1, head_data.index('计算要素2') + 1).value,
                                into_calc_elem_other=table.cell(datas + 1, head_data.index('其他计算要素') + 1).value,
                            )
                        else:
                            error_str += "第" + str(datas) + "行工号和姓名不匹配，请修正。"
                            continue
                    else:
                        error_str += "第" + str(datas) + "行有空字符串，请整行删除。"
                        continue
            # 如果错误
            if error_str == "":
                status = 'success'
                msg = '上传成功！'
            else:
                status = 'error'
                msg = error_str
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })
        else:
            status = 'error'
            msg = '列名错误，请使用下载的文档进行导入！'
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })

    upload_file.short_description = '文件上传'
    upload_file.type = 'success'
    upload_file.icon = 'el-icon-upload'
    upload_file.enable = True

    upload_file.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': '文件'
        }]
    }


# 绩效引入表
class WagePerformanceIntoAdmin(AjaxAdmin):
    list_display = ['perfor_emp', 'dept', 'perfor_center', 'position', 'perfor_periods', 'perfor_period_type',
                    'perfor_costs_attach', 'perfor_proof_ip', 'perfor_proof_dp', 'perfor_proof_cp', 'perfor_score_ip', 'perfor_score_dp', 'perfor_score_cp',
                    'perfor_ratio_ip', 'perfor_ratio_dp', 'perfor_ratio_cp', 'perfor_ratio_tp', 'perfor_result']
    raw_id_fields = ['perfor_emp']
    list_filter = ['perfor_emp__emp_dept__dept_short_name', 'perfor_emp__emp_posi', 'perfor_periods', 'perfor_costs_attach', 'perfor_center']
    actions = ['upload_file', 'download_templates']
    search_fields = ['perfor_emp__emp_id', 'perfor_emp__emp_name']

    def dept(self, obj):
        return obj.perfor_emp.emp_dept.dept_short_name

    dept.short_description = '部门'

    def position(self, obj):
        return obj.perfor_emp.emp_posi

    position.short_description = '岗位'

    def download_templates(self, request, queryset):
        file = open('static/templates/performance.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="performance.xlsx"'
        return response

    download_templates.short_description = '下载模板'
    download_templates.type = 'warning'
    download_templates.icon = 'el-icon-paperclip'
    download_templates.acts_on_all = True

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload = request.FILES['upload']
        # 将上传的文件保存到static中
        with open('static/performance/' + str(firstdate.date.today()) + upload.name, 'wb') as f:
            for line in upload.chunks():
                f.write(line)
        f.close()
        workbook = openpyxl.load_workbook('static/performance/' + str(firstdate.date.today()) + upload.name)
        # 可以使用workbook对象的sheetnames属性获取到excel文件中哪些表有数据
        table = workbook.active
        rows = table.max_row
        cols = table.max_column
        # 获取标题栏数据
        head_data = []
        for datas in range(cols):
            head_data.append(table.cell(1, datas + 1).value)
        # 首先判断列名是否都正确，正确则进入循环，错误就返回报错
        if '工号' in head_data and '姓名' in head_data and '中心别' in head_data and '周期名称' in head_data and '周期类型' in head_data and '成本归属' in head_data and '公司' in head_data and '个人绩效占比' in head_data and '部门绩效占比' in head_data and '公司绩效占比' in head_data and '个人绩效分数' in head_data and '部门绩效分数' in head_data and '公司绩效分数' in head_data and '个人绩效系数' in head_data and '部门绩效系数' in head_data and '公司绩效系数' in head_data:
            # 创建一个字符串来手机所有错误数据
            error_str = ''
            for datas in range(rows):
                if datas > 0:
                    emp_id = table.cell(datas + 1, head_data.index('工号') + 1).value
                    if type(emp_id) == int:
                        perfor_emp_id = WageEmployee.objects.filter(emp_id=int(emp_id)).values('id')[0]['id']
                        sql_name = WageEmployee.objects.raw("select id,emp_name from wage_employee where emp_id = '" + str(emp_id) + "'")
                        perfor_name = table.cell(datas + 1, head_data.index('姓名') + 1).value
                        if len(sql_name) > 0 and str(sql_name[0]) == perfor_name:
                            perfor_center = table.cell(datas + 1, head_data.index('中心别') + 1).value if table.cell(datas + 1, head_data.index('中心别') + 1).value is not None else ""
                            period_name = table.cell(datas + 1, head_data.index('周期名称') + 1).value
                            # 判断是否为日期格式（datetime），不是的话报错，是的话继续循环
                            if type(period_name) == int:
                                error_str += "第" + str(datas) + "行日期格式错误，请以文本格式，不要使用自定义格式。"
                                continue
                            else:
                                perfor_period_type = table.cell(datas + 1, head_data.index('周期类型') + 1).value
                                perfor_costs_attach = table.cell(datas + 1, head_data.index('成本归属') + 1).value
                                perfor_proof_ip = table.cell(datas + 1, head_data.index('个人绩效占比') + 1).value if table.cell(datas + 1, head_data.index('个人绩效占比') + 1).value is not None else 0
                                perfor_proof_dp = table.cell(datas + 1, head_data.index('部门绩效占比') + 1).value if table.cell(datas + 1, head_data.index('部门绩效占比') + 1).value is not None else 0
                                perfor_proof_cp = table.cell(datas + 1, head_data.index('公司绩效占比') + 1).value if table.cell(datas + 1, head_data.index('公司绩效占比') + 1).value is not None else 0
                                perfor_score_ip = table.cell(datas + 1, head_data.index('个人绩效分数') + 1).value if table.cell(datas + 1, head_data.index('个人绩效分数') + 1).value is not None else 0
                                perfor_score_dp = table.cell(datas + 1, head_data.index('部门绩效分数') + 1).value if table.cell(datas + 1, head_data.index('部门绩效分数') + 1).value is not None else 0
                                perfor_score_cp = table.cell(datas + 1, head_data.index('公司绩效分数') + 1).value if table.cell(datas + 1, head_data.index('公司绩效分数') + 1).value is not None else 0
                                perfor_ratio_ip = table.cell(datas + 1, head_data.index('个人绩效系数') + 1).value if table.cell(datas + 1, head_data.index('个人绩效系数') + 1).value is not None else 0
                                perfor_ratio_dp = table.cell(datas + 1, head_data.index('部门绩效系数') + 1).value if table.cell(datas + 1, head_data.index('部门绩效系数') + 1).value is not None else 0
                                perfor_ratio_cp = table.cell(datas + 1, head_data.index('公司绩效系数') + 1).value if table.cell(datas + 1, head_data.index('公司绩效系数') + 1).value is not None else 0
                                # perfor_ratio_tp=table.cell(datas + 1, head_data.index('综合绩效系数') + 1).value
                                WagePerformanceInto.objects.update_or_create(
                                    defaults={
                                        'perfor_emp_id': perfor_emp_id,
                                        'perfor_center': perfor_center,
                                        'perfor_periods': period_name,
                                        'perfor_period_type': perfor_period_type,
                                        'perfor_costs_attach': perfor_costs_attach,
                                        'perfor_proof_ip': float(perfor_proof_ip),
                                        'perfor_proof_dp': float(perfor_proof_dp),
                                        'perfor_proof_cp': float(perfor_proof_cp),
                                        'perfor_score_ip': float(perfor_score_ip),
                                        'perfor_score_dp': float(perfor_score_dp),
                                        'perfor_score_cp': float(perfor_score_cp),
                                        'perfor_ratio_ip': float(perfor_ratio_ip),
                                        'perfor_ratio_dp': float(perfor_ratio_dp),
                                        'perfor_ratio_cp': float(perfor_ratio_cp),
                                        'perfor_ratio_tp': float(perfor_proof_ip) * float(perfor_ratio_ip) + float(
                                            perfor_proof_dp) * float(perfor_ratio_dp) + float(perfor_proof_cp) * float(
                                            perfor_ratio_cp)

                                    },
                                    perfor_emp_id=perfor_emp_id,
                                    perfor_periods=period_name,
                                )
                        else:
                            error_str += "第" + str(datas) + "行工号和姓名不匹配，请修正。"
                            continue
                    else:
                        error_str += "第" + str(datas) + "行有空字符串，请整行删除。"
                        continue
            # 如果错误
            if error_str == "":
                status = 'success'
                msg = '上传成功！'
            else:
                status = 'error'
                msg = error_str
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })
        else:
            status = 'error'
            msg = '列名错误，请使用下载的文档进行导入！'
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })

    upload_file.short_description = '文件上传'
    upload_file.type = 'success'
    upload_file.icon = 'el-icon-upload'
    upload_file.enable = True

    upload_file.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': '文件'
        }]
    }


# 固定工资引入表
class WageFixWageAdmin(AjaxAdmin):
    list_display = ['fix_emp', 'fix_emp_ids', 'dept', 'position', 'fix_begin_date', 'fix_work_pro', 'fix_wage_type',
                    'fix_skill_level',
                    'fix_manage_level', 'fix_wage_stand', 'fix_base_wage', 'fix_post_wage', 'fix_perfor_wage',
                    'fix_skill_wage', 'fix_manage_wage', 'fix_phone_subsidy', 'fix_change_reason', 'fix_resource']
    raw_id_fields = ['fix_emp']
    actions = ['upload_file', 'download_templates']
    search_fields = ['fix_emp__emp_id', 'fix_emp__emp_name']
    list_filter = ['fix_emp__emp_dept__dept_short_name', 'fix_emp__emp_posi']

    def fix_emp_ids(self, obj):
        return obj.fix_emp.emp_id

    fix_emp_ids.short_description = '工号'

    def dept(self, obj):
        return obj.fix_emp.emp_dept.dept_short_name

    dept.short_description = '部门'

    def position(self, obj):
        return obj.fix_emp.emp_posi

    position.short_description = '岗位'

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload = request.FILES['upload']
        # 将上传的文件保存到static中
        with open('static/fixwage/' + str(firstdate.date.today()) + upload.name, 'wb') as f:
            for line in upload.chunks():
                f.write(line)
        f.close()
        # try:
        workbook = openpyxl.load_workbook('static/fixwage/' + str(firstdate.date.today()) + upload.name)
        # 可以使用workbook对象的sheetnames属性获取到excel文件中哪些表有数据
        table = workbook.active
        rows = table.max_row
        cols = table.max_column
        # 获取标题栏数据
        head_data = []
        for datas in range(cols):
            head_data.append(table.cell(1, datas + 1).value)
        # 首先判断列名是否都正确，正确则进入循环，错误就返回报错
        if '工号' in head_data and '姓名' in head_data and '类型' in head_data and '起始日期' in head_data and '公司' in head_data and '部门简称' in head_data and '岗位名称' in head_data and '工序' in head_data and '薪酬类型' in head_data and '技能等级' in head_data and '管理等级' in head_data and '标准工资' in head_data and '基本工资' in head_data and '岗位工资' in head_data and '绩效工资' in head_data and '技能津贴' in head_data and '管理津贴' in head_data and '话费补贴' in head_data and '变更原因' in head_data:
            # 创建一个字符串来手机所有错误数据
            error_str = ''
            # 列名都正确，开始遍历每行数据
            for datas in range(rows):
                # 从第二行开始写入数据库
                if datas > 0:
                    emp_id = table.cell(datas + 1, head_data.index('工号') + 1).value
                    # 先通过emp_id判断是否这行真有数据，没有的话则是空白格式，有的话就对比工号和姓名。
                    if type(emp_id) == int:
                        # 通过获取的工号去数据库中查找对应的姓名
                        sql_name = WageEmployee.objects.raw("select id,emp_name from wage_employee where emp_id = '" + str(emp_id) + "'")
                        emp_name = table.cell(datas + 1, head_data.index('姓名') + 1).value
                        fix_position = table.cell(datas + 1, head_data.index('岗位名称') + 1).value
                        fix_company = table.cell(datas + 1, head_data.index('公司') + 1).value
                        # 如果此emp_id且有对应的emp_name则继续写入，没有的话则跳过当条循环，记录错误日志。继续下一条。
                        if len(sql_name) > 0 and str(sql_name[0]) == emp_name:
                            emp_id = WageEmployee.objects.filter(emp_id=int(emp_id)).values('id')[0]['id']
                            change_type = table.cell(datas + 1, head_data.index('类型') + 1).value
                            begin_date = table.cell(datas + 1, head_data.index('起始日期') + 1).value
                            # 判断是否为日期格式（datetime），不是的话报错，是的话继续循环
                            if type(begin_date) == int:
                                error_str += "第" + str(datas) + "行日期格式错误，请以文本格式或日期格式，不要使用自定义格式。"
                                continue
                            else:
                                work_pro = table.cell(datas + 1, head_data.index('工序') + 1).value if table.cell(datas + 1, head_data.index('工序') + 1).value is not None else ""
                                wage_type = table.cell(datas + 1, head_data.index('薪酬类型') + 1).value if table.cell(datas + 1, head_data.index('薪酬类型') + 1).value is not None else ""
                                skill_level = table.cell(datas + 1, head_data.index('技能等级') + 1).value if table.cell(datas + 1, head_data.index('技能等级') + 1).value is not None else ""
                                manage_level = table.cell(datas + 1, head_data.index('管理等级') + 1).value if table.cell(datas + 1, head_data.index('管理等级') + 1).value is not None else ""
                                # 因技能等级、管理等级只有计时制有，系统添加自动识别功能，如责任制上传了技能等级或管理等级，报错
                                if wage_type == '责任制' and (skill_level != "" or manage_level != ""):
                                    error_str += "第" + str(datas) + "行错误，责任制员工不能有技能等级和管理等级"
                                    continue
                                else:
                                    wage_stand = table.cell(datas + 1, head_data.index('标准工资') + 1).value if table.cell(datas + 1, head_data.index('标准工资') + 1).value is not None else 0
                                    base_wage = table.cell(datas + 1, head_data.index('基本工资') + 1).value if table.cell(datas + 1, head_data.index('基本工资') + 1).value is not None else 0
                                    post_wage = table.cell(datas + 1, head_data.index('岗位工资') + 1).value if table.cell(datas + 1, head_data.index('岗位工资') + 1).value is not None else 0
                                    perfor_wage = table.cell(datas + 1, head_data.index('绩效工资') + 1).value if table.cell(datas + 1, head_data.index('绩效工资') + 1).value is not None else 0
                                    # 如果是计时制的，就获取技能津贴和管理津贴
                                    if wage_type == '计时制':
                                        if manage_level != "":
                                            # 管理津贴
                                            if "班长" in fix_position:
                                                manage_wage = WageManage.objects.get(manage_position='班长', manage_grade=manage_level)
                                                manage_wages = manage_wage.manage_allowance
                                            elif "主管" in fix_position:
                                                manage_wage = WageManage.objects.get(manage_position='主管', manage_grade=manage_level)
                                                manage_wages = manage_wage.manage_allowance
                                            else:
                                                manage_wages = 0
                                        else:
                                            manage_wages = 0
                                        # 技能津贴 根据基地和技能等级查找技能津贴
                                        if skill_level != "":
                                            skill_wage = WageSkill.objects.get(skill_grade=skill_level, skill_local=fix_company)
                                            skill_wages = skill_wage.skill_allowance
                                        else:
                                            skill_wages = 0
                                    else:
                                        manage_wages = 0
                                        skill_wages = 0

                                    phone_subsidy = table.cell(datas + 1, head_data.index('话费补贴') + 1).value if table.cell(datas + 1, head_data.index('话费补贴') + 1).value is not None else 0
                                    change_reason = table.cell(datas + 1, head_data.index('变更原因') + 1).value
                                    WageFixWage.objects.update_or_create(
                                        defaults={
                                            'fix_emp_id': emp_id,
                                            'fix_change_type': change_type,
                                            'fix_begin_date': begin_date,
                                            'fix_work_pro': work_pro,
                                            'fix_wage_type': wage_type,
                                            'fix_skill_level': skill_level,
                                            'fix_manage_level': manage_level,
                                            'fix_wage_stand': float(wage_stand),
                                            'fix_base_wage': float(base_wage),
                                            'fix_post_wage': float(post_wage),
                                            'fix_perfor_wage': float(perfor_wage),
                                            'fix_skill_wage': float(skill_wages),
                                            'fix_manage_wage': float(manage_wages),
                                            'fix_phone_subsidy': float(phone_subsidy),
                                            'fix_change_reason': change_reason,
                                            'fix_resource': 'excel导入',
                                        },
                                        fix_emp_id=emp_id,
                                    )
                                    WageFixLog.objects.create(log_creater=str(request.user),
                                                              log_time=firstdate.datetime.now(),
                                                              log_emp_id=emp_id,
                                                              log_change_type=change_type,
                                                              log_begin_date=begin_date,
                                                              log_work_pro=work_pro,
                                                              log_wage_type=wage_type,
                                                              log_skill_level=skill_level,
                                                              log_manage_level=manage_level,
                                                              log_wage_stand=wage_stand,
                                                              log_base_wage=base_wage,
                                                              log_post_wage=post_wage,
                                                              log_perfor_wage=perfor_wage,
                                                              log_skill_wage=skill_wages,
                                                              log_manage_wage=manage_wages,
                                                              log_phone_subsidy=phone_subsidy,
                                                              log_change_reason=change_reason,
                                                              log_resource='excel导入',
                                                              )
                        else:
                            error_str += "第" + str(datas) + "行工号和姓名不匹配，请修正。"
                            continue
                    else:
                        print('该行为空')
                        error_str += "第" + str(datas) + "行有空字符串，请整行删除。"
                        continue
            # 如果错误
            if error_str == "":
                status = 'success'
                msg = '上传成功！'
            else:
                status = 'error'
                msg = error_str
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })
        # 列名错误，报错
        else:
            status = 'error'
            msg = '列名错误，请使用下载的文档进行导入！'
            return JsonResponse(data={
                'status': status,
                'msg': str(msg)
            })

    upload_file.short_description = '文件上传'
    upload_file.type = 'success'
    upload_file.icon = 'el-icon-upload'
    upload_file.enable = True

    upload_file.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': '文件'
        }]
    }

    def download_templates(self, request, queryset):
        file = open('static/templates/fixwage.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="fixwage.xlsx"'
        return response

    download_templates.short_description = '下载模板'
    download_templates.type = 'warning'
    download_templates.icon = 'el-icon-paperclip'
    download_templates.acts_on_all = True


# 月度工资汇总表
class WageMonthAdmin(AjaxAdmin):
    list_display = ['mon_emp', 'dept', 'position', 'mon_periods', 'mon_wage_way', 'mon_standard_wage', 'mon_base_wage',
                    'mon_post_wage', 'mon_perfor_wage', 'mon_manage_wage', 'mon_seniority_wage', 'mon_post_subsidy',
                    'mon_skill_wage', 'mon_perfor_merit', 'mon_reward_punish', 'mon_other_deduc', 'mon_si_af_deduc',
                    'mon_reward', 'mon_phyexam', 'mon_water_elect', 'mon_rent', 'mon_quart_bonus', 'mon_annual_bonus',
                    'mon_sale_com', 'mon_temp_wage', 'mon_laber_cost', 'mon_income_tax', 'mon_non_compet',
                    'mon_severance']
    raw_id_fields = ['mon_emp']
    search_fields = ['mon_emp__emp_id', 'mon_emp__emp_name']
    list_filter = ['mon_periods', 'mon_emp__emp_dept__dept_short_name', 'mon_emp__emp_posi']
    actions = ['layer_input', 'download']
    list_per_page = 10

    def dept(self, obj):
        return obj.mon_emp.emp_dept.dept_short_name

    dept.short_description = '部门'

    def position(self, obj):
        return obj.mon_emp.emp_posi

    position.short_description = '岗位'

    def layer_input(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据
        post = request.POST
        print(post.get('type'))
        monthcalc.calc(post.get('type'))
        # GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'
        # # 将前端获取的时间转换为年月日时间
        # local_data = str(datetime.strptime(post.get('date'), GMT_FORMAT))[:10]
        # WageMonth.objects.create(mon_emp_id=104482,mon_date=local_data)
        # 根据前端获取到的日期，取费用引入表、绩效表当月数据，结合固定工资表，整合为月度工资汇总表
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割

        if not post.get('type'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })
        else:
            return JsonResponse(data={
                'status': 'success',
                'msg': '处理成功！'
            })

    layer_input.short_description = '生成报表'
    layer_input.type = 'success'
    layer_input.icon = 'el-icon-s-promotion'

    # 指定一个输入参数，应该是一个数组

    # 指定为弹出层，这个参数最关键
    layer_input.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '请选择',
        # 提示信息
        'tips': '请选择需要生成薪酬的周期',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [{
            'type': 'month',
            'key': 'type',
            'label': '周期',
            'width': '200px',
            # size对应elementui的size，取值为：medium / small / mini
            'size': 'small',
            # value字段可以指定默认值
            # 'value': '0',
            # 'options': list(WagePeriod.objects.annotate(key=F('id'), label=F('period_name')).values('key', 'label'))
        }, ]
    }

    def download(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        row1 = ['工号', '姓名', '集团入职日期', '入职日期', '离职结薪日期', '离职办理日期', '公司', '部门', '岗位', '计薪周期', '计薪方式', '标准工资', '基本工资', '岗位工资', '绩效工资', '管理津贴', '年资津贴', '岗位补贴',
                '技能津贴', '绩效系数', '奖惩', '其他补扣款', '社保公积金补扣款', '奖金/津贴', '体检费报销', '代收水电费', '代收房租', '季度奖金', '年度奖金', '销售提成',
                '临时补贴', '劳务费', '个人所得税', '竞业限制补偿金', '离职补偿金'
                ]
        ws.append(row1)
        for datas in queryset:
            row2 = [
                str(datas.mon_emp.emp_id) if str(datas.mon_emp.emp_id) != "None" else "",  # 工号
                str(datas.mon_emp.emp_name) if str(datas.mon_emp.emp_name) != "None" else "",  # 姓名
                str(datas.mon_emp.emp_entry_date) if str(datas.mon_emp.emp_entry_date) != "None" else "",  # 集团入职日期
                str(datas.mon_emp.emp_in_date) if str(datas.mon_emp.emp_in_date) != "None" else "",  # 入职日期
                str(datas.mon_emp.emp_leave_date) if str(datas.mon_emp.emp_leave_date) != "None" else "",  # 离职结薪日期
                str(datas.mon_emp.emp_leave_bl_date) if str(datas.mon_emp.emp_leave_bl_date) != "None" else "",  # 离职办理日期
                str(datas.mon_emp.emp_dept.dept_base) if str(datas.mon_emp.emp_dept.dept_base) != "None" else "",  # 公司
                str(datas.mon_emp.emp_dept.dept_name) if str(datas.mon_emp.emp_dept.dept_name) != "None" else "",  # 部门
                str(datas.mon_emp.emp_posi.posi_name) if str(datas.mon_emp.emp_posi.posi_name) != "None" else "",  # 岗位
                str(datas.mon_periods) if str(datas.mon_periods) != "None" else "",  # 计薪周期
                str(datas.mon_wage_way) if str(datas.mon_wage_way) != "None" else "",  # 计薪方式
                str(datas.mon_standard_wage) if str(datas.mon_standard_wage) != "None" else 0,  # 标准工资
                str(datas.mon_base_wage) if str(datas.mon_base_wage) != "None" else 0,  # 基本工资
                str(datas.mon_post_wage) if str(datas.mon_post_wage) != "None" else 0,  # 岗位工资
                str(datas.mon_perfor_wage) if str(datas.mon_perfor_wage) != "None" else 0,  # 绩效工资
                str(datas.mon_manage_wage) if str(datas.mon_manage_wage) != "None" else 0,  # 管理津贴
                str(datas.mon_seniority_wage) if str(datas.mon_seniority_wage) != "None" else 0,  # 年资津贴
                str(datas.mon_post_subsidy) if str(datas.mon_post_subsidy) != "None" else 0,  # 岗位补贴
                str(datas.mon_skill_wage) if str(datas.mon_skill_wage) != "None" else 0,  # 技能津贴
                str(datas.mon_perfor_merit) if str(datas.mon_perfor_merit) != "None" else "",  # 绩效系数
                str(datas.mon_reward_punish) if str(datas.mon_reward_punish) != "None" else 0,  # 奖惩
                str(datas.mon_other_deduc) if str(datas.mon_other_deduc) != "None" else 0,  # 其他补扣款
                str(datas.mon_si_af_deduc) if str(datas.mon_si_af_deduc) != "None" else 0,  # 社保公积金补扣款
                str(datas.mon_reward) if str(datas.mon_reward) != "None" else 0,  # 奖金/津贴
                str(datas.mon_phyexam) if str(datas.mon_phyexam) != "None" else 0,  # 体检费报销
                str(datas.mon_water_elect) if str(datas.mon_water_elect) != "None" else 0,  # 代收水电费
                str(datas.mon_rent) if str(datas.mon_rent) != "None" else 0,  # 代收房租
                str(datas.mon_quart_bonus) if str(datas.mon_quart_bonus) != "None" else 0,  # 季度奖金
                str(datas.mon_annual_bonus) if str(datas.mon_annual_bonus) != "None" else 0,  # 年度奖金
                str(datas.mon_sale_com) if str(datas.mon_sale_com) != "None" else 0,  # 销售提成
                str(datas.mon_temp_wage) if str(datas.mon_temp_wage) != "None" else 0,  # 临时补贴
                str(datas.mon_laber_cost) if str(datas.mon_laber_cost) != "None" else 0,  # 劳务费
                str(datas.mon_income_tax) if str(datas.mon_income_tax) != "None" else 0,  # 个人所得税
                str(datas.mon_non_compet) if str(datas.mon_non_compet) != "None" else 0,  # 竞业限制补偿金
                str(datas.mon_severance) if str(datas.mon_severance) != "None" else 0,  # 离职补偿金
            ]
            ws.append(row2)
        wb.save('static/data.xlsx')
        #     下载
        file = open('static/data.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="record.xlsx"'
        return response

        # 显示的文本，与django admin一致

    download.short_description = '下载数据'
    # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    download.type = 'success'
    download.confirm = '是否确定下载此报表？'

    # 给按钮追加自定义的颜色
    # custom_button.style = 'color:black;'


# 基地表
class WageBaseAdmin(AjaxAdmin):
    list_display = ['base_name']
    search_fields = ['base_name']


# 技能津贴表
class WageSkillAdmin(AjaxAdmin):
    list_display = ['skill_local', 'skill_grade', 'skill_allowance']
    list_filter = ['skill_local', 'skill_grade']


# 管理津贴表
class WageManageAdmin(AjaxAdmin):
    list_display = ['manage_position', 'manage_grade', 'manage_allowance']
    list_filter = ['manage_position', 'manage_grade']


admin.site.site_header = '薪酬系统'
admin.site.site_title = '薪酬系统'
admin.site.index_title = '欢迎使用薪酬系统'

admin.site.register(WageDeptment, WageDeptmentAdmin)
admin.site.register(WagePosition, WagePositionAdmin)
admin.site.register(WageEmployee, WageEmployeeAdmin)
admin.site.register(WageExpense, WageExpenseAdmin)
admin.site.register(WageExpenseInto, WageExpenseIntoAdmin)
admin.site.register(WagePerformanceInto, WagePerformanceIntoAdmin)
admin.site.register(WageFixWage, WageFixWageAdmin)
admin.site.register(WageMonth, WageMonthAdmin)
admin.site.register(WagePeriod, WagePeriodAdmin)
admin.site.register(WageBase, WageBaseAdmin)
admin.site.register(WageSkill, WageSkillAdmin)
admin.site.register(WageManage, WageManageAdmin)
# admin.site.unregister(Group)
# admin.site.unregister(User)
