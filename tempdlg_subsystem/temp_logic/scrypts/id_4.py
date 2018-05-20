import datetime

def execute(*args):
	return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")