import openpyxl
from django.contrib import admin
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin
from django.shortcuts import render, HttpResponse

from .models import WageDeptment


# Register your models here.
class WageDeptmentAdmin(AjaxAdmin):
    list_display = ['dept_id', 'dept_name', 'dept_base']
    actions = ['upload_file']

    def upload_file(self, request, queryset):
        # 这里的upload 就是和params中配置的key一样
        upload = request.FILES['upload']
        # 将上传的文件保存到static中
        with open('static/' + upload.name, 'wb') as f:
            for line in upload.chunks():
                f.write(line)
        f.close()

        # 读取excel需要考虑文件格式，分为xls和xlsx。xls需要使用xlrd,xlsx需要使用openpyxl
        workbook = openpyxl.load_workbook('static/' + upload.name)
        # 可以使用workbook对象的sheetnames属性获取到excel文件中哪些表有数据
        table = workbook.active
        rows = table.max_row
        cols = table.max_column
        for row in range(rows):
            for col in range(cols):
                data = table.cell(row + 1, col + 1).value
                print(data)
        # 后续进行数据处理
        return JsonResponse(data={
            'status': 'success',
            'msg': '成功！'
        })

    upload_file.short_description = '文件上传对话框'
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


admin.site.register(WageDeptment, WageDeptmentAdmin)
