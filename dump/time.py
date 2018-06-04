from datetime import date,datetime,timedelta
current_date=datetime.now()
expdate=current_date+timedelta(days=1)
print("%s  ,    %s"%(current_date,expdate))