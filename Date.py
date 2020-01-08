import time
from datetime import datetime 
 
class Date():
    
     # Function to get the current minutes, hour, day, month and year.
    def get_date(self):
        return int(time.time())
        #return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

