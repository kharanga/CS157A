import re
from datetime import datetime

def checkEmail(email):
 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
    	return True
 
    else:
        return False

def checkDate(date):
	dateFormatted = datetime.strptime(date, "%Y-%m-%d")
	today = datetime.today()
	if(dateFormatted < today):
		return False
	else:
		return True