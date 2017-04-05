import datetime

def get_time(idx):
	days = 0 - idx / 1440
	minutes = 0 - idx % 1440
	return datetime.datetime.now()+datetime.timedelta(days = days, minutes = minutes) 
