import datetime

def GetAnswer(mainLogic=0):
	return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")