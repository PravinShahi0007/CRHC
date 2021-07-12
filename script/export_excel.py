from openpyxl import Workbook
# from openpyxl.styles import Alignment
import winreg


def get_desktop():
	# 获取电脑桌面路径
	key = winreg.OpenKey(
		winreg.HKEY_CURRENT_USER,
		r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
	)
	return winreg.QueryValueEx(key, 'Desktop')[0]


def general_table(data):
	# 将指定的打卡记录导出到Excel
	wb = Workbook()
	ws = wb.active
	ws.title = '打卡记录'
	ws.column_dimensions['D'].width = 14
	ws.column_dimensions['C'].width = 14
	ws.append(['编号', '姓名', '打卡日期', '打卡时间'])
	for i in data:
		ws.append([i.user_num, i.user_name, i.user_date, i.user_time])
	b = r'%s\打卡日期.xlsx' % get_desktop()
	wb.save(b)


# def data_screen_table(data):
# 	wb = Workbook()
# 	ws = wb.active
# 	ws.title = '分析表'
# 	ws.column_dimensions['C'].width = 14
# 	ws.column_dimensions['E'].width = 20
# 	ws.append(['编号', '姓名', '打卡日期', '标记', '状态'])
# 	for i in data:
# 		ws.append([i.check_num, i.check_name, i.check_date, i.check_state, q[i.check_state]])
# 	b = r'%s\分析表.xlsx' % get_desktop()
# 	wb.save(b)
