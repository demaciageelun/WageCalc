# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class WageDeptment(models.Model):
    dept_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门编码')
    dept_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门名')
    dept_base = models.CharField(max_length=255, blank=True, null=True, verbose_name='所属基地')

    def __str__(self):
        return str(self.dept_name)

    class Meta:
        managed = False
        db_table = 'wage_deptment'
        verbose_name = '部门表'
        verbose_name_plural = '部门表'


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


class WageEmployee(models.Model):
    emp_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工工号')
    emp_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工名')
    emp_dept = models.ForeignKey(WageDeptment, models.DO_NOTHING, blank=True, null=True, verbose_name='部门')
    emp_posi = models.ForeignKey('WagePosition', models.DO_NOTHING, blank=True, null=True, verbose_name='岗位')
    emp_entry_date = models.DateField(blank=True, null=True, verbose_name='入职日期')
    emp_leave_date = models.DateField(blank=True, null=True, verbose_name='离职日期')
    emp_job_status = models.IntegerField(blank=True, null=True, verbose_name='在职状态', choices=job_status_choices)
    emp_job_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='在职类型')

    def __str__(self):
        return str(self.emp_name)

    class Meta:
        managed = False
        db_table = 'wage_employee'
        verbose_name = '员工表'
        verbose_name_plural = '员工表'


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
    into_period = models.ForeignKey(WagePeriod, models.DO_NOTHING, blank=True, null=True, verbose_name='周期')
    into_periods = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期')
    into_expense = models.ForeignKey(WageExpense, models.DO_NOTHING, blank=True, null=True, verbose_name='费用项目')
    into_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='原因')
    into_calc_elem_1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='计算要素1')
    into_calc_elem_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='计算要素2')
    into_calc_elem_other = models.CharField(max_length=255, blank=True, null=True, verbose_name='其他计算要素')
    into_money = models.FloatField(blank=True, null=True, verbose_name='金额')
    into_effecte_date = models.DateField(blank=True, null=True, verbose_name='生效日期')
    into_expir_date = models.DateField(blank=True, null=True, verbose_name='失效日期')

    class Meta:
        managed = False
        db_table = 'wage_expense_into'
        verbose_name = '费用引入表'
        verbose_name_plural = '费用引入表'


class WagePerformanceInto(models.Model):
    perfor_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True, verbose_name='员工')
    perfor_period = models.ForeignKey(WagePeriod, models.DO_NOTHING, blank=True, null=True, verbose_name='周期')
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

    class Meta:
        managed = False
        db_table = 'wage_performance_into'
        verbose_name = '绩效表'
        verbose_name_plural = '绩效表'


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
    fix_wage_stand = models.FloatField(blank=True, null=True, verbose_name='工资标准')
    fix_base_wage = models.FloatField(blank=True, null=True, verbose_name='基本工资')
    fix_post_wage = models.FloatField(blank=True, null=True, verbose_name='岗位工资')
    fix_perfor_wage = models.FloatField(blank=True, null=True, verbose_name='绩效工资')
    fix_skill_wage = models.FloatField(blank=True, null=True, verbose_name='技能津贴')
    fix_manage_wage = models.FloatField(blank=True, null=True, verbose_name='管理津贴')
    fix_phone_subsidy = models.FloatField(blank=True, null=True, verbose_name='话费补助')
    fix_change_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='变更原因')
    fix_resource = models.CharField(max_length=255, blank=True, null=True, verbose_name='数据来源')

    class Meta:
        managed = False
        db_table = 'wage_fix_wage'
        verbose_name = '固定工资表'
        verbose_name_plural = '固定工资表'


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
