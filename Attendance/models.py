from django.db import models

# Create your models here.


class Name(models.Model):
	user_num = models.CharField(max_length=40, verbose_name='编号')
	user_name = models.CharField(max_length=40, verbose_name='姓名')

	def __str__(self):
		return self.user_num

	class Meta:
		verbose_name_plural = '人员'


class GeneralTable(models.Model):
	user_num = models.CharField(max_length=40, verbose_name='编号')
	user_name = models.CharField(max_length=40, verbose_name='姓名', null=True)
	user_date = models.DateField(verbose_name='打卡日期')
	user_time = models.TimeField(verbose_name='打卡时间')

	def __str__(self):
		return self.user_num

	class Meta:
		verbose_name_plural = '打卡记录'


class DataScreen(models.Model):
	check_num = models.CharField(max_length=40, verbose_name='编号')
	check_name = models.CharField(max_length=40, verbose_name='姓名')
	check_date = models.DateField(verbose_name='日期')
	check_morning = models.CharField(max_length=40, verbose_name='上午')
	check_noon = models.CharField(max_length=40, null=True, verbose_name='中午')
	check_afternoon = models.CharField(max_length=40, verbose_name='下午')
	check_state = models.CharField(max_length=10, null=True, verbose_name='请假类型')
	check_day = models.CharField(max_length=10, null=True, verbose_name='请假天数')

	def __str__(self):
		return self.check_name

	class Meta:
		verbose_name_plural = '汇总'


class Register(models.Model):
	types = (
		('事假', '事假'),
		('病假', '病假'),
		('丧假', '丧假'),
		('婚假', '婚假'),
	)
	time = (
		('上午', '上午'),
		('下午', '下午'),
		('全天', '全天'),

	)
	register_name = models.CharField(max_length=10, verbose_name='姓名')
	register_date = models.DateField(verbose_name='日期')
	register_type = models.CharField(max_length=10, choices=types, verbose_name='类型')
	register_day = models.CharField(max_length=10, default=1, verbose_name='请假天数')
	register_time = models.CharField(max_length=10, choices=time, default='全天', verbose_name='时间段')

	def __str__(self):
		return self.register_name

	class Meta:
		verbose_name_plural = '请假登记'


class Leave(models.Model):
	time = (
		('上午', '上午'),
		('中午', '中午'),
		('下午', '下午'),
		('全天', '全天'),
	)
	leave_name = models.CharField(max_length=10, verbose_name='姓名')
	leave_date = models.DateField(verbose_name='日期')
	leave_time_interval = models.CharField(max_length=10, choices=time, verbose_name='时间段')

	def __str__(self):
		return self.leave_name

	class Meta:
		verbose_name_plural = '外出、报备登记'
