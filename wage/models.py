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
    dept_id = models.IntegerField(verbose_name='部门编码')
    dept_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门名')
    dept_base = models.CharField(max_length=255, blank=True, null=True, verbose_name='所属基地')

    class Meta:
        managed = False
        db_table = 'wage_deptment'
        verbose_name = '部门表'


class WageEmployee(models.Model):
    emp_id = models.IntegerField(blank=True, null=True)
    emp_name = models.CharField(max_length=255, blank=True, null=True)
    emp_dept = models.ForeignKey(WageDeptment, models.DO_NOTHING, blank=True, null=True)
    emp_posi = models.ForeignKey('WagePosition', models.DO_NOTHING, blank=True, null=True)
    emp_entry_date = models.DateField(blank=True, null=True)
    emp_leave_date = models.DateField(blank=True, null=True)
    emp_job_status = models.IntegerField(blank=True, null=True)
    emp_job_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wage_employee'


class WageExpense(models.Model):
    expense_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wage_expense'


class WageExpenseInto(models.Model):
    into_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True)
    into_period = models.DateField(blank=True, null=True)
    into_expense = models.ForeignKey(WageExpense, models.DO_NOTHING, blank=True, null=True)
    into_reason = models.CharField(max_length=255, blank=True, null=True)
    into_calc_elem_1 = models.CharField(max_length=255, blank=True, null=True)
    into_calc_elem_2 = models.CharField(max_length=255, blank=True, null=True)
    into_calc_elem_other = models.CharField(max_length=255, blank=True, null=True)
    into_money = models.FloatField(blank=True, null=True)
    into_effecte_date = models.DateField(blank=True, null=True)
    into_expir_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wage_expense_into'


class WagePerformanceInto(models.Model):
    perfor_emp = models.ForeignKey(WageEmployee, models.DO_NOTHING, blank=True, null=True)
    perfor_period = models.DateField(blank=True, null=True)
    perfor_period_type = models.CharField(max_length=255, blank=True, null=True)
    perfor_costs_attach = models.CharField(db_column='perfor_costs attach', max_length=255, blank=True,
                                           null=True)  # Field renamed to remove unsuitable characters.
    perfor_proof_ip = models.FloatField(blank=True, null=True)
    perfor_proof_dp = models.FloatField(blank=True, null=True)
    perfor_proof_cp = models.FloatField(blank=True, null=True)
    perfor_score_ip = models.FloatField(blank=True, null=True)
    perfor_score_dp = models.FloatField(blank=True, null=True)
    perfor_score_cp = models.FloatField(blank=True, null=True)
    perfor_ratio_ip = models.FloatField(blank=True, null=True)
    perfor_ratio_dp = models.FloatField(blank=True, null=True)
    perfor_ratio_cp = models.FloatField(blank=True, null=True)
    perfor_ratio_tp = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wage_performance_into'


class WagePosition(models.Model):
    posi_id = models.IntegerField(verbose_name='岗位id')
    posi_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wage_position'
