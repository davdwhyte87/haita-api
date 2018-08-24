# from datetime import date,datetime,timedelta
# current_date=datetime.now()
# expdate=current_date+timedelta(days=1)
# print("%s  ,    %s"%(current_date,expdate))
import json
roles="1;3;3;4;4;5;5;5"
r=[int(x) for x in roles.split(';')]
print(type(r))
