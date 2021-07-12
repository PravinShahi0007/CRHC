from django.contrib import admin
from . import models
from script import export_excel, update_data, ceshi
import datetime


class DateFilter(admin.SimpleListFilter):
	# 添加过滤器
	title = '日期过滤'
	parameter_name = 'date'

	def lookups(self, request, model_admin):
		return (
			('today', '昨天'),
			('month', '本月'),
			('before', '上月'),
		)

	def queryset(self, request, queryset):
		today = datetime.date.today()
		if self.value() == 'today':
			yesterday = today - datetime.timedelta(days=1)
			return queryset.filter(
				user_date__year=yesterday.year,
				user_date__month=yesterday.month,
				user_date__day=yesterday.day
			)
		if self.value() == 'month':
			return queryset.filter(
				user_date__year=today.year,
				user_date__month=today.month
			)
		if self.value() == 'before':
			first = today.replace(day=1)
			last_month = first - datetime.timedelta(days=1)
			return queryset.filter(
				user_date__year=last_month.year,
				user_date__month=last_month.month
			)


class DateFilter1(admin.SimpleListFilter):
	# 添加过滤器
	title = '日期过滤'
	parameter_name = 'date'

	def lookups(self, request, model_admin):
		return (
			('month', '本月'),
			('before', '上月'),
		)

	def queryset(self, request, queryset):
		today = datetime.date.today()
		if self.value() == 'month':
			return queryset.filter(
				check_date__year=today.year,
				check_date__month=today.month
			)
		if self.value() == 'before':
			first = today.replace(day=1)
			last_month = first - datetime.timedelta(days=1)
			return queryset.filter(
				check_date__year=last_month.year,
				check_date__month=last_month.month
			)


class NameAdmin(admin.ModelAdmin):
	actions_on_top = False  # 是否在列表上方显示下拉框
	list_display_links = None  # 链接
	list_display = ('user_num', 'user_name')  # 要显示的列
	search_fields = ['^user_num', '^user_name']  # 在顶部添加一个搜索框
	readonly_fields = ('user_num', 'user_name')  # 不可修改的字段


class GeneralTableAdmin(admin.ModelAdmin):
	actions = ['import_excel']
	# actions_on_top = False  # 是否在列表上方显示下拉框
	list_display_links = None  # 链接
	date_hierarchy = 'user_date'  # 通过日期过滤对象
	list_display = ('user_num', 'user_name', 'user_date', 'user_time')  # 要显示的列
	list_filter = (DateFilter,)  # 过滤栏
	search_fields = ['^user_date', '^user_name', '^user_num']  # 在顶部添加一个搜索框
	readonly_fields = ('user_num', 'user_name', 'user_date', 'user_time')  # 不可修改的字段

	def import_excel(self, request, queryset):
		data = queryset.all()
		export_excel.general_table(data)

		data_message = '导出完成，共导出%s条记录' % data.count()
		self.message_user(request, data_message)

	import_excel.short_description = '所选的打卡记录导出Excel'

	def has_delete_permission(self, request, obj=None):
		# 编辑页面禁用删除按钮
		return False


class RegisterAdmin(admin.ModelAdmin):
	date_hierarchy = 'register_date'  # 通过日期过滤对象
	list_display = ('register_name', 'register_date', 'register_type', 'register_day', 'register_time')
	search_fields = ['^register_name']  # 在顶部添加一个搜索框
	actions = ['data_update']

	def data_update(self, request, queryset):
		data = queryset.all()
		data2 = models.DataScreen.objects.all()
		update_data.update_register(data, data2)

		data_message = '更新完成'
		self.message_user(request, data_message)

	data_update.short_description = '更新'


class DataScreenAdmin(admin.ModelAdmin):
	list_filter = (DateFilter1,)  # 过滤栏
	date_hierarchy = 'check_date'  # 通过日期过滤对象
	actions = ['import_excel', 'data_excel']
	list_display_links = None  # 链接
	list_display = (
		'check_num', 'check_name',
		'check_date', 'check_morning',
		'check_noon', 'check_afternoon',
		'check_state', 'check_day'
	)  # 要显示的列
	readonly_fields = (
		'check_num', 'check_name', 'check_date', 'check_morning', 'check_noon', 'check_afternoon', 'check_state',
		'check_day'
	)  # 不可编辑列
	search_fields = ['^check_num', '^check_name']  # 在顶部添加一个搜索框

	# def import_excel(self, request, queryset):
	# 	data = queryset.all()
	# 	export_excel.data_screen_table(data)
	#
	# 	data_message = '导出完成，共导出%s条记录' % data.count()
	# 	self.message_user(request, data_message)
	#
	# import_excel.short_description = '所选的记录导出Excel'

	def has_delete_permission(self, request, obj=None):
		# 编辑页面禁用删除按钮
		return False

	def data_excel(self, request, queryset):
		name = models.Name.objects.all()
		data = queryset.all()
		ceshi.excel(data, name)

		data_message = '导出完成'
		self.message_user(request, data_message)

	data_excel.short_description = '导出为汇总表'


class LeaveAdmin(admin.ModelAdmin):
	list_display = ['leave_name', 'leave_date', 'leave_time_interval']
	search_fields = ['^leave_name']
	date_hierarchy = 'leave_date'
	actions = ['data_update']

	def data_update(self, request, queryset):
		data = queryset.all()
		data2 = models.DataScreen.objects.all()
		update_data.update_leave(data, data2)

		data_message = '更新完成'
		self.message_user(request, data_message)

	data_update.short_description = '更新'


admin.site.register(models.Name, NameAdmin)
admin.site.register(models.GeneralTable, GeneralTableAdmin)
admin.site.register(models.DataScreen, DataScreenAdmin)
admin.site.register(models.Register, RegisterAdmin)
admin.site.register(models.Leave, LeaveAdmin)
