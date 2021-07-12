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
	print('��ʼ��ȡ�û����ݣ�')
	zk.ReadAllUserID(number)  # ��ȡ�򿨻�����
	user_number = 0

	while 1:
		# ��ȡ�򿨻�����, ���ŵ���Ӧ�ı���
		num_id, user_id, user_name, user_pw, user_root, user_xx = zk.SSR_GetAllUserInfo(1)
		if not num_id:
			break
		else:
			if user_id not in b:
				user_number += 1
				models.Name.objects.create(user_num=user_id, user_name=user_name)
			# idName[user_id] = user_name
	print('��ȡ��%s���û������ϴ�' % user_number)


def get_user_time(number, date=None):
	print('��ʼ��ȡ�򿨼�¼')
	# ��ȡ�û��Ĵ�ʱ�䣬����һ�������Ϳ�ѡ������
	# number:�����ţ�
	# date���������ָ�����ڵ��б�����ȡָ�����ڵĴ򿨼�¼�����������dateֵ������ȡ�򿨻������еĴ򿨼�¼��
	user_time = 0
	zk.ReadGeneralLogData(number)  # ��ȡ�򿨻�����

	while 1:
		# ��ȡ�򿨻�����
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
	print('��ȡ��%s���򿨼�¼�����ϴ�' % user_time)


def filtering(date):
	print('��ʼ�ж��û��򿨼�¼')

	def time_handle(time):
		return datetime.datetime.strptime(time, '%H:%M:%S').time()

	if is_workday(date):
		names = models.Name.objects.all().values('user_name', 'user_num')
		for i in names:  # ѭ��ÿ���û�
			morning = None  # ���������״̬
			noon = None  # �����������״̬
			afternoon = None  # ���������״̬
			records = models.GeneralTable.objects.filter(user_num=i['user_num'], user_date=date)
			# ��ѯ��ӦID�����ڵĴ򿨼�¼������ʱ���ж�
			for records in records:
				if records.user_time <= time_handle('9:15:00'):
					morning = '����'

				elif time_handle('09:15:00') < records.user_time <= time_handle('9:45:00'):
					if morning != '����':
						morning = '�ٵ�'

				elif time_handle('13:10:00') <= records.user_time <= time_handle('13:30:00'):
					if sale_time:  # ���sale_timeΪTrue ִ���������䣬
						noon = '����'

				elif time_handle('13:30:00') < records.user_time <= time_handle('14:00:00'):
					if sale_time:
						if noon != '����':
							noon = '�ٵ�'

				elif time_handle('17:30:00') <= records.user_time < time_handle('18:00:00'):
					if afternoon != '����':
						afternoon = '����'

				elif time_handle('18:00:00') <= records.user_time:
					if afternoon != '����':
						afternoon = '����'

			if morning is None:
				morning = '����'
			if noon is None:
				if sale_time:
					noon = '����'
			if afternoon is None:
				afternoon = '����'

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
		print('%s�ж���ɣ����ϴ������ܱ�' % date)
	else:
		print('%s���ǹ�����' % date)


if __name__ == '__main__':
	zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')  # ��ȡ�п�API
	zk.Connect_Net('192.168.1.36', 4370)

	idName = {}
	sale_time = True

	get_date = datetime.date.today()  # ��ȡ���������
	yesterday = get_date + datetime.timedelta(-1)  # ��ȡǰһ�������
	appoint_date = datetime.datetime.strptime('2021-6-28', '%Y-%m-%d').date()  # ָ������

	# get_user_name(1)
	# get_user_time(1, )

	filtering(appoint_date)

	zk.Disconnect()
