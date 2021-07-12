
def update_leave(data, data2):
	# 外出、报备更新
	for i in data:
		b = data2.filter(check_name=i.leave_name, check_date=i.leave_date)
		if i.leave_time_interval == '上午':
			b.update(check_morning='正常')
		elif i.leave_time_interval == '中午':
			b.update(check_noon='正常')
		elif i.leave_time_interval == '下午':
			b.update(check_afternoon='正常')
		elif i.leave_time_interval == '全天':
			b.update(check_morning='正常', check_noon='正常', check_afternoon='正常')


def update_register(data, data2):
	# 请假更新
	for i in data:
		b = data2.filter(
			check_name=i.register_name,
			check_date=i.register_date
		)
		if i.register_time == '上午':
			b.update(
				check_morning='正常',
				check_state=i.register_type,
				check_day=i.register_day
			)
		elif i.register_time == '下午':
			b.update(
				check_noon='正常',
				check_afternoon='正常',
				check_state=i.register_type,
				check_day=i.register_day
			)
		elif i.register_time == '全天':
			b.update(
				check_morning='正常',
				check_noon='正常',
				check_afternoon='正常',
				check_state=i.register_type,
				check_day=i.register_day
			)
