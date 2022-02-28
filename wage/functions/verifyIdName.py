'''
识别员工号和姓名是否对应
'''
from ..models import WageEmployee


def verify(code, name):
    data = WageEmployee.objects.get(emp_id=code)
    if data == name:
        return True
    else:
        return False
