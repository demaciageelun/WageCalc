# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class WageDeptment(models.Model):
    dept_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门编码')
    dept_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门名')
    dept_base = models.CharField(max_length=255, blank=True, null=True, verbose_name='管理归属')
    dept_short_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门简称')

    def __str__(self):
        return str(isNull(self.dept_name) + '  | |  ' + self.dept_base + '  | |  ' + isNull(self.dept_short_name))

    class Meta:
        managed = False
        db_table = 'wage_deptment'
        verbose_name = '部门表'
        verbose_name_plural = '部门表'


class WageRank(models.Model):
    rank_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='合同归属')

    def __str__(self):
        return str(self.rank_name)

    class Meta:
        managed = False
        db_table = 'wage_rank'
        verbose_name = '合同归属表'
        verbose_name_plural = '合同归属表'


class WageField(models.Model):
    field_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段中文名')
    field_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='字段代码')

    def __str__(self):
        return str(isNull(self.field_name) + '  | |  ' + self.field_code)

    class Meta:
        managed = False
        db_table = 'wage_field'
        verbose_name = '字段权限表'
        verbose_name_plural = '字段权限表'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(WageDeptment, verbose_name='部门')
    rank = models.ManyToManyField(WageRank, verbose_name='合同归属')
    is_full = models.BooleanField(verbose_name='能否看到本基地部门所有上传数据')
    field = models.ManyToManyField(WageField, verbose_name='授权字段')
    is_time = models.BooleanField(verbose_name='是否只能看到计时制数据')

    class Meta:
        managed = False
        db_table = 'my_user'
        verbose_name_plural = '管辖范围'
        verbose_name = '管辖范围'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class WageJobLevel(models.Model):
    level_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级编码')
    level_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级名称')

    def __str__(self):
        return str(self.level_name)

    class Meta:
        managed = False
        db_table = 'wage_job_level'
        verbose_name_plural = '职级表'
        verbose_name = '职级表'


def isNull(data):
    if data != "" and data is not None:
        return data
    else:
        return "..."


class WageBase(models.Model):
    base_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='基地名')

    def __str__(self):
        return str(self.base_name)

    class Meta:
        managed = False
        db_table = 'wage_base'
        verbose_name = '基地表'
        verbose_name_plural = '基地表'


class WagePeriod(models.Model):
    period_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')

    def __str__(self):
        return str(self.period_name)

    class Meta:
        managed = False
        db_table = 'wage_period'
        verbose_name = '周期表'
        verbose_name_plural = '周期表'


job_status_choices = (
    (1, '在职'),
    (2, '离职'),
    (99, '黑名单')
)
pay_type_choices = (
    (1, '计时制'),
    (2, '责任制')
)


class WageEmployee(models.Model):
    emp_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工工号')
    emp_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工名')
    emp_dept = models.ForeignKey('WageDeptment', models.DO_NOTHING, blank=True, null=True, verbose_name='部门')
    emp_posi = models.ForeignKey('WagePosition', models.DO_NOTHING, blank=True, null=True, verbose_name='岗位')
    emp_entry_date = models.DateField(blank=True, null=True, verbose_name='集团入职日期')
    emp_leave_date = models.DateField(blank=True, null=True, verbose_name='离职结薪日期')
    emp_job_status = models.IntegerField(blank=True, null=True, verbose_name='在职状态', choices=job_status_choices)
    emp_job_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='在职类型')
    emp_rank = models.ForeignKey('WageRank', models.DO_NOTHING, blank=True, null=True, verbose_name='合同归属')
    emp_in_date = models.DateField(blank=True, null=True, verbose_name='入职日期')
    emp_leave_bl_date = models.DateField(blank=True, null=True, verbose_name='离职办理日期')
    emp_base = models.ForeignKey('WageBase', models.DO_NOTHING, blank=True, null=True, verbose_name='基地')
    emp_job_level = models.ForeignKey('WageJobLevel', models.DO_NOTHING, blank=True, null=True, verbose_name='职级')
    emp_dlidl = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工类型')
    emp_pay_type = models.IntegerField(blank=True, null=True, verbose_name='计薪方式', choices=pay_type_choices)
    emp_id_num = models.CharField(max_length=255, blank=True, null=True, verbose_name='身份证')
    emp_source = models.CharField(max_length=255, blank=True, null=True, verbose_name='招聘来源')
    emp_tel = models.CharField(max_length=255, blank=True, null=True, verbose_name='联系方式')
    emp_gsgs = models.CharField(max_length=255, blank=True, null=True, verbose_name='等级')

    def __str__(self):
        return str(self.emp_name)

    class Meta:
        managed = False
        db_table = 'wage_employee'
        verbose_name = '员工表'
        verbose_name_plural = '员工表'
        permissions = [('can_download_employee', u'下载员工信息')]


class WageExpense(models.Model):
    expense_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='费用项目')

    def __str__(self):
        return str(self.expense_name)

    class Meta:
        managed = False
        db_table = 'wage_expense'
        verbose_name = '费用项目表'
        verbose_name_plural = '费用项目表'


class WageExpenseInto(models.Model):
    into_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    # into_period = models.ForeignKey(WagePeriod, models.DO_NOTHING, blank=True, null=True, verbose_name='周期')
    into_periods = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')
    into_expense = models.ForeignKey(WageExpense, models.DO_NOTHING, blank=True, null=True, verbose_name='费用项目')
    into_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='原因')
    into_calc_elem_1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='计算要素1')
    into_calc_elem_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='计算要素2')
    into_calc_elem_other = models.CharField(max_length=255, blank=True, null=True, verbose_name='其他计算要素')
    into_money = models.FloatField(blank=True, null=True, verbose_name='金额')
    into_effecte_date = models.DateField(blank=True, null=True, verbose_name='生效日期')
    into_expir_date = models.DateField(blank=True, null=True, verbose_name='失效日期')
    into_creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    into_create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')

    class Meta:
        managed = False
        db_table = 'wage_expense_into'
        verbose_name = '费用引入表'
        verbose_name_plural = '费用引入表'
        permissions = [('can_import_expense', u'导入费用')]


class WagePerformanceInto(models.Model):
    perfor_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    perfor_center = models.CharField(max_length=255, blank=True, null=True, verbose_name='中心别')
    perfor_periods = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')
    perfor_period_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期类型')
    perfor_costs_attach = models.CharField(max_length=255, blank=True, null=True, verbose_name='成本归属')
    perfor_proof_ip = models.FloatField(blank=True, null=True, verbose_name='个人绩效指数占比')
    perfor_proof_dp = models.FloatField(blank=True, null=True, verbose_name='部门绩效指数占比')
    perfor_proof_cp = models.FloatField(blank=True, null=True, verbose_name='公司绩效指数占比')
    perfor_score_ip = models.FloatField(blank=True, null=True, verbose_name='个人绩效分数')
    perfor_score_dp = models.FloatField(blank=True, null=True, verbose_name='部门绩效分数')
    perfor_score_cp = models.FloatField(blank=True, null=True, verbose_name='公司绩效分数')
    perfor_ratio_ip = models.FloatField(blank=True, null=True, verbose_name='个人绩效系数')
    perfor_ratio_dp = models.FloatField(blank=True, null=True, verbose_name='部门绩效系数')
    perfor_ratio_cp = models.FloatField(blank=True, null=True, verbose_name='公司绩效系数')
    perfor_ratio_tp = models.FloatField(blank=True, null=True, verbose_name='综合绩效系数')
    perfor_result = models.CharField(max_length=255, blank=True, null=True, verbose_name='考核结果')
    perfor_creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    perfor_create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')

    class Meta:
        managed = False
        db_table = 'wage_performance_into'
        verbose_name = '绩效表'
        verbose_name_plural = '绩效表'
        permissions = [('can_import_performance', u'导入绩效')]


class WagePosition(models.Model):
    posi_id = models.CharField(max_length=255, verbose_name='岗位编码')
    posi_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位名')

    def __str__(self):
        return str(self.posi_name)

    class Meta:
        managed = False
        db_table = 'wage_position'
        verbose_name = '岗位表'
        verbose_name_plural = '岗位表'


class WageFixWage(models.Model):
    fix_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    fix_change_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='类型')
    fix_begin_date = models.DateField(blank=True, null=True, verbose_name='起始日期')
    fix_work_pro = models.CharField(max_length=255, blank=True, null=True, verbose_name='工序')
    fix_wage_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='薪酬类型')
    fix_skill_level = models.CharField(max_length=255, blank=True, null=True, verbose_name='技能等级')
    fix_manage_level = models.CharField(max_length=255, blank=True, null=True, verbose_name='管理等级')
    fix_wage_stand = models.FloatField(blank=True, null=True, verbose_name='标准工资')
    fix_base_wage = models.FloatField(blank=True, null=True, verbose_name='基本工资')
    fix_post_wage = models.FloatField(blank=True, null=True, verbose_name='岗位工资')
    fix_perfor_wage = models.FloatField(blank=True, null=True, verbose_name='绩效工资')
    fix_skill_wage = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    fix_manage_wage = models.FloatField(blank=True, null=True, verbose_name='管理津贴')
    fix_phone_subsidy = models.FloatField(blank=True, null=True, verbose_name='话费补助')
    fix_change_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='变更原因')
    fix_resource = models.CharField(max_length=255, blank=True, null=True, verbose_name='数据来源')
    fix_creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    fix_create_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')

    class Meta:
        managed = False
        db_table = 'wage_fix_wage'
        verbose_name = '固定工资表'
        verbose_name_plural = '固定工资表'
        permissions = [('can_import_fix', u'导入固定工资')]


class WageMonth(models.Model):
    mon_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    mon_period = models.ForeignKey(WagePeriod, models.DO_NOTHING, blank=True, null=True, verbose_name='周期')
    mon_periods = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')
    mon_wage_way = models.CharField(max_length=255, blank=True, null=True, verbose_name='计薪方式')
    mon_standard_wage = models.FloatField(blank=True, null=True, verbose_name='标准工资')
    mon_base_wage = models.FloatField(blank=True, null=True, verbose_name='基本工资')
    mon_post_wage = models.FloatField(blank=True, null=True, verbose_name='岗位工资')
    mon_perfor_wage = models.FloatField(blank=True, null=True, verbose_name='绩效工资')
    mon_manage_wage = models.FloatField(blank=True, null=True, verbose_name='管理津贴')
    mon_seniority_wage = models.FloatField(blank=True, null=True, verbose_name='年资津贴')
    mon_post_subsidy = models.FloatField(blank=True, null=True, verbose_name='岗位补贴')
    mon_skill_wage = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    mon_perfor_merit = models.FloatField(blank=True, null=True, verbose_name='绩效系数')
    mon_reward_punish = models.FloatField(blank=True, null=True, verbose_name='奖惩')
    mon_other_deduc = models.FloatField(blank=True, null=True, verbose_name='其他补扣款')
    mon_si_af_deduc = models.FloatField(blank=True, null=True, verbose_name='社保公积金补扣款')
    mon_reward = models.FloatField(blank=True, null=True, verbose_name='奖金/津贴')
    mon_phyexam = models.FloatField(blank=True, null=True, verbose_name='体检费报销')
    mon_water_elect = models.FloatField(blank=True, null=True, verbose_name='代收水电费')
    mon_rent = models.FloatField(blank=True, null=True, verbose_name='代收房租')
    mon_quart_bonus = models.FloatField(blank=True, null=True, verbose_name='季度奖金')
    mon_annual_bonus = models.FloatField(blank=True, null=True, verbose_name='年度奖金')
    mon_sale_com = models.FloatField(blank=True, null=True, verbose_name='销售提成')
    mon_temp_wage = models.FloatField(blank=True, null=True, verbose_name='临时补贴')
    mon_laber_cost = models.FloatField(blank=True, null=True, verbose_name='劳务费')
    mon_income_tax = models.FloatField(blank=True, null=True, verbose_name='个人所得税')
    mon_non_compet = models.FloatField(blank=True, null=True, verbose_name='竞业限制补偿金')
    mon_severance = models.FloatField(blank=True, null=True, verbose_name='离职补偿金')

    class Meta:
        managed = False
        db_table = 'wage_month'
        verbose_name = '月度工资汇总表'
        verbose_name_plural = '月度工资汇总表'
        permissions = [('can_export_month', u'导出月度工资汇总表')]


class WageFixLog(models.Model):
    log_creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    log_time = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    log_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    log_change_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='变动类型')
    log_begin_date = models.DateField(blank=True, null=True, verbose_name='起始日期')
    log_work_pro = models.CharField(max_length=255, blank=True, null=True, verbose_name='工序')
    log_wage_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='工序')
    log_skill_level = models.CharField(max_length=255, blank=True, null=True, verbose_name='技能等级')
    log_manage_level = models.CharField(max_length=255, blank=True, null=True, verbose_name='管理等级')
    log_wage_stand = models.FloatField(blank=True, null=True, verbose_name='工资标准')
    log_base_wage = models.FloatField(blank=True, null=True, verbose_name='基本工资')
    log_post_wage = models.FloatField(blank=True, null=True, verbose_name='岗位工资')
    log_perfor_wage = models.FloatField(blank=True, null=True, verbose_name='绩效工资')
    log_skill_wage = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    log_manage_wage = models.FloatField(blank=True, null=True, verbose_name='管理津贴')
    log_phone_subsidy = models.FloatField(blank=True, null=True, verbose_name='话费补助')
    log_change_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='变更原因')
    log_resource = models.CharField(max_length=255, blank=True, null=True, verbose_name='数据来源')

    class Meta:
        managed = False
        db_table = 'wage_fix_log'
        verbose_name = '固定工资导入日志'
        verbose_name_plural = '固定工资导入日志'


# 离职理由
class LeaveReason(models.Model):
    leave_reason_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='离职理由')

    def __str__(self):
        return self.leave_reason_name

    class Meta:
        managed = False
        db_table = 'leave_reason'
        verbose_name_plural = '离职理由表'
        verbose_name = '离职理由表'


success_choice = (
    ('Y', '成功'),
    ('N', '失败'),
)
other_choice = (
    ('Y', '是'),
    ('N', '否'),
)


# 离职台账表
class LeaveAccount(models.Model):
    leave_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, verbose_name="员工", related_name='emp')
    leave_dates = models.DateField(blank=True, null=True, verbose_name="面谈日期")
    leave_leading_man = models.CharField(max_length=255, blank=True, null=True, verbose_name='负责人')
    leave_prepare_leave_date = models.DateField(blank=True, null=True, verbose_name="预离职日期")
    leave_reason = models.ForeignKey(LeaveReason, models.DO_NOTHING, verbose_name="离职原因")
    leave_content = models.CharField(max_length=255, blank=True, null=True, verbose_name='具体内容')
    leave_is_success = models.CharField(max_length=255, blank=True, null=True, verbose_name='是否挽留成功', choices=success_choice)
    leave_is_other = models.CharField(max_length=255, blank=True, null=True, verbose_name='是否愿意去其他基地', choices=other_choice)
    leave_remarks = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    leave_suggests = models.CharField(max_length=255, blank=True, null=True, verbose_name='建议')
    leave_creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='修改人')
    leave_create_time = models.DateTimeField(blank=True, null=True, verbose_name="修改时间", auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'leave_account'
        verbose_name_plural = '员工离职面谈台账'
        verbose_name = '员工离职面谈台账'


class WageSkill(models.Model):
    skill_grade = models.CharField(max_length=255, blank=True, null=True, verbose_name='技能等级')
    skill_allowance = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    skill_local = models.ManyToManyField(WageBase, verbose_name='基地')
    skill_dept = models.ManyToManyField(WageDeptment, verbose_name='部门')
    skill_job_level = models.ManyToManyField(WageJobLevel, verbose_name='职级')

    class Meta:
        managed = True
        db_table = 'wage_skill'
        verbose_name = '技能津贴表'
        verbose_name_plural = '技能津贴表'


class WageManage(models.Model):
    manage_position = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位')
    manage_grade = models.CharField(max_length=255, blank=True, null=True, verbose_name='管理等级')
    manage_allowance = models.FloatField(blank=True, null=True, verbose_name='管理津贴')

    class Meta:
        managed = False
        db_table = 'wage_manage'
        verbose_name = '管理津贴表'
        verbose_name_plural = '管理津贴表'


class WageLeave(models.Model):
    leave_wage_period = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')
    leave_tel = models.CharField(max_length=255, blank=True, null=True, verbose_name='手机号码')
    leave_emp_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='工号')
    leave_emp_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='身份证号')
    leave_emp_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工姓名')
    leave_emp_dept = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门简称')
    leave_emp_post = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位名称')
    leave_wage_date = models.DateField(blank=True, null=True, verbose_name='离职结薪日期')
    leave_base_wage = models.FloatField(blank=True, null=True, verbose_name='基本工资')
    leave_position_wage = models.FloatField(blank=True, null=True, verbose_name='岗位工资')
    leave_perfor_wage = models.FloatField(blank=True, null=True, verbose_name='绩效工资')
    leave_phone = models.FloatField(blank=True, null=True, verbose_name='话费补贴')
    leave_skill = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    leave_manage = models.FloatField(blank=True, null=True, verbose_name='管理津贴')
    leave_year = models.FloatField(blank=True, null=True, verbose_name='年资津贴')
    leave_fix = models.FloatField(blank=True, null=True, verbose_name='固定补贴')
    leave_eat = models.FloatField(blank=True, null=True, verbose_name='就餐补贴')
    leave_s_base_wage = models.FloatField(blank=True, null=True, verbose_name='应发基本工资')
    leave_s_position_wage = models.FloatField(blank=True, null=True, verbose_name='应发岗位工资')
    leave_perfor_ratio = models.FloatField(blank=True, null=True, verbose_name='综合绩效系数')
    leave_perfor = models.FloatField(blank=True, null=True, verbose_name='绩效')
    leave_subsidy = models.FloatField(blank=True, null=True, verbose_name='补贴合计')
    leave_over = models.FloatField(blank=True, null=True, verbose_name='加班费')
    leave_night = models.FloatField(blank=True, null=True, verbose_name='夜班津贴')
    leave_rp = models.FloatField(blank=True, null=True, verbose_name='奖惩')
    leave_reward = models.FloatField(blank=True, null=True, verbose_name='奖金')
    leave_temp = models.FloatField(blank=True, null=True, verbose_name='临时补贴')
    leave_test = models.FloatField(blank=True, null=True, verbose_name='体检报销费用')
    leave_attend = models.FloatField(blank=True, null=True, verbose_name='考勤异常扣款')
    leave_holiday = models.FloatField(blank=True, null=True, verbose_name='请假补扣款')
    leave_pfund = models.FloatField(blank=True, null=True, verbose_name='社保公积金补扣')
    leave_other = models.FloatField(blank=True, null=True, verbose_name='其他补扣款')
    leave_compet = models.FloatField(blank=True, null=True, verbose_name='竞业补偿金')
    leave_total_wage = models.FloatField(blank=True, null=True, verbose_name='应发合计')
    leave_person_insur = models.FloatField(blank=True, null=True, verbose_name='社保公积金个人承担')
    leave_comp_insur = models.FloatField(blank=True, null=True, verbose_name='社保公积金公司承担')
    leave_income_tax = models.FloatField(blank=True, null=True, verbose_name='代扣个税')
    leave_we = models.FloatField(blank=True, null=True, verbose_name='水电费')
    leave_house = models.FloatField(blank=True, null=True, verbose_name='房租费')
    leave_otherplus = models.FloatField(blank=True, null=True, verbose_name='其他加')
    leave_othersub = models.FloatField(blank=True, null=True, verbose_name='其他减')
    leave_disp = models.FloatField(blank=True, null=True, verbose_name='一次性补偿金')
    leave_special = models.FloatField(blank=True, null=True, verbose_name='专项附加扣除合计')
    leave_actual_wage = models.FloatField(blank=True, null=True, verbose_name='实发工资')
    leave_remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='薪资备注')

    class Meta:
        managed = False
        db_table = 'wage_leave'
        verbose_name = '离职人员工资表'
        verbose_name_plural = '离职人员工资表'
        permissions = [('can_import_month', u'导入离职人员工资表')]


standards_zg_degree_choices = (
    (1, '一级'),
    (2, '二级'),
    (3, '三级')
)


class RecomdStandards(models.Model):
    standards_effect_date = models.DateField(blank=True, null=True, verbose_name='生效日期')
    standards_invalid_date = models.DateField(blank=True, null=True, verbose_name='失效日期')
    standards_job_levels = models.ManyToManyField(WageJobLevel, verbose_name='职级')
    standards_zg_degree = models.IntegerField(blank=True, null=True, choices=standards_zg_degree_choices, verbose_name='助工等级')
    standards_first_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第一次发放月')
    standards_second_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第二次发放月')
    standards_third_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第三次发放月')
    standards_four_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第四次发放月')
    standards_five_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第五次发放月')
    standards_six_month = models.IntegerField(blank=True, null=True, verbose_name='入职后第六次发放月')
    standards_first_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第一次发放金额')
    standards_second_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第二次发放金额')
    standards_third_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第三次发放金额')
    standards_four_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第四次发放金额')
    standards_five_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第五次发放金额')
    standards_six_money = models.FloatField(blank=True, null=True, verbose_name='推荐人第六次发放金额')
    standards_first_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第一次发放金额')
    standards_second_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第二次发放金额')
    standards_third_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第三次发放金额')
    standards_four_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第四次发放金额')
    standards_five_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第五次发放金额')
    standards_six_money_b = models.FloatField(blank=True, null=True, verbose_name='被推荐人第六次发放金额')
    create_user = models.CharField(max_length=100, verbose_name='创建者')
    modify_user = models.CharField(max_length=100, verbose_name='修改者')
    create_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    modify_time = models.DateTimeField(blank=True, null=True, verbose_name="修改时间", auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'recomd_standards'
        verbose_name = '内荐奖励标准'
        verbose_name_plural = '内荐奖励标准'


Candidates_status_choices = (
    (1, '正常'),
    (2, '二次入职'),
    (2, '劳务输入')
)


class RecomdCandidates(models.Model):
    Candidates_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, related_name='Candidates_emp', verbose_name="推荐人")
    Candidates_emp_b = models.ForeignKey(WageEmployee, models.DO_NOTHING, related_name='Candidates_emp_b', verbose_name="被推荐人")
    Candidates_native = models.CharField(max_length=255, blank=True, null=True, verbose_name='籍贯')
    Candidates_peer_exper = models.BooleanField(verbose_name='是否有同行经验')
    Candidates_peer = models.CharField(max_length=255, blank=True, null=True, verbose_name='同行名称')
    Candidates_status = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工状态', choices=Candidates_status_choices)
    create_user = models.CharField(max_length=100, verbose_name='创建者')
    modify_user = models.CharField(max_length=100, verbose_name='修改者')
    create_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    modify_time = models.DateTimeField(blank=True, null=True, verbose_name="修改时间", auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'recomd_candidates'
        verbose_name = '内荐名单'
        verbose_name_plural = '内荐名单'


class WageLog(models.Model):
    log_user = models.CharField(max_length=100, blank=True, null=True, verbose_name='上传人')
    log_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='模块')
    log_path = models.CharField(max_length=255, blank=True, null=True, verbose_name='文件路径')
    log_file_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='文件名')
    log_create_time = models.DateTimeField(blank=True, null=True, verbose_name="上传时间", auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'wage_log'
        verbose_name = '文件上传日志'
        verbose_name_plural = '文件上传日志'
