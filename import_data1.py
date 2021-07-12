# _*_ coding:gbk _*_
from chinese_calendar import is_workday
import win32com.client
import datetime
import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'CRHC_ATTENDANCE.settings'
django.setup()

from Attendance import models
name = models.Name.objects.all().values('user_num', 'user_name')
b = [i['user_num'] for i in name]


def get_user_name(number):
	print('开始获取用户数据！')
	zk.ReadAllUserID(number)  # 读取打卡机数据
	user_number = 0

	while 1:
		# 获取打卡机数据, 并放到对应的变量
		num_id, user_id, user_name, user_pw, user_root, user_xx = zk.SSR_GetAllUserInfo(1)
		if not num_id:
			break
		else:
			if user_id not in b:
				user_number += 1
				models.Name.objects.create(user_num=user_id, user_name=user_name)
			# idName[user_id] = user_name
	print('获取到%s条用户，已上传' % user_number)


def get_user_time(number, date=None):
	print('开始获取打卡记录')
	# 获取用户的打卡时间，接受一个参数和可选参数。
	# number:机器号，
	# date：如果传入指定日期的列表，将获取指定日期的打卡记录，如果不传入date值，将获取打卡机上所有的打卡记录。
	user_time = 0
	zk.ReadGeneralLogData(number)  # 读取打卡机数据

	while 1:
		# 获取打卡机数据
		exists, name_id, func, mode, year, month, day, hour, minute, second, work = zk.SSR_GetGeneralLogData(1)
		if not exists:
			break
		else:
			if date is not None:
				if year == date.year and month == date.month and day == date.day:
					date_date = '%s-%s-%s' % (year, month, day)
					time = '%s:%s:%s' % (hour, minute, second)
					if name_id in b:
						models.GeneralTable.objects.create(
							user_num=name_id,
							user_name=name[b.index(name_id)]['user_name'],
							user_date=date_date, user_time=time
						)
						user_time += 1
					else:
						models.GeneralTable.objects.create(
							user_num=name_id, user_name=name_id, user_date=date_date, user_time=time
						)
						user_time += 1

			else:
				date_date = '%s-%s-%s' % (year, month, day)
				time = '%s:%s:%s' % (hour, minute, second)
				if name_id in b:
					models.GeneralTable.objects.create(
						user_num=name_id,
						user_name=name[b.index(name_id)]['user_name'],
						user_date=date_date, user_time=time
					)
					user_time += 1
				else:
					models.GeneralTable.objects.create(
						user_num=name_id, user_name=name_id, user_date=date_date, user_time=time
					)
					user_time += 1
	print('获取到%s条打卡记录，已上传' % user_time)


def filtering(date):
	print('开始判断用户打卡记录')

	def time_handle(time):
		return datetime.datetime.strptime(time, '%H:%M:%S').time()

	if is_workday(date):
		names = models.Name.objects.all().values('user_name', 'user_num')
		for i in names:  # 循环每个用户
			morning = None  # 保存上午的状态
			noon = None  # 保存中午午的状态
			afternoon = None  # 保存下午的状态
			records = models.GeneralTable.objects.filter(user_num=i['user_num'], user_date=date)
			# 查询对应ID、日期的打卡记录，并做时间判断
			for records in records:
				if records.user_time <= time_handle('9:15:00'):
					morning = '正常'

				elif time_handle('09:15:00') < records.user_time <= time_handle('9:45:00'):
					if morning != '正常':
						morning = '迟到'

				elif time_handle('13:10:00') <= records.user_time <= time_handle('13:30:00'):
					if sale_time:  # 如果sale_time为True 执行下面的语句，
						noon = '正常'

				elif time_handle('13:30:00') < records.user_time <= time_handle('14:00:00'):
					if sale_time:
						if noon != '正常':
							noon = '迟到'

				elif time_handle('17:30:00') <= records.user_time < time_handle('18:00:00'):
					if afternoon != '正常':
						afternoon = '早退'

				elif time_handle('18:00:00') <= records.user_time:
					if afternoon != '正常':
						afternoon = '正常'

			if morning is None:
				morning = '旷工'
			if noon is None:
				if sale_time:
					noon = '旷工'
			if afternoon is None:
				afternoon = '旷工'

			if sale_time:
				models.DataScreen.objects.create(
					check_num=i['user_num'],
					check_name=i['user_name'],
					check_date=date,
					check_morning=morning,
					check_noon=noon,
					check_afternoon=afternoon
				)
			else:
				models.DataScreen.objects.create(
					check_num=i['user_num'],
					check_name=i['user_name'],
					check_date=date,
					check_morning=morning,
					check_afternoon=afternoon
				)
		print('%s判断完成，并上传到汇总表' % date)
	else:
		print('%s不是工作日' % date)


if __name__ == '__main__':
	zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')  # 获取中控API
	zk.Connect_Net('192.168.1.36', 4370)

	idName = {}
	sale_time = True

	get_date = datetime.date.today()  # 获取当天的日期
	yesterday = get_date + datetime.timedelta(-1)  # 获取前一天的日期
	appoint_date = datetime.datetime.strptime('2021-6-28', '%Y-%m-%d').date()  # 指定日期

	# get_user_name(1)
	# get_user_time(1, )

	filtering(appoint_date)

	zk.Disconnect()
