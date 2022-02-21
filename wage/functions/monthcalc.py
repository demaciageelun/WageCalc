"""
1、遍历emp表。
2、根据员工找到固定工资表，创建表单。
3、根据选中的周期，筛选当前员工的当周期的绩效、费用引入表，根据计算规则，写入月度工资表
"""

from django.db.models import Q

from wage.models import WagePeriod, WageEmployee, WageFixWage, WageMonth, WagePerformanceInto, WageExpenseInto


def calc(period_id):
    # 根据选择的周期确定需要计算工资的人员，人员包括：1、离职日期为空的人。2、离职日期以周期开头的。即计算1月份的工资的话，筛选离职日期为空的人和1月份离职的人。默认不会提前一个月设置离职日期。
    # period = WagePeriod.objects.filter(id=period_id).values('period_name')
    emp_list = WageEmployee.objects.filter(
        Q(emp_leave_date=None) | Q(emp_leave_date__startswith=str(period_id))).values('id')
    # 根据员工工号获取固定工资信息，再依次写入月度工资表中。使用in的写法，减少遍历，速度加快很多。
    sql = "select id,fix_emp_id,fix_wage_stand,fix_base_wage,fix_wage_type,fix_post_wage,fix_perfor_wage,fix_skill_wage,fix_manage_wage,fix_phone_subsidy from wage_fix_wage where fix_emp_id in ({})".format(
        ','.join(["'%s'" % item['id'] for item in emp_list]))
    testdata = WageFixWage.objects.raw(sql)
    for obj in testdata:
        WageMonth.objects.update_or_create(
            defaults={
                'mon_emp_id': obj.fix_emp_id,
                'mon_periods': str(period_id),
                'mon_wage_way': obj.fix_wage_type,
                'mon_standard_wage': obj.fix_wage_stand,
                'mon_base_wage': obj.fix_base_wage,
                'mon_post_wage': obj.fix_post_wage,
                'mon_perfor_wage': obj.fix_perfor_wage,
                'mon_manage_wage': obj.fix_skill_wage,
                'mon_skill_wage': obj.fix_manage_wage,
            },
            mon_emp_id=obj.fix_emp_id,
            mon_periods=str(period_id)
        )

    # 查找绩效表，获取当月绩效数据
    sql = (
            "select id,perfor_emp_id,perfor_ratio_tp from wage_performance_into where perfor_emp_id in ({}) and perfor_periods = '" + str(
        period_id) + "'").format(
        ','.join(["'%s'" % item['id'] for item in emp_list]))
    testdata = WagePerformanceInto.objects.raw(sql)
    for obj in testdata:
        WageMonth.objects.update_or_create(
            defaults={
                'mon_emp_id': obj.perfor_emp_id,
                'mon_periods': str(period_id),
                'mon_perfor_merit': obj.perfor_ratio_tp,

            },
            mon_emp_id=obj.perfor_emp_id,
            mon_periods=str(period_id)
        )
    # 查找费用项目表，行列转换费用引入表。
    # 根据员工号用in一次性查询，再遍历写入月度工资表中，减少一次遍历，加快程序运行
    # sql = (
    #         "select id, into_emp_id as '工号',sum(case into_expense_id when 8 then into_money else 0 end) '餐补',sum(case into_expense_id when 9 then into_money else 0 end) '劳动报酬',sum(case into_expense_id when 10 then into_money else 0 end) '国内外派津贴' from wage_expense_into where into_emp_id in ({}) and into_period_id = " + period_id + " GROUP BY into_emp_id").format(
    #     ','.join(["'%s'" % item['id'] for item in emp_list]))

    sql = ("select id, into_emp_id,into_periods,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '奖惩') then into_money else 0 end) 'expense1',\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '停车费') then into_money else 0 end) 'expense2',\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '司机里程补贴') then into_money else 0 end) 'expense3' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '行政扣款') then into_money else 0 end) 'expense4' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '人事扣款') then into_money else 0 end) 'expense5' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '内荐费') then into_money else 0 end) 'expense6' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '购车补贴') then into_money else 0 end) 'expense7' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '其他扣款') then into_money else 0 end) 'expense8' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '离职调休折算') then into_money else 0 end) 'expense9' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '餐补') then into_money else 0 end) 'expense10' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '其他原因') then into_money else 0 end) 'expense11' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '劳务报酬') then into_money else 0 end) 'expense12' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '社保公积金补扣款') then into_money else 0 end) 'expense13' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '国内外派津贴') then into_money else 0 end) 'expense14' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '境外外派津贴') then into_money else 0 end) 'expense15' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '中心比拼奖金') then into_money else 0 end) 'expense16' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '项目奖金') then into_money else 0 end) 'expense17' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = 'KPI排名奖励') then into_money else 0 end) 'expense18' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '体检费报销') then into_money else 0 end) 'expense19' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '水电费') then into_money else 0 end) 'expense20' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '房租') then into_money else 0 end) 'expense21' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '季度奖金') then into_money else 0 end) 'expense22' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '年度奖金') then into_money else 0 end) 'expense23' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '销售奖励') then into_money else 0 end) 'expense24' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '高温费') then into_money else 0 end) 'expense25' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '留任补贴') then into_money else 0 end) 'expense26' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '劳务转正费') then into_money else 0 end) 'expense27' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '劳务补贴') then into_money else 0 end) 'expense28' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '外包管理费') then into_money else 0 end) 'expense29' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '个税') then into_money else 0 end) 'expense30' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '竞业限制补偿金') then into_money else 0 end) 'expense31' ,\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '离职补偿金') then into_money else 0 end) 'expense32',\
            sum(case into_expense_id when (SELECT id from wage_expense where expense_name = '岗位补贴') then into_money else 0 end) 'expense33'\
            from wage_expense_into where into_emp_id in ({}) and into_periods = '" + str(
        period_id) + "' GROUP BY into_emp_id").format(
        ','.join(["'%s'" % item['id'] for item in emp_list]))

    expense_list = WageExpenseInto.objects.raw(sql)
    print(expense_list)
    for obj in expense_list:
        print(obj.into_emp_id)
        WageMonth.objects.update_or_create(
            defaults={
                'mon_emp_id': obj.into_emp_id,
                'mon_periods': str(period_id),
                'mon_reward_punish': obj.expense1,
                'mon_other_deduc': obj.expense2 + obj.expense3 + obj.expense4 + obj.expense5 + obj.expense6 +
                                   obj.expense7 + obj.expense8 + obj.expense9 + obj.expense10 + obj.expense11 +
                                   obj.expense12,
                'mon_si_af_deduc': obj.expense13,
                'mon_reward': obj.expense14 + obj.expense15 + obj.expense16 + obj.expense17 + obj.expense18,
                'mon_phyexam': obj.expense19,
                'mon_water_elect': obj.expense20,
                'mon_rent': obj.expense21,
                'mon_quart_bonus': obj.expense22,
                'mon_annual_bonus': obj.expense23,
                'mon_sale_com': obj.expense24,
                'mon_temp_wage': obj.expense25 + obj.expense26,
                'mon_laber_cost': obj.expense27 + obj.expense28 + obj.expense29,
                'mon_income_tax': obj.expense30,
                'mon_non_compet': obj.expense31,
                'mon_severance': obj.expense32,
                'mon_post_subsidy': obj.expense33
            },
            mon_emp_id=obj.into_emp_id,
            mon_periods=str(period_id)
        )
